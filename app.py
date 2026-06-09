from time import perf_counter

from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

app = Flask(__name__)

# Load once at startup so each request only performs embedding generation.
# local_files_only keeps the API offline after the model has been cached once.
model = SentenceTransformer(MODEL_NAME, local_files_only=False)


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def encode_texts(texts):
    start_time = perf_counter()
    embeddings = model.encode(texts)
    elapsed_ms = round((perf_counter() - start_time) * 1000, 2)
    return embeddings.tolist(), elapsed_ms


@app.get("/")
def index():
    return jsonify({"status": "running"})


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "running",
            "model": MODEL_NAME,
            "dimension": EMBEDDING_DIMENSION,
        }
    )


@app.post("/embed")
def embed():
    data = request.get_json(silent=True) or {}
    text = data.get("text")

    if text is None:
        return error_response("Missing required field: text", 400)

    if not isinstance(text, str):
        return error_response("Field 'text' must be a string", 400)

    embeddings, elapsed_ms = encode_texts([text])

    return jsonify(
        {
            "text": text,
            "model": MODEL_NAME,
            "dimension": EMBEDDING_DIMENSION,
            "embedding": embeddings[0],
            "generation_time_ms": elapsed_ms,
        }
    )


@app.post("/embed-batch")
def embed_batch():
    data = request.get_json(silent=True) or {}
    texts = data.get("texts")

    if texts is None:
        return error_response("Missing required field: texts", 400)

    if not isinstance(texts, list):
        return error_response("Field 'texts' must be an array of strings", 400)

    if not all(isinstance(text, str) for text in texts):
        return error_response("All items in 'texts' must be strings", 400)

    if not texts:
        return jsonify(
            {
                "texts": texts,
                "model": MODEL_NAME,
                "dimension": EMBEDDING_DIMENSION,
                "embeddings": [],
                "generation_time_ms": 0,
            }
        )

    embeddings, elapsed_ms = encode_texts(texts)

    return jsonify(
        {
            "texts": texts,
            "model": MODEL_NAME,
            "dimension": EMBEDDING_DIMENSION,
            "embeddings": embeddings,
            "generation_time_ms": elapsed_ms,
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)