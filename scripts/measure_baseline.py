# scripts/measure_baseline.py
import subprocess, sys, xml.etree.ElementTree as ET, re
from pathlib import Path
import inspect, importlib.util

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS_PY = ROOT / "problems" / "problems.py"
XML_OUT = ROOT / "coverage_all.xml"

FUNC_NAME = {
    "two_sum": "two_sum",
    "is_anagram": "is_anagram",
    "roman_to_int": "roman_to_int",
    "longest_common_prefix": "longest_common_prefix",
    "valid_parentheses": "valid_parentheses",
    "rotate_matrix_90_clockwise": "rotate_matrix_90_clockwise",
    "merge_intervals": "merge_intervals",
    "nth_fib": "nth_fib",
    "sum_of_primes_upto": "sum_of_primes_upto",
    "word_wrap": "word_wrap",
}

def load_module_from_path(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod

PROBLEMS_MOD = load_module_from_path("problems_problems", PROBLEMS_PY)

def get_func_span(func_name: str):
    func_obj = getattr(PROBLEMS_MOD, func_name)
    src_lines, start = inspect.getsourcelines(func_obj)
    end = start + len(src_lines) - 1   # inclusive
    return start, end

def run_full_suite():
    if XML_OUT.exists():
        XML_OUT.unlink()

    cmd = [
        sys.executable, "-m", "pytest",
        "--cov=problems",            # instrument problems/
        "--cov-branch",              # collect branch data
        f"--cov-report=xml:{XML_OUT}",   # write XML here
        "--cov-report=term-missing",     # console summary (helps debug)
        "-q",
    ]
    res = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        check=False,
        cwd=str(ROOT),               # RUN FROM PROJECT ROOT
    )

    # Always show logs so if something goes wrong we see it
    sys.stdout.write(res.stdout or "")
    sys.stderr.write(res.stderr or "")

    if not XML_OUT.exists():
        raise FileNotFoundError(
            f"coverage xml was not created at: {XML_OUT}\n"
            f"Return code: {res.returncode}\n"
            f"Working dir: {ROOT}\n"
            f"Command: {' '.join(cmd)}"
        )


FILENAME_RXES = [
    re.compile(r"problems[/\\]problems\.py$"),
    re.compile(r"(?:^|[/\\])problems\.py$"),
]

def pick_class_elem(root: ET.Element):
    classes = list(root.findall(".//class"))
    for c in classes:
        fn = c.get("filename", "")
        if any(rx.search(fn) for rx in FILENAME_RXES):
            return c
    if len(classes) == 1:
        return classes[0]
    # Debug prints if not found
    seen = sorted({c.get("filename", "") for c in classes})
    print("\n[measure_baseline.py] Could not match problems.py in coverage.xml.")
    print("Files present in XML:")
    for f in seen:
        print(" -", f)
    return None

def parse_function_coverage(xml_path: Path, span_start: int, span_end: int):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    cls = pick_class_elem(root)
    if cls is None:
        return 0.0, 0.0

    lines_elem = cls.find("lines")
    if lines_elem is None:
        return 0.0, 0.0

    total_lines = covered_lines = 0
    cond_cov_num = cond_cov_den = 0

    for line in lines_elem.findall("line"):
        n = int(line.get("number", "0"))
        if not (span_start <= n <= span_end):
            continue
        total_lines += 1
        hits = int(line.get("hits", "0"))
        if hits > 0:
            covered_lines += 1
        if line.get("branch") == "true":
            cc = line.get("condition-coverage", "")
            m = re.search(r"\((\d+)/(\d+)\)", cc)
            if m:
                cond_cov_num += int(m.group(1))
                cond_cov_den += int(m.group(2))

    line_pct = round((covered_lines / total_lines * 100), 1) if total_lines else 0.0
    branch_pct = round((cond_cov_num / cond_cov_den * 100), 1) if cond_cov_den else 0.0
    return line_pct, branch_pct

def main():
    run_full_suite()  # runs ALL tests (baseline + your new LLM tests)
    rows = []
    for prob, fname in FUNC_NAME.items():
        start, end = get_func_span(fname)
        lp, bp = parse_function_coverage(XML_OUT, start, end)
        # For Part 2 we don't need per-problem "passed" count—coverage is what matters
        rows.append((prob, lp, bp))

    print("\n| Problem | Line % | Branch % |")
    print("|---|---:|---:|")
    for name, lp, bp in rows:
        print(f"| {name} | {lp} | {bp} |")

if __name__ == "__main__":
    main()
