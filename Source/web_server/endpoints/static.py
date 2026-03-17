import mimetypes
from pathlib import Path

from web_server._logic import server_path, web_server_handler


STATIC_DIR = (Path(__file__).resolve().parent.parent / "static").resolve()


def _serve_static(self: web_server_handler, requested_path: str) -> bool:
    # Prevent path traversal: requested file must stay under web_server/static.
    safe_relative = Path(requested_path.lstrip("/\\"))
    full_path = (STATIC_DIR / safe_relative).resolve()
    if STATIC_DIR not in full_path.parents and full_path != STATIC_DIR:
        self.send_error(403)
        return True

    if not full_path.is_file():
        self.send_error(404)
        return True

    with full_path.open("rb") as fp:
        content = fp.read()

    content_type = mimetypes.guess_type(str(full_path))[0] or "application/octet-stream"
    self.send_data(content, content_type=content_type)
    return True


@server_path(r"/static/(.+)", regex=True, commands={"GET", "HEAD"})
def _(self: web_server_handler, match) -> bool:
    return _serve_static(self, match.group(1))


@server_path(r"/static/img/(.+)", regex=True, commands={"GET", "HEAD"})
def __(self: web_server_handler, match) -> bool:
    # Backward compatibility for old redirects to /static/img/<file>.
    return _serve_static(self, match.group(1))
