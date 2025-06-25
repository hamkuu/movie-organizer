from pathlib import Path

from fasthtml.common import Div, P, fast_app, serve

app, rt = fast_app()


@rt("/")
def get():
    return Div(P("Hello from Movie Organizer!"), hx_get="/change")


@rt("/folders/{folder_path:path}")
def get_folders(folder_path: Path):
    return Div(*[P(item) for item in folder_path.iterdir()])


serve()
