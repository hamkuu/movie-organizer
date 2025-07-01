from pathlib import Path

from fasthtml.common import (
    Button,
    Div,
    Form,
    Input,
    Label,
    P,
    Titled,
    Ul,
    fast_app,
    serve,
)
from fasthtml.components import Section

app, rt = fast_app()


def get_default_path():
    """Get the default Downloads directory path for the current user"""
    return str(Path.home() / "Downloads" / "Movies")


@rt
def index():
    return Titled(
        "Movie Organizer",
        Form(
            Div(
                Label("Target Directory:", _for="directory"),
                Input(
                    type="text",
                    name="directory",
                    id="directory",
                    value=get_default_path(),
                    placeholder="Enter directory path...",
                ),
                Button("List Folders", type="submit"),
                cls="container",
            ),
            hx_get="/list-folders",
            hx_target="#folder-results",
            hx_swap="innerHTML",
        ),
        Div(id="folder-results"),
    )


@rt("/list-folders")
def list_folders(directory: Path):
    try:
        return Section(map(Ul, directory.iterdir()))
    except Exception as e:
        return Section(P(f"Error: {str(e)}"))


serve()
