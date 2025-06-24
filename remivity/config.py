"""The Remivity configurations."""

from typing import Literal

from llama_index.core.llms import LLM
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel


class PipelineConfig(BaseModel):
    """Configuration for the pipeline process."""

    model: str = "mistral"
    device: str = "auto"
    compute_type: str = "default"
    llm_provider: Literal["ollama", "chatgpt", "claude"] = "ollama"
    llm_api_key: str | None = None

    def build_llm(self) -> LLM:
        """Constructs the appropriate LLM client."""
        if self.llm_provider == "ollama":
            return Ollama(
                model=self.model,
                request_timeout=120.0,
                json_mode=False,
            )
        elif self.llm_provider == "chatgpt":
            return OpenAI(
                api_key=self.llm_api_key,
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
            )
        elif self.llm_provider == "claude":
            return Anthropic(
                api_key=self.llm_api_key,
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
            )
        raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")


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
