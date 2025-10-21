# scripts/generate_samples_llama.py
import os, time, pathlib, re, argparse, requests, ast

CODE_FENCE_RE = re.compile(r"```(?:python)?\s*(.*?)```", flags=re.S | re.I)

PROBLEMS = {
    "two_sum": {"signature": "def two_sum(nums: list[int], target: int) -> tuple[int,int] | None:", "task": "Find indices i<j with nums[i]+nums[j]==target; return (i,j) else None."},
    "is_anagram": {"signature": "def is_anagram(a: str, b: str) -> bool:", "task": "Case-insensitive; ignore spaces/punctuation; return True if anagrams."},
    "roman_to_int": {"signature": "def roman_to_int(s: str) -> int:", "task": "Convert Roman numeral (<=3999) to integer."},
    "longest_common_prefix": {"signature": "def longest_common_prefix(strs: list[str]) -> str:", "task": "Return longest common prefix of strs or ''."},
    "valid_parentheses": {"signature": "def valid_parentheses(s: str) -> bool:", "task": "Validate (), [], {} are balanced and properly nested."},
    "rotate_matrix_90_clockwise": {"signature": "def rotate_matrix_90_clockwise(m: list[list[int]]) -> list[list[int]]:", "task": "Return the 90-degree clockwise rotation of a square matrix."},
    "merge_intervals": {"signature": "def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:", "task": "Merge overlapping [start,end] intervals and return sorted."},
    "nth_fib": {"signature": "def nth_fib(n: int) -> int:", "task": "0-indexed Fibonacci; n>=0."},
    "sum_of_primes_upto": {"signature": "def sum_of_primes_upto(n: int) -> int:", "task": "Sum all primes <= n (n>=0)."},
    "word_wrap": {"signature": "def word_wrap(text: str, width: int) -> list[str]:", "task": "Greedy wrap on spaces; no line exceeds width; words longer than width occupy a single line."},
}

STRATEGIES = {
    "cot": "Think briefly about algorithm & edge cases, then provide the final function.",
    "self_repair": "Write the function, mentally test 3 edge cases, revise once if needed, and output only the final function.",
    "debug_hint": (
    "You previously failed tests. Produce a corrected implementation.\n"
    "MANDATORY: exact signature, no I/O/imports, Python 3.11, return only one ```python fenced block```.\n"
    "General pitfalls to fix:\n"
    "- Handle empty inputs and boundary conditions.\n"
    "- Validate tricky edge cases before returning.\n"
    "- Keep the algorithm simple and deterministic.\n"
),
}

DEBUG_HINTS = {
    "word_wrap": """
Specific to word_wrap:
- Use GREEDY packing: add next word only if len(current_line) + (1 if current_line else 0) + len(word) <= width.
- If len(word) > width, emit that word on its own line (do NOT split).
- Return List[str] with no trailing spaces. Keep word order. Handle empty text and width>=1.
- Mental checks:
  text="a bc def", width=4 => ["a bc","def"]
  text="superlong", width=5 => ["superlong"]
  text="", width=5 => []
"""
}


def extract_code(text: str) -> str:
    m = CODE_FENCE_RE.search(text)
    return m.group(1).strip() if m else text.strip()

def expected_name(sig: str) -> str:
    m = re.match(r"\s*def\s+([a-zA-Z_]\w*)\s*\(", sig)
    return m.group(1) if m else ""

def compilable(src: str) -> bool:
    try:
        ast.parse(src)
        return True
    except SyntaxError:
        return False

def build_prompt(task, signature, strategy):
    return f"""You are a Python expert. Follow the rules strictly.

Task:
{task}

Strategy:
{strategy}

Function signature (must match exactly):
{signature}

Output format (MANDATORY):
Begin your answer with exactly:
```python
and end with:
"""

def llama_generate(prompt, model="codellama:7b-instruct", temperature=0.1, retries=1):
    """
    Call Ollama local API with a long timeout (first load of weights can be slow).
    No stop tokens; we rely on fenced extraction.
    """
    opts = {
        "temperature": temperature,
        "num_predict": 896,   # more room to avoid truncation
        "top_p": 0.9,
        "repeat_penalty": 1.05,
        # no "stop" here
    }
    base = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    url = f"{base}/api/generate"

    last_err = None
    for _ in range(retries + 2):  # one extra retry
        try:
            r = requests.post(
                url,
                json={"model": model, "prompt": prompt, "stream": False, "options": opts},
                timeout=600,  # allow model to load on first call
            )
            if r.status_code == 200:
                text = r.json().get("response", "")
                if text and text.strip():
                    return text
            else:
                last_err = f"status={r.status_code}, body={r.text[:200]}"
        except requests.exceptions.ReadTimeout as e:
            last_err = f"timeout: {e}"
        except Exception as e:
            last_err = str(e)
        time.sleep(3)

    print(f"[ERROR] Ollama generate failed after retries ({last_err})")
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--problem", required=True)
    ap.add_argument("--strategy", choices=list(STRATEGIES.keys()), required=True)
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--model", default="llama3.2")  
    ap.add_argument("--temperature", type=float, default=0.1)
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parents[1]
    out_root = root / "runs" / "raw_generations"
    out_root.mkdir(parents=True, exist_ok=True)

    meta = PROBLEMS[args.problem]
    sig = meta["signature"]
    fname = expected_name(sig)
    strat_note = STRATEGIES[args.strategy]

    for i in range(args.n):
        prompt = build_prompt(meta["task"], sig, strat_note)
        if args.strategy == "debug_hint":
            prompt = prompt + "\n" + DEBUG_HINTS.get(args.problem, "")
        raw = llama_generate(prompt, model=args.model, temperature=args.temperature, retries=1)
        if not raw:
            print(f"[ERROR] No text for {args.problem}/{args.strategy}/sample_{i}")
            continue

        code = extract_code(raw)

        # Ensure correct function name/signature appears; if not, one stricter retry
        if f"def {fname}(" not in code:
            strict = prompt + "\n\nYour last output did not keep the exact function name/signature. Fix it now."
            raw2 = llama_generate(strict, model=args.model, temperature=0.0, retries=0)
            if raw2:
                code2 = extract_code(raw2)
                if f"def {fname}(" in code2:
                    code = code2

        # Compile check; if broken, do one retry asking for complete compilable function
        if not compilable(code):
            strict2 = prompt + "\n\nYour last output was incomplete. Return ONLY one fenced ```python``` block with a COMPLETE function that compiles."
            raw3 = llama_generate(strict2, model=args.model, temperature=0.0, retries=0)
            code3 = extract_code(raw3) if raw3 else ""
            if not code3 or not compilable(code3):
                print(f"[ERROR] Non-compilable code for {args.problem}/{args.strategy}/sample_{i}. Skipping.")
                continue
            code = code3

        out_dir = out_root / args.problem / f"llama-{args.model}" / args.strategy
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"sample_{i}.py").write_text(code)
        print(f"✅ Saved {args.problem}/{args.strategy}/sample_{i}")

if __name__ == "__main__":
    main()
