from pathlib import Path

from fasthtml.common import (
    Button,
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
from starlette.requests import Request


def not_found(req: Request, exc):
    return Titled(f"404: URL {req.url} is not found.")


exception_handlers = {404: not_found}

app, rt = fast_app(exception_handlers=exception_handlers)


def get_default_path():
    return str(Path.home() / "Downloads" / "Movies")


@rt
def index():
    return Titled(
        "Movie Organizer",
        Form(
            Label("Target Path:"),
            Input(name="path", value=get_default_path()),
            Button("List Folders", type="submit"),
            hx_get="/list-folders",
            hx_target="#folder-list",
        ),
        P(id="folder-list"),
    )


@rt("/list-folders")
def list_folders(path: Path):
    if path.is_dir():
        return Section(map(Ul, path.iterdir()))
    else:
        return Section(P(f"{path} is not a directory."))


serve()
