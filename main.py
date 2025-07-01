import os
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


@rt("/")
def get():
    """Home page with directory listing feature"""
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
    """List all folders in the specified directory"""
    try:
        # Expand a user path if it contains ~
        directory = os.path.expanduser(directory)

        # Check if a directory exists
        if not os.path.exists(directory):
            return Div(P(f"❌ Directory not found: {directory}"), cls="container")

        # Check if it's actually a directory
        if not os.path.isdir(directory):
            return Div(P(f"❌ Path is not a directory: {directory}"), cls="container")

        # Get all folders in the directory
        try:
            items = os.listdir(directory)
            folders = [item for item in items if os.path.isdir(os.path.join(directory, item))]
            folders.sort()  # Sort alphabetically
        except PermissionError:
            return Div(P(f"❌ Permission denied: Cannot access {directory}"), cls="container")

        if not folders:
            return Div(P(f"📁 No folders found in: {directory}"), cls="container")

        # Create the folder list
        folder_items = [Li(f"📁 {folder}") for folder in folders]

        return Div(
            H3(f"Folders in: {directory}"), P(f"Found {len(folders)} folder(s)"), Ul(*folder_items), cls="container"
        )

    except Exception as e:
        return Div(P(f"❌ Error: {str(e)}"), cls="container")


if __name__ == "__main__":
    serve()
