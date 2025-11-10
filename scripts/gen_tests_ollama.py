# scripts/gen_tests_ollama.py
import subprocess, sys, pathlib, re

PROMPT_TMPL = """You are a Python unit-test generator.

Goal: Increase **BRANCH** coverage for the function {func} in its split module.

Write pytest tests in a NEW file.

Rules:
- MUST include as the first non-comment line: {import_line}
- Use only the public function: {func}{sig}
- Target DISTINCT conditional outcomes (no near-duplicates).
- Prefer minimal, focused tests that each hit a different branch.
- Add a short comment above each test stating *which branch* it targets.
- Do not import external libraries.
- Return ONLY one ```python fenced block``` containing valid tests.

Branches / cases to hit:
{hints}
"""


FENCE = re.compile(r"```(?:python)?\s*(.*?)```", re.S | re.I)

# ---- Per-problem metadata (imports + signatures + coverage-aware hints) ----

# NOTE: These import lines assume you've split implementations into:
#   problems/longest_common_prefix.py  (exports longest_common_prefix)
#   problems/valid_parentheses.py      (exports valid_parentheses)
IMPORT = {
    "longest_common_prefix": "from problems.longest_common_prefix import longest_common_prefix",
    "valid_parentheses":     "from problems.valid_parentheses import valid_parentheses",
}

SIG = {
    "longest_common_prefix": "(strs: list[str]) -> str",
    "valid_parentheses":     "(s: str) -> bool",
}

HINTS = {
    "longest_common_prefix": """Early mismatch; full word as prefix; empty list; single element; progressive shrink.
Cover:
- classic positive: ["flower","flow","flight"] -> "fl"
- early mismatch: ["dog","racecar","car"] -> ""
- empty input: [] -> ""
- single element: ["solo"] -> "solo"
- progressive shrink: ["interview","internet","internal"] -> "inte" """,

    "valid_parentheses": """Success path vs three failure branches:
- closing on empty stack: ")" -> False
- mismatched type: "(]" -> False
- leftover stack at end: "(" -> False
Also include nested valid: "{[]}" -> True and mixed valids like "()[]{}". """,
}

ALL_PROBLEMS = ["longest_common_prefix", "valid_parentheses"]

def run_ollama(prompt: str, model: str, timeout_sec: int = 600) -> str:
    res = subprocess.run(
        ["ollama", "run", model],
        input=prompt, text=True, capture_output=True, timeout=timeout_sec
    )
    txt = (res.stdout or "").strip()
    m = FENCE.search(txt)
    return (m.group(1) if m else txt).strip()

def emit_for_problem(prob: str, outfile: pathlib.Path, model: str):
    prompt = PROMPT_TMPL.format(
        func=prob,
        sig=SIG[prob],
        import_line=IMPORT[prob],
        hints=HINTS[prob]
    )
    code = run_ollama(prompt, model=model)
    # safety: prepend the required import if the model forgot it
    if IMPORT[prob] not in code:
        code = f"{IMPORT[prob]}\n\n{code}"
    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text(code + "\n")
    print(f"Wrote {outfile}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/gen_tests_ollama.py <longest_common_prefix|valid_parentheses|ALL> <outfile or DIR> [model]")
        print("Examples:")
        print("  python scripts/gen_tests_ollama.py longest_common_prefix tests/test_ext_lcp_iter1.py llama3.2")
        print("  python scripts/gen_tests_ollama.py valid_parentheses tests/test_ext_validpar_iter1.py llama3.2")
        print("  python scripts/gen_tests_ollama.py ALL tests/ qwen2.5:7b-instruct")
        sys.exit(1)

    sel = sys.argv[1]
    out_arg = pathlib.Path(sys.argv[2])
    model = sys.argv[3] if len(sys.argv) > 3 else "llama3.2"

    if sel == "ALL":
        if out_arg.suffix:
            print("When using ALL, provide a directory for the second arg.", file=sys.stderr)
            sys.exit(2)
        for p in ALL_PROBLEMS:
            emit_for_problem(p, out_arg / f"test_ext_{p}_iter1.py", model)
    else:
        if sel not in ALL_PROBLEMS:
            print(f"Unknown problem '{sel}'. Choose from: {', '.join(ALL_PROBLEMS)} or ALL")
            sys.exit(2)
        emit_for_problem(sel, out_arg, model)

if __name__ == "__main__":
    main()
