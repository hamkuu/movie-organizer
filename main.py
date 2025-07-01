from pathlib import Path

from fasthtml.common import (
    H3,
    Button,
    Div,
    Form,
    Input,
    Label,
    Li,
    P,
    Titled,
    Ul,
    fast_app,
    serve,
)

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
        folders = [p for p in directory.iterdir() if p.is_dir()]
        folders.sort()

        # Create the folder list
        folder_items = [Li(f"{folder}") for folder in folders]

        return Div(
            H3(f"Folders in: {directory}"), P(f"Found {len(folders)} folder(s)"), Ul(*folder_items), cls="container"
        )

    except Exception as e:
        return Div(P(f"Error: {str(e)}"), cls="container")


serve()
