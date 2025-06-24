"""Gradio interface for Remivity transcript summarization."""

import gradio as gr
from gradio import themes
from gradio.components.file import File
from gradio.components.textbox import Textbox

from remivity.config import PipelineConfig
from remivity.core.processor import process_pipeline

CONFIG = PipelineConfig()


def process_input(
    youtube_url: str | None, audio_file_path: str | None
) -> tuple[str, str]:
    """Process either YouTube URL or audio file and return transcript and summary."""
    result = process_pipeline(
        youtube_url=youtube_url,
        audio_file_path=audio_file_path,
        config=CONFIG,
    )
    return result["transcript"], result["summary"]


def create_tab_content(input_component: File | Textbox) -> tuple:
    """Create consistent tab content with input, button, and outputs."""
    button = gr.Button("Summarize", variant="primary")
    summary = gr.Textbox(label="Summary", lines=5, max_lines=15)

    with gr.Column():
        gr.HTML('<div class="transcript-label">Transcript</div>')
        with gr.Accordion("", open=False):
            transcript = gr.Textbox(label="", lines=10, max_lines=20, container=False)

    return input_component, button, summary, transcript


def setup_tab_events(
    button: gr.Button,
    input_component: File | Textbox,
    outputs: list[Textbox],
    is_file_tab: bool = False,
) -> None:
    """Setup click events for tabs."""
    if is_file_tab:
        button.click(
            lambda file: process_input(youtube_url=None, audio_file_path=file),
            inputs=[input_component],
            outputs=outputs,
        )
    else:
        button.click(
            lambda url: process_input(youtube_url=url, audio_file_path=None),
            inputs=[input_component],
            outputs=outputs,
        )


with gr.Blocks(
    title="Remivity",
    theme=themes.Soft(),
    css="""
        .gradio-container {max-width: 900px; margin: auto;}
        .footer-text {text-align: center;}
        .custom-header {
            text-align: center;
            font-size: 2.2em;
            font-weight: 700;
            margin-bottom: 0.25em;
        }
        .transcript-label {
            font-weight: bold;
            font-size: 1.1em;
            color: #6366f1;
            margin-bottom: 0.5em;
        }
    """,
) as app:
    gr.HTML('<div class="custom-header">Remivity</div>')
    gr.Markdown(
        """
        <h3 style="display: inline-block; padding-left: 120px; padding-right: 120px;">
            Paste in a YouTube URL or a file from your local machine to get started.
        </h3>
        """
    )

    with gr.Tab("🎬 YouTube URL") as youtube_tab:
        url_input, url_button, url_summary, url_transcript = create_tab_content(
            gr.Textbox(
                label="YouTube Video URL",
                placeholder="https://www.youtube.com/watch?v=...",
                scale=4,
            ),
        )

    with gr.Tab("📁 Upload file") as file_tab:
        file_input, file_button, file_summary, file_transcript = create_tab_content(
            gr.File(
                label="File",
                file_types=[".mp3", ".wav", ".m4a", ".flac"],
                type="filepath",
            ),
        )

    setup_tab_events(url_button, url_input, [url_transcript, url_summary])
    setup_tab_events(
        file_button, file_input, [file_transcript, file_summary], is_file_tab=True
    )

    gr.HTML('<div class="footer-text">Remivity</div>')


if __name__ == "__main__":
    app.launch(
        server_port=7860,
        server_name="0.0.0.0",
        share=False,
        show_error=True,
    )
