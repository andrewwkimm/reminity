"""The YouTube URL audio extractor."""

from pathlib import Path
from uuid import uuid4

from yt_dlp import YoutubeDL

from remivity.exceptions import AudioExtractionError


def extract_audio_from_youtube(url: str, output_dir: Path | None = None) -> Path:
    """Extracts audio from a YouTube URL and saves it to the tmp/ directory."""
    if output_dir is None:
        output_dir = Path("scratch/tmp")

    output_dir.mkdir(parents=True, exist_ok=True)
    unique_id = uuid4().hex
    output_template = str(output_dir / f"audio_{unique_id}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as error:
        raise AudioExtractionError("yt-dlp extraction failed") from error

    matching_files = list(output_dir.glob(f"audio_{unique_id}.*"))
    if not matching_files:
        raise AudioExtractionError("Audio file not found after download.")

    return matching_files[0]
