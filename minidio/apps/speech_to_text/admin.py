from django.contrib import admin

from .models import AudioFile, Conversation, Message

admin.site.register(AudioFile)
admin.site.register(Conversation)
admin.site.register(Message)
