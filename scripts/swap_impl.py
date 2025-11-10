# scripts/swap_impl.py
import shutil, sys, pathlib

root = pathlib.Path(__file__).resolve().parents[1]

def swap(func: str, src_path: str):
    src = root / src_path
    dst = root / "problems" / f"{func}.py"
    if not src.exists():
        raise SystemExit(f"Source not found: {src}")
    shutil.copyfile(src, dst)
    print(f"Swapped in: {dst} <- {src}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/swap_impl.py <function_name> <relative_source_path>")
        print("Example:")
        print("  python scripts/swap_impl.py longest_common_prefix "
              "runs/raw_generations/longest_common_prefix/google-models_gemini-2.5-flash/self_repair/sample_1.py")
        raise SystemExit(2)

    func, rel = sys.argv[1], sys.argv[2]
    swap(func, rel)
