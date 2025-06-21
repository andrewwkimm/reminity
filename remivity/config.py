"""The Remivity configurations."""

from llama_index.core.llms import LLM
from pydantic import BaseModel


class PipelineConfig(BaseModel):
    """Configuration for the pipeline process."""

    whisper_model: str
    whisper_device: str
    whisper_compute_type: str
    llm: LLM


class SummaryConfig(BaseModel):
    """Configuration for summarization."""

    max_length: int = 300
    chunk_size: int = 1000
    chunk_overlap: int = 100
    temperature: float = 0.3
    model_name: str = "mistral"
    ollama_url: str = "http://localhost:11434"


class SummaryResult(BaseModel):
    """Configuration for the summarization result."""

    summary: str
    word_count: int
    chunk_count: int
    original_length: int
