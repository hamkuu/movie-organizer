from fasthtml.common import Div, P, fast_app, serve

app, rt = fast_app()


@rt("/")
def get():
    return Div(P("Hello from Movie Organizer!"), hx_get="/change")


serve()
