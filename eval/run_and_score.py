# eval/run_and_score.py
import sys, subprocess, json, tempfile, shutil, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

def run_one_sample(problem_name: str, py_path: str) -> bool:
    """
    Run pytest for one generated sample by creating an isolated temp project:
      temp/
        problems/  (original problems.py + appended override function)
        tests/     (copied from repo)
    This ensures tests import the local 'problems' package, not the repo one.
    """
    tmpdir = pathlib.Path(tempfile.mkdtemp())
    try:
        # --- create package layout in temp ---
        pkg = tmpdir / "problems"
        pkg.mkdir(parents=True, exist_ok=True)
        (pkg / "__init__.py").write_text("")

        # combine original problems.py + generated override
        orig = ROOT / "problems" / "problems.py"
        gen_code = pathlib.Path(py_path).read_text()
        combined = orig.read_text().rstrip() + "\n\n# === Override injected ===\n" + gen_code + "\n"
        (pkg / "problems.py").write_text(combined)

        # copy tests into the temp dir
        src_tests = ROOT / "tests"
        dst_tests = tmpdir / "tests"
        shutil.copytree(src_tests, dst_tests)

        # run pytest in the temp dir, targeting just this problem suite
        cmd = [sys.executable, "-m", "pytest", "-q", "-k", problem_name, "tests"]
        proc = subprocess.run(cmd, cwd=tmpdir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        # print(proc.stdout)  # <- uncomment if you want to see details
        return proc.returncode == 0
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--problem", required=True)
    ap.add_argument("--sample_path", required=True)
    args = ap.parse_args()
    ok = run_one_sample(args.problem, args.sample_path)
    print(json.dumps({"problem": args.problem, "sample_path": args.sample_path, "pass": ok}))
