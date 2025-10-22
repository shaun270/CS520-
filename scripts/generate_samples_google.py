import os, pathlib, time, re, sys, argparse
import google.generativeai as genai


DEFAULT_PRIMARY_MODEL  = "models/gemini-2.5-flash"
DEFAULT_FALLBACK_MODEL = "models/gemini-2.5-flash"
DEFAULT_TEMPERATURE    = 0.2
DEFAULT_N_SAMPLES      = 2
MAX_TOKENS             = 2000
DEFAULT_RETRIES        = 1        
DEFAULT_SLEEP_SECONDS  = 35        


PROBLEMS = {
    "two_sum": {
        "signature": "def two_sum(nums: list[int], target: int) -> tuple[int,int] | None:",
        "task": "Implement the function to find i<j with nums[i]+nums[j]==target and return (i, j), or None if not found."
    },
    "is_anagram": {
        "signature": "def is_anagram(a: str, b: str) -> bool:",
        "task": "Implement the function: case-insensitive, ignore spaces/punctuation, return True if anagrams."
    },
    "roman_to_int": {
        "signature": "def roman_to_int(s: str) -> int:",
        "task": "Implement the function to convert a Roman numeral (<=3999) to integer."
    },
    "longest_common_prefix": {
        "signature": "def longest_common_prefix(strs: list[str]) -> str:",
        "task": "Implement the function returning the longest common prefix of the list, or '' if none."
    },
    "valid_parentheses": {
        "signature": "def valid_parentheses(s: str) -> bool:",
        "task": "Implement the function to validate (), [], {} parentheses are properly nested and balanced."
    },
    "rotate_matrix_90_clockwise": {
        "signature": "def rotate_matrix_90_clockwise(m: list[list[int]]) -> list[list[int]]:",
        "task": "Implement the function returning a new 90-degree clockwise rotation of a square matrix."
    },
    "merge_intervals": {
        "signature": "def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:",
        "task": "Implement the function to merge overlapping [start,end] intervals and return sorted result."
    },
    "nth_fib": {
        "signature": "def nth_fib(n: int) -> int:",
        "task": "Implement the function returning the 0-indexed Fibonacci number; n>=0."
    },
    "sum_of_primes_upto": {
        "signature": "def sum_of_primes_upto(n: int) -> int:",
        "task": "Implement the function summing all primes <= n (n>=0)."
    },
    "word_wrap": {
        "signature": "def word_wrap(text: str, width: int) -> list[str]:",
        "task": "Implement greedy word wrap: no line exceeds width; words longer than width occupy a single line."
    },
}

BASE_TASK = (
    "Write a correct and efficient Python 3.11 implementation for the function described.\n"
    "Rules:\n"
    "- Do not import external libraries.\n"
    "- Do not write I/O or a main guard.\n"
    "- Keep the function name and signature exactly as given.\n"
    "Return ONLY a Python code block with the function implementation."
)

STRATEGIES = {
    "cot": "Briefly consider the algorithm and edge cases, then provide the final function.",
    "self_repair": "Write the function, mentally test edge cases, and adjust once if needed. Output only the final function.",
    "debug_hint": (
    "You previously failed tests. Read carefully and correct the function. "
    "Rules: keep EXACT signature, no I/O/imports, Python 3.11, return only a code fence.\n"
    "General pitfalls to fix:\n"
    "- Handle edge cases and boundary conditions precisely.\n"
    "- Prefer clear, deterministic logic over clever tricks.\n"
    "- Mentally run through the provided test cases before finalizing.\n"
),
}

DEBUG_HINTS = {
    "sum_of_primes_upto": """
Specific to sum_of_primes_upto:
- Sum all primes <= n (inclusive). If n < 2, return 0.
- Use a sieve of Eratosthenes up to n (O(n log log n)) for reliability.
- Corner checks: n=0->0, n=1->0, n=2->2, n=10->17.
""",
    "roman_to_int": """
Specific to roman_to_int:
- Valid subtractives: IV, IX, XL, XC, CD, CM only.
- Iterate with index i; if value[i] < value[i+1], add (value[i+1]-value[i]) and i+=2; else add value[i] and i+=1.
- Inputs are valid Roman (<=3999). Examples: III->3, LVIII->58, MCMXCIV->1994.
"""
}


CODE_FENCE_RE = re.compile(r"```(?:python)?\s*(.*?)```", flags=re.S | re.I)

def extract_code_block(text: str) -> str:
    m = CODE_FENCE_RE.search(text)
    return m.group(1) if m else text

def response_to_text(resp):
    try:
        if getattr(resp, "candidates", None):
            for cand in resp.candidates:
                parts = getattr(cand, "content", None)
                parts = getattr(parts, "parts", []) if parts else []
                out = []
                for p in parts:
                    t = getattr(p, "text", None)
                    if t: out.append(t)
                if out:
                    return "\n".join(out), str(getattr(cand, "finish_reason", None))
        return (getattr(resp, "text", "") or ""), "unknown"
    except Exception as e:
        return "", f"exception:{e}"

def build_prompt(task, signature, strategy_note):
    return f"""{BASE_TASK}

Strategy:
{strategy_note}

Task:
{task}

Function signature:
{signature}
"""

def generate_with_model(model_name: str, prompt: str, temperature: float):
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content(
        prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": MAX_TOKENS,
            "response_mime_type": "text/plain",
        },
        request_options={"timeout": 90},
    )
    text, finish = response_to_text(resp)
    return (text or "").strip(), str(finish)

def try_models(prompt: str, primary_model: str, fallback_model: str, retries: int,
               sleep_between_calls: int, temperature: float):
    for model_name in (primary_model, fallback_model):
        for _ in range(retries + 1):
            text, finish = generate_with_model(model_name, prompt, temperature=temperature)
            time.sleep(sleep_between_calls)  # help avoid 429 on free tier
            if text:
                return model_name, text, finish
    return None, "", "no_text_after_retries"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--problem", help="one problem name (e.g., two_sum)")
    ap.add_argument("--strategy", choices=list(STRATEGIES.keys()), help="one strategy")
    ap.add_argument("--n", type=int, default=DEFAULT_N_SAMPLES, help="num samples")
    ap.add_argument("--model", default=DEFAULT_PRIMARY_MODEL, help="primary model id")
    ap.add_argument("--fallback_model", default=DEFAULT_FALLBACK_MODEL, help="fallback model id")
    ap.add_argument("--sleep", type=int, default=DEFAULT_SLEEP_SECONDS, help="seconds between calls")
    ap.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE, help="sampling temperature")
    ap.add_argument("--retries", type=int, default=DEFAULT_RETRIES, help="retries per model")
    args = ap.parse_args()

    assert os.environ.get("GOOGLE_API_KEY"), "Set GOOGLE_API_KEY"
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    problems_to_run = {args.problem: PROBLEMS[args.problem]} if args.problem else PROBLEMS
    strategies_to_run = {args.strategy: STRATEGIES[args.strategy]} if args.strategy else STRATEGIES

    root = pathlib.Path(__file__).resolve().parents[1]
    out_root = root / "runs" / "raw_generations"
    out_root.mkdir(parents=True, exist_ok=True)

    for prob, meta in problems_to_run.items():
        for strat_key, strat_note in strategies_to_run.items():
            for i in range(int(args.n)):
                prompt = build_prompt(meta["task"], meta["signature"], strat_note)
                if args.strategy == "debug_hint":
                    prompt = prompt + "\n" + DEBUG_HINTS.get(args.problem, "")
                model_used, text, finish = try_models(
                    prompt,
                    primary_model=args.model,
                    fallback_model=args.fallback_model,
                    retries=int(args.retries),
                    sleep_between_calls=int(args.sleep),
                    temperature=float(args.temperature),
                )
                if not text:
                    print(f"[ERROR] No usable text for {prob} / {strat_key} / sample_{i} (finish={finish}). Skipping.", file=sys.stderr)
                    continue
                code = extract_code_block(text)
                out_dir = out_root / prob / f"google-{(model_used or args.model).replace('/', '_')}" / strat_key
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / f"sample_{i}.py").write_text(code)

    print("Done.")

if __name__ == "__main__":
    main()
