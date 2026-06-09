import json

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .model_services import generate_chat_reply, generate_embedding, run_task_assistant


def _json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return None


@require_GET
def home(request):
    return render(
        request,
        "assistant_app/home.html",
        {
            "embedding_model": settings.EMBEDDING_MODEL_NAME,
            "chat_model": settings.CHAT_MODEL_LABEL,
            "dimension": settings.EMBEDDING_DIMENSION,
        },
    )


@require_GET
def about(request):
    return render(
        request,
        "assistant_app/about.html",
        {
            "embedding_model": settings.EMBEDDING_MODEL_NAME,
            "chat_model": settings.CHAT_MODEL_LABEL,
            "dimension": settings.EMBEDDING_DIMENSION,
        },
    )


@require_GET
def contact(request):
    return render(request, "assistant_app/contact.html")


@require_GET
def health_api(request):
    return JsonResponse(
        {
            "status": "running",
            "embedding_model": settings.EMBEDDING_MODEL_NAME,
            "chat_model": settings.CHAT_MODEL_LABEL,
            "dimension": settings.EMBEDDING_DIMENSION,
        }
    )


@require_POST
def chat_api(request):
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    message = data.get("message", "")
    if not isinstance(message, str):
        return JsonResponse({"error": "Field 'message' must be a string"}, status=400)

    message = message.strip()
    if not message:
        return JsonResponse({"error": "Please enter a message"}, status=400)

    return JsonResponse(generate_chat_reply(message))


@csrf_exempt
@require_POST
def embed_api(request):
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    text = data.get("text", "")
    if not isinstance(text, str):
        return JsonResponse({"error": "Field 'text' must be a string"}, status=400)

    text = text.strip()
    if not text:
        return JsonResponse({"error": "Please enter text to embed"}, status=400)

    return JsonResponse(generate_embedding(text))


@csrf_exempt
@require_POST
def task_api(request):
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    text = data.get("text", "")
    if not isinstance(text, str):
        return JsonResponse({"error": "Field 'text' must be a string"}, status=400)

    text = text.strip()
    if not text:
        return JsonResponse({"error": "Please enter a task"}, status=400)

    result = run_task_assistant(text)
    status = 500 if result.get("error") else 200
    return JsonResponse(result, status=status)
