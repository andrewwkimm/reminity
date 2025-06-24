"""The audio file transcriber."""

from pathlib import Path

from faster_whisper import WhisperModel


def transcribe_audio(
    audio_file: str | Path,
    compute_type: str,
    device: str,
    whisper_model: str,
) -> str:
    """Transcribes an audio file to text."""
    loaded_model = WhisperModel(
        model_size_or_path=whisper_model, device=device, compute_type=compute_type
    )

    segments, _ = loaded_model.transcribe(str(audio_file))

    transcript = " ".join(segment.text.strip() for segment in segments)
    return transcript
