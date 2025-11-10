import os, pathlib, sys, argparse, re
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

DEFAULT_MODEL = "models/gemini-2.5-flash"

TEST_PROMPT_TEMPLATE = """You are a Python unit-test generator.

Context: You are writing harmless software unit tests for a classroom assignment. 
No biological, political, or unsafe content is involved; these are simple algorithmic functions.

Goal: Increase BRANCH coverage for `problems/problems.py::{func}`.

Write pytest tests in a NEW file. 
Rules:
- Use only the public function {func}{signature_suffix}.
- Avoid near-duplicates; target distinct conditional outcomes.
- Add short comments explaining which branch each test exercises.
- Do NOT import external libraries.
- Return ONLY one ```python fenced block with the tests```.

Branches / cases to hit:
{hints}
"""

HINTS = {
    "is_anagram": """Normalization (.isalnum + lower), punctuation/space ignored, digits retained.
Include:
- "A decimal point" vs "I'm a dot in place" -> True
- "Dormitory123" vs "Dirty room 321" -> True
- only punctuation vs punctuation -> True
- "aabbc" vs "abbc" -> False
- "" vs "abc" -> False
- Optionally: digits-only-one-side -> False; both-empty -> True""",
    "word_wrap": """Greedy equality; break when exceed; long word > width goes alone (flush current first if non-empty); empty text; width=1 edge.
Include:
- "a bc", 4 -> ["a bc"]            # equality fits exactly
- "ab cdefghij k", 5 -> ["ab","cdefghij","k"]  # flush before long word
- "", 7 -> []
- "This is a small piece of text to wrap.", 10 -> lengths<=10 and join equals original
- "a bb c", 1 -> ["a","bb","c"]
- "superlongword", 5 -> ["superlongword"]""",
}

SIG_SUFFIX = {
    "is_anagram": "(a: str, b: str) -> bool",
    "word_wrap": "(text: str, width: int) -> list[str]",
}

FENCE_RE = re.compile(r"```(?:python)?\s*(.*?)```", re.S | re.I)

def extract_fenced(text: str) -> str:
    m = FENCE_RE.search(text or "")
    if not m:
        return (text or "").strip()
    return m.group(1).strip()

def response_to_text(resp) -> str:
    """
    Be robust to empty candidates/parts and SAFETY blocks.
    Returns the concatenated text (may be empty).
    """
    try:
        # Prefer candidates->content.parts->text
        if getattr(resp, "candidates", None):
            for cand in resp.candidates:
                # collect any text parts
                parts = []
                if getattr(cand, "content", None) and getattr(cand.content, "parts", None):
                    for p in cand.content.parts:
                        t = getattr(p, "text", None)
                        if t:
                            parts.append(t)
                if parts:
                    return "\n".join(parts)
        # Fallback to resp.text quick accessor (may raise in some SDK versions)
        return getattr(resp, "text", "") or ""
    except Exception:
        return ""

def explain_failure(resp):
    # Print diagnostics once so you know why it failed (safety, tokens, etc.)
    try:
        fr_list = []
        if getattr(resp, "candidates", None):
            for cand in resp.candidates:
                fr_list.append(str(getattr(cand, "finish_reason", None)))
        pf = getattr(resp, "prompt_feedback", None)
        print("[generate_tests_google] No text returned.")
        if fr_list:
            print("  finish_reason(s):", fr_list)
        if pf:
            print("  prompt_feedback:", pf)
    except Exception as e:
        print("  (could not inspect response:", e, ")")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--problem", required=True, choices=list(HINTS.keys()))
    ap.add_argument("--outfile", required=True)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--temperature", type=float, default=0.1)
    args = ap.parse_args()

    assert os.environ.get("GOOGLE_API_KEY"), "Set GOOGLE_API_KEY"
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # Build safety_settings that works across SDK versions
    _safety = {}
    for name in [
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_HARASSMENT",
        "HARM_CATEGORY_DANGEROUS_CONTENT",
        "HARM_CATEGORY_CIVIC_INTEGRITY",
        # sexual categories vary by SDK version; try both common spellings:
        "HARM_CATEGORY_SEXUAL_AND_MINORS",
        "HARM_CATEGORY_SEXUAL_CONTENT",
    ]:
        cat = getattr(HarmCategory, name, None)
        if cat is not None:
            _safety[cat] = HarmBlockThreshold.BLOCK_NONE

    model = genai.GenerativeModel(
        args.model,
        system_instruction=(
            "You are generating harmless Python unit tests for simple algorithms. "
            "Avoid any unsafe content. Output only code when asked."
        ),
        safety_settings=_safety,
    )



    prompt = TEST_PROMPT_TEMPLATE.format(
        func=args.problem,
        signature_suffix=SIG_SUFFIX[args.problem],
        hints=HINTS[args.problem],
    )

    # Lower temp, set plain text, and reasonable token budget
    resp = model.generate_content(
        prompt,
        generation_config={
            "temperature": args.temperature,
            "max_output_tokens": 1200,
            "response_mime_type": "text/plain",
        },
        # You can also relax or customize safety settings if needed:
        # safety_settings={"HARASSMENT": "block_none", ...}
        request_options={"timeout": 90},
    )

    text = response_to_text(resp)
    if not text.strip():
        explain_failure(resp)
        sys.exit(2)

    code = extract_fenced(text)
    pathlib.Path(args.outfile).write_text(code + "\n")
    print(f"Wrote {args.outfile}")

if __name__ == "__main__":
    main()
