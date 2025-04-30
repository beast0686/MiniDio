from pathlib import Path
from itertools import groupby
from typing import NamedTuple

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1.types import WordInfo
from google import genai
from google.genai import types

DIARIZATION_CONFIG = speech.SpeakerDiarizationConfig(
    enable_speaker_diarization=True,
    min_speaker_count=1,
    max_speaker_count=10,
)


class SentenceInfo(NamedTuple):
    speaker_tag: int
    sentence: str


genai_client = genai.Client()


def generate_transcript(
    audio_file: Path, language_code: str = "en-US"
) -> list[WordInfo]:
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_file.read_bytes())

    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language_code,
        diarization_config=DIARIZATION_CONFIG,
    )

    response = client.long_running_recognize(
        config=recognition_config, audio=audio
    ).result(timeout=300)

    assert response is not None, "Transcript could not be generated from audio file!"

    result, *_ = response.results
    words_info = result.alternatives[0].words
    return words_info


def group_speaker_words(words_info: list[WordInfo]) -> list[SentenceInfo]:
    speaker_words = ((word.speaker_tag, word.word) for word in words_info)

    return [
        SentenceInfo(
            speaker_tag=speaker_tag, sentence=" ".join(word for _, word in words)
        )
        for speaker_tag, words in groupby(speaker_words, key=lambda w: w[0])
    ]


def generate_minutes(sentences: list[SentenceInfo]) -> str:
    transcript = "\n".join(
        f"Speaker {speaker_tag}: {sentence}" for speaker_tag, sentence in sentences
    )

    contents = [
        types.ModelContent(
            [
                types.Part.from_text(
                    text="Generate minutes of the meeting from the following transcript. "
                    "You may format the response in markdown format."
                ),
            ]
        ),
        types.UserContent([types.Part.from_text(text="Transcript\n\n" + transcript)]),
    ]


    response = genai_client.models.generate_content(
        model="gemini-2.0-flash-001", contents=contents
    )

    return response.text or ""


def main() -> None:
    audio_file = Path("/home/ryuga/Downloads/sample_audio.wav")
    transcript = generate_transcript(audio_file)
    sentences = group_speaker_words(transcript)
    minutes = generate_minutes(sentences)

    print(minutes)


if __name__ == "__main__":
    main()
