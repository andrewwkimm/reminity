"""API endpoints for transcript summarization."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from remivity.config import PipelineConfig
from remivity.core.processor import process_pipeline

router = APIRouter()


class YouTubeRequest(BaseModel):
    """Pydantic model for a YouTube request."""

    url: str


@router.post("/summarize/youtube")
def summarize_youtube(data: YouTubeRequest, config: PipelineConfig) -> dict:
    """Handles summarization for a YouTube URL."""
    try:
        result = process_pipeline(
            youtube_url=data.url,
            audio_file_path=None,
            config=config,
        )
        return result
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/summarize/audio")
def summarize_audio(
    audio_file: Annotated[UploadFile, File()], config: PipelineConfig
) -> dict:
    """Handles summarization for an uploaded audio file."""
    try:
        audio_file_name = audio_file.filename or "audio_file"
        tmp_path = Path("scartch/tmp") / audio_file_name
        with tmp_path.open("wb") as f:
            f.write(audio_file.file.read())

        result = process_pipeline(
            youtube_url=None,
            audio_file_path=tmp_path,
            config=config,
        )

        tmp_path.unlink(missing_ok=True)
        return result

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
