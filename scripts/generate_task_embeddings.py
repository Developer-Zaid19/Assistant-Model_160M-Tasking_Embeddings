import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
TASKING_PATH = BASE_DIR / "tasking.json"
MODEL_NAME = "all-MiniLM-L6-v2"


def task_text(task):
    return " ".join(
        value.strip()
        for value in [
            task.get("task", ""),
            task.get("type", ""),
            task.get("description", ""),
        ]
        if isinstance(value, str) and value.strip()
    )


def main():
    tasks = json.loads(TASKING_PATH.read_text(encoding="utf-8"))
    model = SentenceTransformer(MODEL_NAME, local_files_only=True)
    vectors = model.encode([task_text(task) for task in tasks])

    for task, vector in zip(tasks, vectors):
        task["embedding"] = [round(float(value), 8) for value in vector.tolist()]

    TASKING_PATH.write_text(json.dumps(tasks, indent=4), encoding="utf-8")


if __name__ == "__main__":
    main()
