"""Runs the full pipeline from audio to summary."""

from pathlib import Path

from remivity.config import PipelineConfig
from remivity.core.audio_extractor import (
    download_youtube_audio,
    get_youtube_captions,
)
from remivity.core.summarizer import summarize_text
from remivity.core.transcriber import transcribe_audio
from remivity.exceptions import ProcessingError


def process_pipeline(
    youtube_url: str | None,
    audio_file_path: Path | str | None,
    config: PipelineConfig,
) -> dict:
    """Runs the full pipeline: audio → transcript → summary."""
    audio_path: Path | None = None
    delete_after = False

    try:
        if youtube_url:
            subtitle_path = get_youtube_captions(
                youtube_url, output_dir=Path("scratch/tmp"))

            if subtitle_path:
                transcript = subtitle_path.read_text(encoding="utf-8")
            else:
                audio_path = download_youtube_audio(
                    youtube_url, output_dir=Path("scratch/tmp"))
                delete_after = True
                transcript = transcribe_audio(
                    audio_file=audio_path,
                    compute_type=config.compute_type,
                    device=config.device,
                    model=config.model,
                )

        elif audio_file_path:
            audio_path = Path(audio_file_path)
            transcript = transcribe_audio(
                audio_file=audio_path,
                compute_type=config.compute_type,
                device=config.device,
                model=config.model,
            )

        else:
            raise ProcessingError(
                "A YouTube URL or an audio file must be provided.")

        summary = summarize_text(transcript, config.llm)

        return {
            "transcript": transcript,
            "summary": summary,
        }

    except Exception as error:
        raise ProcessingError("Pipeline execution failed.") from error

    finally:
        if delete_after and audio_path and audio_path.exists():
            audio_path.unlink(missing_ok=True)
