import subprocess
import sys
import pathlib
import re

# You can change the default model if needed
DEFAULT_MODEL = "llama3.r2"


PROMPT_TMPL = """You are a Python unit-test generator.

You are given the natural-language description, function signature, and a set
of formal specification assertions for a function. Use these specifications
to generate pytest tests.

Function description:
{description}

Function signature:
{signature}

Specification assertions (Python-style, about inputs and {result_name}):
```python
{specs}
```

Your goal:

- Generate pytest tests that exercise each of these specification properties.
- Use only the public function {func_name} from problems.problems.
- Target distinct logical cases implied by the specs
  (e.g., empty input, normalization behavior, boundary cases, negative cases).

Rules:

- Import: from problems.problems import {func_name}
- Write functions whose names start with test_.
- Do NOT redefine the function. Do NOT write the implementation.
- Do NOT use external libraries.
- Return ONLY one ```python``` fenced block containing the tests.
"""

# Extract the content of a ```python ... ``` fenced block
FENCE = re.compile(r"```(?:python)?\s*(.*?)```", re.S | re.I)

PROBLEMS = {
    "is_anagram": {
        "description": (
            "Checks if two strings are anagrams. Comparison is case-insensitive, "
            "ignores spaces and punctuation, and considers only letters (a-z). "
            "Digits and other non-letters are ignored. Returns True iff the "
            "normalized strings are anagrams."
        ),
        "signature": "def is_anagram(a: str, b: str) -> bool:",
        "result_name": "res",
        "func_name": "is_anagram",
        # Specs copied from your reviewed specification file
        "specs": """na = [c.lower() for c in a if c.isalpha()]
nb = [c.lower() for c in b if c.isalpha()]
assert res == (sorted(na) == sorted(nb))
if len(na) != len(nb): assert res is False
if not na and not nb: assert res is True
if (not na and nb) or (na and not nb): assert res is False
if sorted(na) == sorted(nb): assert res is True""",
    },
    "word_wrap": {
        "description": (
            "Greedy word wrap: given text and width >= 1, split text into a list "
            "of lines, splitting only at spaces between words. Never split words. "
            "Add a word to the current line if "
            "len(current_line) + (1 if current_line else 0) + len(word) <= width. "
            "If len(word) > width, that word occupies a line by itself (after "
            "flushing any existing current line). If text is empty or width < 1, "
            "the result is []. Returned lines have no leading/trailing spaces."
        ),
        "signature": "def word_wrap(text: str, width: int) -> list[str]:",
        "result_name": "lines",
        "func_name": "word_wrap",
        # Specs copied from your reviewed specification file
        "specs": """words = text.split()
flat = [w for line in lines for w in line.split()]
if not text or width < 1: assert lines == []
assert flat == words
for line in lines:
    if len(line) > width:
        parts = line.split()
        assert len(parts) == 1 and len(parts[0]) > width
    else:
        assert len(line) <= width
if words and width >= max(len(w) for w in words):
    assert all(len(line) <= width for line in lines)
assert all(line != "" for line in lines)""",
    },
}


def run_ollama(prompt: str, model: str, timeout_sec: int = 600) -> str:
    """Call `ollama run <model>` with the given prompt and return the text output.

    This expects Ollama to be installed and the model to be available locally.
    """
    res = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True,
        timeout=timeout_sec,
    )
    txt = (res.stdout or "").strip()
    m = FENCE.search(txt)
    return (m.group(1) if m else txt).strip()


def main() -> None:
    if len(sys.argv) < 3:
        print(
            "Usage: python -m scripts.gen_spec_tests_ollama "
            "<is_anagram|word_wrap> <outfile> [model]"
        )
        print(
            "Example:\n"
            "  python -m scripts.gen_spec_tests_ollama "
            "is_anagram tests/test_spec_is_anagram.py llama3.2"
        )
        sys.exit(1)

    problem = sys.argv[1]
    out_path = pathlib.Path(sys.argv[2])
    model = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_MODEL

    if problem not in PROBLEMS:
        print(f"Unknown problem '{problem}'. Choose from: {', '.join(PROBLEMS.keys())}")
        sys.exit(2)

    meta = PROBLEMS[problem]

    prompt = PROMPT_TMPL.format(
        description=meta["description"],
        signature=meta["signature"],
        result_name=meta["result_name"],
        func_name=meta["func_name"],
        specs=meta["specs"],
    )

    code = run_ollama(prompt, model=model)

    # Safety: ensure correct import is present at the top
    import_line = f"from problems.problems import {meta['func_name']}"
    if import_line not in code:
        code = f"{import_line}\n\n{code}"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(code + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
