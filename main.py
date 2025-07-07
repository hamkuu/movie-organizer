from pathlib import Path

from fasthtml import common as fh
from starlette.requests import Request


def not_found(req: Request, exc):
    return fh.Titled(f"404: URL {req.url} is not found.")


exception_handlers = {404: not_found}

app, rt = fh.fast_app(exception_handlers=exception_handlers)


def get_default_path():
    return str(Path.home() / "Downloads" / "Movies")


@rt
def index():
    return fh.Titled(
        "Movie Organizer",
        fh.Form(
            fh.Label("Target Path:"),
            fh.Input(name="path", value=get_default_path()),
            fh.Button("List Folders", type="submit"),
            hx_get="/list-folders",
            hx_target="#folder-list",
        ),
        fh.P(id="folder-list"),
    )


@rt("/list-folders")
def list_folders(path: Path):
    if path.is_dir():
        return fh.Section(map(fh.Ul, path.iterdir()))
    else:
        return fh.Section(fh.P(f"{path} is not a directory."))


fh.serve()
