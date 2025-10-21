import os

dirs = [
    "problems",
    "tests",
    "prompts",
    "runs/raw_generations",
    "eval",
    "scripts"
]

files = {
    "problems/__init__.py": "",
    "tests/__init__.py": "",
    "runs/results.jsonl": "",
    "runs/metrics.json": "",
    "README.md": "# LLM Code Generation Assignment\n",
    "requirements.txt": "pytest\n",
}

for d in dirs:
    os.makedirs(d, exist_ok=True)

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

print("Directory structure created successfully.")
