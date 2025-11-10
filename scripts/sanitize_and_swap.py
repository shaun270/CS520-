# scripts/sanitize_and_swap.py
import re, shutil, sys, pathlib

def sanitize_and_swap(func_name: str, sample_rel_path: str):
    root = pathlib.Path(__file__).resolve().parents[1]
    src = root / sample_rel_path
    dst = root / "problems" / f"{func_name}.py"
    bak = root / "problems" / f"{func_name}.correct.py"

    if not src.exists():
        raise SystemExit(f"Sample not found: {src}")

    if not bak.exists() and dst.exists():
        shutil.copyfile(dst, bak)

    txt = src.read_text(encoding="utf-8")
    m = re.search(r"```(?:python)?\s*(.*?)```", txt, re.S | re.I)
    code = (m.group(1) if m else txt).strip()

    expected = f"def {func_name}("
    if expected not in code:
        raise SystemExit(f"Sample doesn't contain '{expected}...'. Fix the name/signature in the sample.")

    dst.write_text(code + "\n", encoding="utf-8")
    print(f"[OK] Sanitized & swapped: {dst}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/sanitize_and_swap.py <function_name> <relative_sample_path>")
        print("Example:")
        print("  python scripts/sanitize_and_swap.py longest_common_prefix "
              "runs/raw_generations/longest_common_prefix/google-models_gemini-2.5-flash/self_repair/sample_1.py")
        sys.exit(2)

    sanitize_and_swap(sys.argv[1], sys.argv[2])
