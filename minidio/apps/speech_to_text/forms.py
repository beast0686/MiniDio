from django import forms

from .models import AudioFile, Conversation, Message


class AudioFileUploadForm(forms.ModelForm):
    LANGUAGE_CHOICES = [
        ("en-US", "English"),
        ("hi-IN", "Hindi"),
        ("kn-IN", "Kannada"),
        ("ta-IN", "Tamil"),
        ("te-IN", "Telugu"),
        ("ml-IN", "Malayalam"),
        ("other", "Other"),
    ]

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = AudioFile
        fields = ["audio_file", "language"]
