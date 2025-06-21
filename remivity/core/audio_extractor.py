"""The YouTube transcript and audio extractor."""

from pathlib import Path
from uuid import uuid4

from yt_dlp import YoutubeDL

from remivity.exceptions import AudioExtractionError


def get_youtube_captions(url: str, output_dir: Path) -> Path | None:
    """Extracts auto-generated subtitles from a YouTube video."""
    output_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "srt",
        "outtmpl": str(output_dir / "%(id)s.%(ext)s"),
        "quiet": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get("id")
    except Exception:
        return None

    subtitle_path = output_dir / f"{video_id}.en.srt"
    return subtitle_path if subtitle_path.exists() else None


def download_youtube_audio(url: str, output_dir: Path) -> Path:
    """Downloads best-quality audio from a YouTube URL."""
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
        raise AudioExtractionError(
            "yt-dlp audio extraction failed.") from error

    matching_files = list(output_dir.glob(f"audio_{unique_id}.*"))
    if not matching_files:
        raise AudioExtractionError("Audio file not found after download.")

    return matching_files[0]
