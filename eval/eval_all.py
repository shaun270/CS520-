import pathlib, json, subprocess, sys, os
ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "runs" / "raw_generations"
RESULTS = ROOT / "runs" / "results.jsonl"

def iter_samples():
    for prob_dir in RAW.iterdir():
        if not prob_dir.is_dir(): continue
        problem = prob_dir.name
        for model_dir in prob_dir.iterdir():
            for strat_dir in model_dir.iterdir():
                for sample in strat_dir.glob("sample_*.py"):
                    yield problem, model_dir.name, strat_dir.name, sample

def main():
    RESULTS.write_text("")  # reset; remove this line if you want append-only
    for problem, model_key, strategy, sample_path in iter_samples():
        model_family, model_name = model_key.split("-", 1)
        # run scorer
        out = subprocess.check_output([
            sys.executable, "-m", "eval.run_and_score",
            "--problem", problem,
            "--sample_path", str(sample_path)
        ], text=True).strip()
        ok = json.loads(out)["pass"]
        row = {
            "problem": problem,
            "model_family": model_family,
            "model_name": model_name,
            "strategy": strategy,
            "sample_id": int(sample_path.stem.split("_")[-1]),
            "passed": bool(ok)
        }
        with open(RESULTS, "a") as f:
            f.write(json.dumps(row) + "\n")
        print(row)

    # aggregate
    agg = subprocess.check_output([sys.executable, "-m", "eval.eval_passk", str(RESULTS)], text=True)
    (ROOT / "runs" / "metrics.json").write_text(agg)
    print("\n=== Aggregated pass@k written to runs/metrics.json ===")

if __name__ == "__main__":
    main()
