"""Exceptions for Remivity."""


class AudioExtractionError(Exception):
    """Audio extraction error."""


class ProcessingError(Exception):
    """Pipeline processing error."""


class SummarizationError(Exception):
    """Text summarization error."""


class YouTubeCaptionExtractionError(Exception):
    """YouTube caption extraction error."""
