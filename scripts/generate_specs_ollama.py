import sys, argparse, pathlib, re, subprocess

# Where to talk to Ollama
DEFAULT_MODEL = "llama3.2"

SPEC_PROMPT_TEMPLATE = """You are a Python *specification* writer.

Your ONLY task:
From the natural-language description and function signature, write **formal
specifications as Python assert statements** that describe the correct behavior
of the function.

You are NOT:
- writing the function implementation,
- writing example calls with concrete values,
- defining any functions,
- assigning example values to variables.

Function description:
{description}

Function signature:
{signature}

Available variables (assume these already exist in the scope):
- The input parameters from the signature (for example: a, b, text, width, etc.).
- A variable named `{result_name}` that holds the expected return value of the function.

You MUST obey all of the following rules:

1. Output **only assert statements**. Every non-empty line in your answer must start with `assert`.
2. Do NOT write any `def` or `return` statements.
3. Do NOT assign to any variables (no lines with `=`). Do NOT write things like `a = "abc"` or `{result_name} = ...`.
4. Do NOT call the function itself inside the assertions.
5. Do NOT use I/O, randomness, or timing (no print, input, files, random, time, etc.).
6. Each assertion must express a general relationship between the inputs and `{result_name}`,
   not a single concrete test case. Do NOT hard-code specific inputs like `"abc"` or `"cba"`.
7. Write **between 5 and 8** logically distinct assert statements.
   They should cover different aspects and cases (empty inputs, boundary conditions,
   positive and negative cases).

Example style (from the assignment, for a Java method `boolean isEven(int n)`):

    assertTrue(res == (n % 2 == 0));

Your Python assertions should follow the same spirit, for example:

    assert res == (n % 2 == 0)

Output format (MANDATORY):
- Return ONLY one ```python fenced block``` containing valid Python code.
- The code must be 5–8 lines, each starting with `assert`.
- No comments, no blank lines, no prose, no other statements.
"""



PROBLEMS = {
    "is_anagram": {
        "description": "...",
        "signature": "def is_anagram(a: str, b: str) -> bool:",
        "result_name": "res",
    },
    "word_wrap": {
        "description": "...",
        "signature": "def word_wrap(text: str, width: int) -> list[str]:",
        "result_name": "lines",
    },
}


FENCE_RE = re.compile(r"```(?:python)?\s*(.*?)```", re.S | re.I)


def extract_code(text: str) -> str:
    m = FENCE_RE.search(text or "")
    if not m:
        return (text or "").strip()
    return m.group(1).strip()


def run_ollama(prompt: str, model: str, timeout_sec: int = 600) -> str:
    """Call `ollama run` and return the raw text response."""
    res = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True,
        timeout=timeout_sec,
    )
    txt = (res.stdout or "").strip()
    return txt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--problem",
        required=True,
        choices=list(PROBLEMS.keys()),
        help="Problem name: is_anagram or word_wrap",
    )
    ap.add_argument(
        "--outfile",
        required=True,
        help="Output path, e.g. specs/is_anagram_specs_raw_ollama.py",
    )
    ap.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Ollama model name (default: llama3.2)",
    )
    args = ap.parse_args()

    meta = PROBLEMS[args.problem]
    prompt = SPEC_PROMPT_TEMPLATE.format(
        description=meta["description"],
        signature=meta["signature"],
        result_name=meta["result_name"],

    )


    raw = run_ollama(prompt, model=args.model)
    code = extract_code(raw)

    out_path = pathlib.Path(args.outfile)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(code + "\n", encoding="utf-8")
    print(f"[OK] Wrote raw specs for {args.problem} to {out_path}")


if __name__ == "__main__":
    main()
