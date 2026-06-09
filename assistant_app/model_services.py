import json
import math
import os
import subprocess
import webbrowser
from functools import lru_cache
from pathlib import Path
from time import perf_counter
from urllib.parse import quote

import torch
from django.conf import settings
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer

try:
    import requests
except ImportError:  # pragma: no cover - optional until requirements are installed
    requests = None

try:
    import wikipedia
except ImportError:  # pragma: no cover - optional until requirements are installed
    wikipedia = None


@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(settings.EMBEDDING_MODEL_NAME, local_files_only=True)


@lru_cache(maxsize=1)
def get_chat_assets():
    tokenizer = AutoTokenizer.from_pretrained(settings.CHAT_MODEL_PATH, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(settings.CHAT_MODEL_PATH, local_files_only=True)
    model.eval()
    return tokenizer, model


def generate_embedding(text):
    start_time = perf_counter()
    vector = get_embedding_model().encode([text])[0].tolist()
    elapsed_ms = round((perf_counter() - start_time) * 1000, 2)
    preview = ", ".join(f"{value:.4f}" for value in vector[:8])

    return {
        "text": text,
        "model": settings.EMBEDDING_MODEL_NAME,
        "dimension": settings.EMBEDDING_DIMENSION,
        "preview": f"[{preview}, ...]",
        "embedding": vector,
        "generation_time_ms": elapsed_ms,
    }


def _cosine_similarity(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def _tasking_path():
    return Path(settings.BASE_DIR) / "tasking.json"


def _load_tasks():
    with _tasking_path().open("r", encoding="utf-8") as task_file:
        return json.load(task_file)


def _open_desktop_path(path):
    if os.name == "nt":
        os.startfile(path)
    else:
        subprocess.Popen([path])


def _execute_task(task):
    task_type = task.get("type", "").strip().lower()
    openpath = task.get("openpath", "").strip()
    folderpath = (
        task.get("folderpath")
        or task.get("folder_path")
        or task.get("folder path")
        or ""
    ).strip()

    if not openpath:
        return "No open path is configured for this task."

    if task_type == "web url" or openpath.startswith(("http://", "https://")):
        webbrowser.open(openpath)
        return f"Opened URL: {openpath}"

    if task_type == "desktop application":
        _open_desktop_path(openpath)
        return f"Opened application: {openpath}"

    if task_type == "open folder in vs code":
        target_folder = folderpath or openpath
        subprocess.Popen([openpath, target_folder])
        return f"Opened folder in VS Code: {target_folder}"

    return f"Task matched, but type '{task.get('type')}' is not executable yet."


def _wikipedia_summary(query):
    cleaned = query.lower()
    for phrase in [
        "search with wikipedia",
        "search on wikipedia",
        "search wikipedia",
        "wikipedia search",
        "with wikipedia",
        "wikipedia",
        "search",
    ]:
        cleaned = cleaned.replace(phrase, " ")
    cleaned = " ".join(cleaned.split())
    if not cleaned:
        return "Please include a topic to search on Wikipedia."

    if requests is not None:
        try:
            headers = {
                "User-Agent": "LocalAIStudioTaskAssistant/1.0 (local development; contact: local)"
            }
            search_response = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": cleaned,
                    "srlimit": 1,
                    "format": "json",
                },
                headers=headers,
                timeout=10,
            )
            search_response.raise_for_status()
            search_results = search_response.json().get("query", {}).get("search", [])

            if not search_results:
                return "I could not find a matching Wikipedia page for that topic."

            title = search_results[0]["title"]
            summary_response = requests.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title, safe='')}",
                headers=headers,
                timeout=10,
            )
            summary_response.raise_for_status()
            summary_data = summary_response.json()
            print(summary_data.get("extract"))
            return summary_data.get("extract") or "Wikipedia did not return a summary for that topic."
        except Exception as error:
            package_fallback_error = error
    else:
        package_fallback_error = "requests package is not installed."

    if wikipedia is None:
        return f"Wikipedia lookup failed: {package_fallback_error}"

    try:
        return wikipedia.summary(cleaned, sentences=2)
    except wikipedia.exceptions.DisambiguationError as error:
        option = error.options[0] if error.options else cleaned
        try:
            return wikipedia.summary(option, sentences=2)
        except Exception as nested_error:
            return f"Wikipedia found multiple meanings, but summary lookup failed: {nested_error}"
    except wikipedia.exceptions.PageError:
        return "I could not find a matching Wikipedia page for that topic."
    except Exception as error:
        return f"Wikipedia lookup failed: {package_fallback_error}; package fallback failed: {error}"


def _is_wikipedia_request(text):
    lowered = text.lower()
    return "wikipedia" in lowered or "wiki pedia" in lowered


def run_task_assistant(text):
    start_time = perf_counter()

    if _is_wikipedia_request(text):
        wiki_result = _wikipedia_summary(text)
        elapsed_ms = round((perf_counter() - start_time) * 1000, 2)
        return {
            "message": text,
            "matched_task": {
                "task": "wikipedia search",
                "type": "knowledge lookup",
                "openpath": "",
                "description": "Search Wikipedia and return a short knowledge summary without opening a task application or website.",
            },
            "similarity": 1.0,
            "action_result": "Returned Wikipedia summary.",
            "wikipedia_summary": wiki_result,
            "model": settings.EMBEDDING_MODEL_NAME,
            "generation_time_ms": elapsed_ms,
        }

    user_vector = get_embedding_model().encode([text])[0].tolist()
    tasks = _load_tasks()
    candidates = [task for task in tasks if isinstance(task.get("embedding"), list)]

    if not candidates:
        return {
            "message": text,
            "error": "No task embeddings found. Regenerate tasking.json embeddings first.",
            "generation_time_ms": round((perf_counter() - start_time) * 1000, 2),
        }

    best_task = max(candidates, key=lambda task: _cosine_similarity(user_vector, task["embedding"]))
    score = _cosine_similarity(user_vector, best_task["embedding"])
    action_result = _execute_task(best_task)
    elapsed_ms = round((perf_counter() - start_time) * 1000, 2)

    return {
        "message": text,
        "matched_task": {
            "task": best_task.get("task", ""),
            "type": best_task.get("type", ""),
            "openpath": best_task.get("openpath", ""),
            "description": best_task.get("description", ""),
        },
        "similarity": round(score, 4),
        "action_result": action_result,
        "wikipedia_summary": None,
        "model": settings.EMBEDDING_MODEL_NAME,
        "generation_time_ms": elapsed_ms,
    }


def generate_chat_reply(message):
    tokenizer, model = get_chat_assets()
    start_time = perf_counter()
    inputs = tokenizer(message, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=90,
            do_sample=True,
            temperature=0.85,
            top_p=0.95,
            repetition_penalty=1.15,
            pad_token_id=tokenizer.eos_token_id,
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    reply = decoded[len(message) :].strip() if decoded.startswith(message) else decoded.strip()
    elapsed_ms = round((perf_counter() - start_time) * 1000, 2)

    return {
        "message": message,
        "reply": reply or decoded,
        "model": settings.CHAT_MODEL_LABEL,
        "generation_time_ms": elapsed_ms,
    }
