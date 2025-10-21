import json, math, collections, sys

def comb(n, k):
    if k < 0 or k > n: return 0
    return math.comb(n, k)

def pass_at_k(n, c, k):
    if n < k: return None
    return 1.0 - comb(n - c, k) / comb(n, k)

def aggregate(results_path: str, ks=(1,5)):
    """
    results.jsonl lines with:
    {
      "problem": "two_sum",
      "model_family": "gpt",
      "model_name": "gpt-5-thinking",
      "strategy": "cot",
      "sample_id": 3,
      "passed": true
    }
    """
    by_key = collections.defaultdict(list)
    with open(results_path, "r") as f:
        for line in f:
            r = json.loads(line)
            key = (r["problem"], r["model_family"], r["model_name"], r["strategy"])
            by_key[key].append(bool(r["passed"]))

    table = []
    for key, passes in sorted(by_key.items()):
        n = len(passes)
        c = sum(passes)
        row = {
            "problem": key[0],
            "model_family": key[1],
            "model_name": key[2],
            "strategy": key[3],
            "n": n,
            "c": c,
        }
        for k in ks:
            v = pass_at_k(n, c, k)
            row[f"pass@{k}"] = None if v is None else round(v, 4)
        table.append(row)
    return table

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "runs/results.jsonl"
    tbl = aggregate(path)
    print(json.dumps(tbl, indent=2))

