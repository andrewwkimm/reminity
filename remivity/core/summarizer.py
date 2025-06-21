"""The transcript summarizer."""

from llama_index.core.llms import LLM

from remivity.exceptions import SummarizationError


def summarize_text(text: str, llm: LLM) -> str:
    """Summarizes a transcript using a local LLM."""
    if not text.strip():
        raise SummarizationError("Input text is empty.")

    prompt = (
        """Summarize the following transcript clearly and concisely:

        Rules:
            - Focus on the main topics and key points
            - Organize information logically. Make sure you include timestamps.
            - Include important details, names, or numbers mentioned
            - Don't add information not in the transcript

        f"{text}\n\n

        Summary:
        """
    )

    try:
        response = llm.complete(prompt=prompt)
        return response.text.strip()
    except Exception as e:
        raise SummarizationError("Failed to summarize transcript.") from e
