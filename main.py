from pathlib import Path

from fasthtml.common import Div, P, fast_app, serve

app, rt = fast_app()


@rt("/")
def get():
    return Div(P("Hello from Movie Organizer!"), hx_get="/change")


@rt("/folders/{folder_dir:path}")
def get_folders(folder_dir: Path):
    if not folder_dir.exists():
        return Div(P(f"Invalid {folder_dir=}: folder does not exist"))
    if not folder_dir.is_dir():
        return Div(P(f"Invalid {folder_dir=}: folder is not a directory"))
    return Div(*[P(item) for item in folder_dir.iterdir()])


serve()
