from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .forms import AudioFileUploadForm
from .models import AudioFile, Conversation, Message
from .llm_utils import generate_minutes, generate_transcript, group_speaker_words


def landing(requests: HttpRequest) -> HttpResponse:
    return render(requests, "landing.html")


@method_decorator(login_required, name="dispatch")
class AudioFileView(FormView):
    form_class = AudioFileUploadForm
    template_name = "upload.html"
    success_url = "/upload/"

    def form_valid(self, form: AudioFileUploadForm) -> HttpResponse:
        """Upload an audio file and display the generated minutes."""
        audio_file = form.save(commit=False)
        audio_file.created_by = self.request.user
        audio_file.save()

        minutes = self._generated_minutes(audio_file)

        context = self.get_context_data(form=form, minutes=minutes)

        assert self.template_name is not None
        return TemplateResponse(self.request, self.template_name, context)

    def _generated_minutes(self, audio_file: AudioFile) -> str:
        audio_file_path = Path(str(audio_file.audio_file.file))
        transcript = generate_transcript(audio_file=audio_file_path)
        sentences = group_speaker_words(transcript)
        return generate_minutes(sentences)


@method_decorator(login_required, name="dispatch")
class ConversationListView(ListView):
    model = Conversation

    def get_queryset(self) -> QuerySet[Conversation]:
        return Conversation.objects.filter(audio_file__created_by=self.request.user)


@method_decorator(login_required, name="dispatch")
class MessageListView(ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conversation"] = Conversation.objects.get(pk=self.kwargs["pk"])
        return context

    def get_queryset(self) -> QuerySet[Message]:
        context = self.get_context_data()
        conversation = context["conversation"]

        assert conversation.audio_file.created_by == self.request.user
        return Message.objects.filter(conversation=conversation)


@method_decorator(login_required, name="dispatch")
class SendMessageView(View):
    template_name = "chatbot.html"

    def post(self, request: HttpRequest, conversation_id: int) -> HttpResponse:
        """Create a new conversation"""

        conversation = get_object_or_404(Conversation, pk=conversation_id)
        user_input = request.POST.get("message", "").strip()
        if not user_input:
            return JsonResponse({"error": "Empty message"}, status=400)

        Message.objects.create(
            conversation=conversation,
            sender="user",
            message=user_input,
        )

        llm_response = self._generate_llm_response(user_input, conversation)
        Message.objects.create(
            conversation=conversation,
            sender="assistant",
            message=llm_response,
        )

        return JsonResponse({"assistant_message": llm_response})

    def _generate_llm_response(self, message: str, conversation: Conversation):
        return "Placeholder"
