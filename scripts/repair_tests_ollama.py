import subprocess, sys, pathlib, re

MODEL = "llama3.2"
FENCE = re.compile(r"```(?:python)?\s*(.*?)```", re.S|re.I)

REPAIR_PROMPT = """You are a Python unit-test repairer.

Rewrite the ENTIRE pytest file below so that it is correct and increases BRANCH coverage.
Return ONLY one ```python fenced block``` with the corrected tests.

Constraints (mandatory):
- Import the target function exactly: {import_line}
- Use only the public function {func_sig}.
- No external libraries.
- Avoid near-duplicates; each test should hit a distinct branch.
- Keep brief comments per test describing the branch.

Function spec (for correctness):
{spec}

Current test file content:
{current}

java
Copy code

Pytest failure output (trimmed):
{failure}

pgsql
Copy code
"""

SPECS = {
    "is_anagram": """is_anagram(a: str, b: str) -> bool
- A1 behavior (as you decided): lowercase, strip spaces/punct, ignore digits (letters only).
- Branches to exercise: phrase true, punct-only true, count mismatch false, empty vs non-empty false, digits ignored case true, both empty true.""",
    "word_wrap": """word_wrap(text: str, width: int) -> list[str]
- GREEDY: add word if len(cur)+(1 if cur else 0)+len(word) <= width.
- Long word (>width): if cur non-empty flush, then put word alone (no splitting).
- NO trailing spaces. All len(line) <= width. " ".join(out) == original (normal cases).
- Branches: equality fits, exceed-by-one break, long-word when cur empty vs non-empty, empty text, width=1."""
}

IMPORTS = {
    "is_anagram": "from problems.problems import is_anagram",
    "word_wrap": "from problems.problems import word_wrap",
}
SIGS = {
    "is_anagram": "is_anagram(a: str, b: str) -> bool",
    "word_wrap": "word_wrap(text: str, width: int) -> list[str]",
}

def run_pytest_on(path: pathlib.Path):
    res = subprocess.run([sys.executable, "-m", "pytest", str(path), "-q"],
                         capture_output=True, text=True)
    return res.returncode, (res.stdout + "\n" + res.stderr)[-4000:]

def ask_llm(prompt: str, model: str = MODEL) -> str:
    res = subprocess.run(["ollama", "run", model],
                         input=prompt, text=True,
                         capture_output=True, timeout=600)
    txt = res.stdout
    m = FENCE.search(txt)
    return (m.group(1) if m else txt).strip()

def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/repair_tests_ollama.py <is_anagram|word_wrap> <test_file.py> [rounds]")
        sys.exit(1)
    prob = sys.argv[1]
    test_path = pathlib.Path(sys.argv[2])
    rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 2

    for i in range(rounds+1):
        rc, fail = run_pytest_on(test_path)
        if rc == 0:
            print(f"[ok] Tests pass: {test_path}")
            return
        current = test_path.read_text()
        prompt = REPAIR_PROMPT.format(
            import_line=IMPORTS[prob],
            func_sig=SIGS[prob],
            spec=SPECS[prob],
            current=current,
            failure=fail,
        )
        fixed = ask_llm(prompt)
        test_path.write_text(fixed + "\n")
        print(f"[repair] Rewrote {test_path} (round {i+1})")
    print("[warn] Still failing after repair rounds.")

if __name__ == "__main__":
    main()
