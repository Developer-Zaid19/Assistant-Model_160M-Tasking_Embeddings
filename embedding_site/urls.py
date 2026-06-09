from django.urls import path

from assistant_app import views


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("api/health/", views.health_api, name="health_api"),
    path("api/chat/", views.chat_api, name="chat_api"),
    path("api/embed/", views.embed_api, name="embed_api"),
    path("api/task/", views.task_api, name="task_api"),
]
