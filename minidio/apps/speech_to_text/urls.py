from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("upload/", views.AudioFileView.as_view(), name="upload"),
    path(
        "conversation/list/", views.ConversationListView.as_view(), name="conversations"
    ),
    path("message/list/", views.MessageListView.as_view(), name="messages"),
    path("message/send", views.SendMessageView.as_view(), name="send_message"),
    path("", views.landing, name="chatbot"),
]
