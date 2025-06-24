"""Runner for full video summary pipeline using Ollama LLM."""

from pathlib import Path

from llama_index.llms.ollama import Ollama

from remivity.config import PipelineConfig
from remivity.core.processor import process_pipeline

OLLAMA_MODEL = "mistral:7b-instruct-q4_0"

YOUTUBE_URL: str | None = "https://www.youtube.com/watch?v=XEWBixfnbb4"
AUDIO_FILE_PATH: Path | None = None

llm = Ollama(
    model=OLLAMA_MODEL,
    request_timeout=500.0,
    json_mode=False,
)

config = PipelineConfig(model="large-v2")

if __name__ == "__main__":
    result = process_pipeline(
        youtube_url=YOUTUBE_URL,
        audio_file_path=AUDIO_FILE_PATH,
        config=config,
    )

    print("\n=== TRANSCRIPT ===\n")
    print(result["transcript"][:1000])

    print("\n=== SUMMARY ===\n")
    print(result["summary"])
