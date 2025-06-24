"""The transcript summarizer."""

from llama_index.core.llms import LLM

from remivity.exceptions import SummarizationError


def summarize_text(text: str, llm: LLM) -> str:
    """Summarizes a transcript using a local LLM."""
    if not text.strip():
        raise SummarizationError("Input text is empty.")

    prompt = f"""You are summarizing a video transcript which may have timestamps.
If so, create a summary that ALWAYS includes timestamps for key points.

IMPORTANT: Every major point in your summary MUST reference a timestamp from the
transcript.

FORMAT YOUR RESPONSE LIKE THIS:
• [00:01:23] Main topic or key point discussed
• [00:05:45] Another important point or transition
• [00:12:30] Conclusion or final thoughts

RULES:
- Extract the most important topics and ideas
- ALWAYS include the timestamp [HH:MM:SS] before each point
- Use the exact timestamps from the transcript
- Focus on substantive content, not filler words
- Organize chronologically by timestamp
- If multiple related points happen close together, you can group them togehter

TRANSCRIPT:
{text}

TIMESTAMP SUMMARY:
"""

    try:
        response = llm.complete(prompt=prompt)
        return response.text.strip()
    except Exception as error:
        raise SummarizationError("Failed to summarize transcript.") from error
