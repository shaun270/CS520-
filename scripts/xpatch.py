
import os
import re
import sys
import json
import time
import shutil
import argparse
import pathlib
import tempfile
import subprocess
from typing import Optional
import google.generativeai as genai
import requests


ROOT = pathlib.Path(__file__).resolve().parents[1]

PROBLEMS = {
    "two_sum": {"signature":"def two_sum(nums: list[int], target: int) -> tuple[int,int] | None:", "task":"Find i<j with nums[i]+nums[j]==target; return (i,j) else None."},
    "is_anagram":{"signature":"def is_anagram(a: str, b: str) -> bool:", "task":"Case-insensitive; ignore spaces/punct; True if anagrams."},
    "roman_to_int":{"signature":"def roman_to_int(s: str) -> int:", "task":"Convert Roman (<=3999) to int."},
    "longest_common_prefix":{"signature":"def longest_common_prefix(strs: list[str]) -> str:", "task":"Longest common prefix or ''."},
    "valid_parentheses":{"signature":"def valid_parentheses(s: str) -> bool:", "task":"Validate (), [], {} balanced & nested."},
    "rotate_matrix_90_clockwise":{"signature":"def rotate_matrix_90_clockwise(m: list[list[int]]) -> list[list[int]]:", "task":"Return m rotated 90° clockwise."},
    "merge_intervals":{"signature":"def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:", "task":"Merge overlapping [start,end] and sort."},
    "nth_fib":{"signature":"def nth_fib(n: int) -> int:", "task":"0-indexed Fibonacci."},
    "sum_of_primes_upto":{"signature":"def sum_of_primes_upto(n: int) -> int:", "task":"Sum all primes <= n."},
    "word_wrap":{"signature":"def word_wrap(text: str, width: int) -> list[str]:", "task":"Greedy wrap on spaces; words longer than width alone line."},
}

BUILDER_PROMPT = """You are a Python expert. Implement the function below.

Task:
{task}

Function signature (must match exactly):
{signature}

Rules:
- Python 3.11 only. No I/O, no external imports.
- Keep the function name and signature exactly as given.
- Return ONLY one fenced ```python code block``` with the complete function. No prose.
"""

EXAMINER_PROMPT = """You are reviewing Python code against a spec and failing tests.
Return a UNIFIED DIFF that minimally fixes the code. If you cannot produce a valid diff, return a single fenced ```python block``` with the full corrected function (no prose).

Spec (task):
{task}

Function signature (must match exactly):
{signature}

Current implementation:
```python
{current_code}
```

Pytest output (if any):

```
{pytest_output}
```

Rules:

* Output ONLY one of:
  1) a unified diff with filenames 'a.py' and 'b.py' (no code fences, no prose), or
  2) a single fenced ```python block``` with the corrected function.
* Keep the same function name & signature. No imports or I/O.
"""

FENCE_RE = re.compile(r"```(?:python)?\s*(.*?)```", re.S | re.I)


def extract_code(txt: str) -> str:
    """Extract code from a ```python fenced block; if none, return text as-is."""
    if not txt:
        return ""
    m = FENCE_RE.search(txt)
    return (m.group(1) if m else txt).strip()

def apply_unified_diff(original: str, diff_txt: str) -> Optional[str]:
    """
    Minimal unified-diff applier (multi-hunk; soft context).
    Falls back to fenced full-function replacement if provided.
    """
    diff_txt = (diff_txt or "").strip()
    if not diff_txt:
        return None
    
    if diff_txt.startswith("```"):
        rep = extract_code(diff_txt)
        return rep if rep else None

    lines = diff_txt.splitlines()
    if len(lines) < 2 or not (lines[0].startswith("--- ") and lines[1].startswith("+++ ")):
        return None

    src = original.splitlines()
    out = []
    i = 0
    idx = 2

    while idx < len(lines):
        if not lines[idx].startswith("@@"):
            idx += 1
            continue

        header = lines[idx]
        idx += 1
        m = re.search(r"@@\s+-(\d+)(?:,(\d+))?\s+\+(\d+)(?:,(\d+))?\s+@@", header)
        if not m:
            return None
        old_start = int(m.group(1))

        while i < old_start - 1 and i < len(src):
            out.append(src[i])
            i += 1

        while idx < len(lines) and not lines[idx].startswith("@@"):
            line = lines[idx]
            if line.startswith("-"):
                if i >= len(src):
                    return None
                i += 1
            elif line.startswith("+"):
                out.append(line[1:])
            elif line.startswith(" "):
                if i >= len(src):
                    return None
                out.append(src[i])
                i += 1
            else:
                return None
            idx += 1
    
    out.extend(src[i:])
    return "\n".join(out)

def write_temp_project(workdir: pathlib.Path, func_src: str) -> None:
    (workdir / "problems").mkdir(parents=True, exist_ok=True)
    (workdir / "problems" / "__init__.py").write_text("")
    
    base_problems_path = ROOT / "problems" / "problems.py"
    if base_problems_path.exists():
        base = base_problems_path.read_text()
        (workdir / "problems" / "problems.py").write_text(
            base.rstrip() + "\n\n# --- candidate ---\n" + func_src + "\n"
        )
    else:
        print(f"Warning: Base problems file not found at {base_problems_path}", file=sys.stderr)
        (workdir / "problems" / "problems.py").write_text(func_src + "\n")

    tests_path = ROOT / "tests"
    if tests_path.exists():
        shutil.copytree(tests_path, workdir / "tests")
    else:
        print(f"Error: Tests directory not found at {tests_path}", file=sys.stderr)
        sys.exit(1)


def run_pytests(workdir: pathlib.Path, kexpr: str, timeout_s: int = 60):
    try:
        p = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-k", kexpr, "tests"],
            cwd=workdir, text=True, capture_output=True, timeout=timeout_s
        )
        return p.returncode == 0, (p.stdout + "\n" + p.stderr)[-6000:]
    except subprocess.TimeoutExpired as e:
        return False, f"[TIMEOUT after {timeout_s}s]\n{(e.stdout or '')}\n{(e.stderr or '')}"

def call_google(model: str, prompt: str) -> str:
    assert os.environ.get("GOOGLE_API_KEY"), "Set GOOGLE_API_KEY"
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    m = genai.GenerativeModel(model)
    for attempt in range(3):
        try:
            r = m.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.2,
                    "max_output_tokens": 2000,
                    "response_mime_type": "text/plain",
                },
                request_options={"timeout": 90},
            )
        except Exception:
            time.sleep(1.0)
            continue
        try:
            if getattr(r, "candidates", None):
                for cand in r.candidates:
                    parts = getattr(cand, "content", None)
                    parts = getattr(parts, "parts", []) if parts else []
                    out = [getattr(p, "text", "") for p in parts if getattr(p, "text", "")]
                    if out:
                        return "\n".join(out)
            txt = getattr(r, "text", None)
            if isinstance(txt, str) and txt.strip():
                return txt
        except Exception:
            pass
        time.sleep(1.0)
    return ""
 
        
def call_ollama(model: str, prompt: str) -> str:
    base = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    url = f"{base}/api/generate"
    opts = {"temperature":0.1, "num_predict":2048, "top_p":0.9, "repeat_penalty":1.05}
    last_err = None
    for _ in range(3):
        try:
            r = requests.post(url, json={"model": model, "prompt": prompt, "stream": False, "options": opts}, timeout=600)
            if r.status_code == 200:
                return r.json().get("response","")
            last_err = f"status={r.status_code}, body={r.text[:200]}"
        except Exception as e:
            last_err = str(e)
        time.sleep(2)
        
    print(f"Ollama call failed after retries: {last_err}", file=sys.stderr) 
    return ""

def gen_code(builder_family: str, builder_model: str, meta: dict) -> str:
    prompt = BUILDER_PROMPT.format(task=meta["task"], signature=meta["signature"])
    raw = call_google(builder_model, prompt) if builder_family=="google" else call_ollama(builder_model, prompt)
    code = extract_code(raw)
    if not code.strip():
        # Stricter fallback: force a single fenced function and exact signature
        strict = (
            "Return ONLY one fenced ```python block``` with a COMPLETE function that COMPILES.\n"
            "Keep EXACT signature:\n"
            f"{meta['signature']}\n\n"
            "Do not include prose, tests, or imports.\n\n"
            f"Task:\n{meta['task']}\n"
        )
        raw2 = call_google(builder_model, strict) if builder_family=="google" else call_ollama(builder_model, strict)
        code2 = extract_code(raw2)
        if code2.strip():
            return code2
    return code

def get_patch_or_replacement(exam_family: str, exam_model: str, meta: dict, code: str, pytest_output: str) -> str:
    prompt = EXAMINER_PROMPT.format(task=meta["task"], signature=meta["signature"], current_code=code, pytest_output=pytest_output)
    return call_google(exam_model, prompt) if exam_family=="google" else call_ollama(exam_model, prompt)

def main():
    ap = argparse.ArgumentParser(description="Cross-family patch-and-test loop (Part 3).")
    ap.add_argument("--problem", required=True, choices=sorted(PROBLEMS.keys()))
    ap.add_argument("--builder_family", choices=["google","llama"], required=True)
    ap.add_argument("--builder_model", required=True)
    ap.add_argument("--exam_family", choices=["google","llama"], required=True)
    ap.add_argument("--exam_model", required=True)
    ap.add_argument("--max_rounds", type=int, default=2)
    args = ap.parse_args()

    meta = PROBLEMS[args.problem]
    kexpr = args.problem

    print(f"--- Round 0: Building '{kexpr}' with {args.builder_family}/{args.builder_model} ---", file=sys.stderr)
    code = gen_code(args.builder_family, args.builder_model, meta)
    if not code.strip():
        print(json.dumps({"round": 0, "passed": False, "error": "Builder returned empty code."}))
        return

    tmp0 = pathlib.Path(tempfile.mkdtemp(prefix="xpatch_r0_"))
    write_temp_project(tmp0, code)
    ok, out = run_pytests(tmp0, kexpr)
    print(json.dumps({"round": 0, "passed": ok}))
    if ok or args.max_rounds <= 0:
        shutil.rmtree(tmp0)
        return

    for r in range(1, args.max_rounds + 1):
        print(f"--- Round {r}: Examining with {args.exam_family}/{args.exam_model} ---", file=sys.stderr)
        suggestion = get_patch_or_replacement(args.exam_family, args.exam_model, meta, code, out)
        patched = apply_unified_diff(code, suggestion)
        
        if not patched:
            rep = extract_code(suggestion)
            if rep.strip().startswith("def "):
                patched = rep
        
        if not patched or patched == code:
            print(json.dumps({"round": r, "patched": False, "reason": "Unusable patch or no change."}))
            break
        
        code = patched
        tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"xpatch_r{r}_"))
        write_temp_project(tmp, code)
        ok, out = run_pytests(tmp, kexpr)
        print(json.dumps({"round": r, "patched": True, "passed": ok}))
        shutil.rmtree(tmp)
        if ok:
            break
    
    shutil.rmtree(tmp0)

if __name__ == "__main__":
    main()
