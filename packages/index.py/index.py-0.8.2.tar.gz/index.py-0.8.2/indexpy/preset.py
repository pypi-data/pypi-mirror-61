"""
Load some preset functions into Index
"""
import os
from typing import Optional

from starlette.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from .config import config
from .autoreload import MonitorFile
from .applications import Index

app = Index()

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(config.path, "static"), check_dir=False),
    "asgi",
)

if config.FORCE_SSL:
    app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.ALLOWED_HOSTS)


monitor: Optional[MonitorFile] = None


@app.on_event("startup")
def check_on_startup() -> None:
    # monitor file event
    global monitor
    monitor = MonitorFile(config.path)


@app.on_event("shutdown")
def clear_check_on_shutdown() -> None:
    global monitor
    if monitor is not None:
        monitor.stop()


@app.on_event("startup")
def create_directories() -> None:
    """
    create directories for static & template
    """
    os.makedirs(os.path.join(config.path, "views"), exist_ok=True)
    os.makedirs(os.path.join(config.path, "static"), exist_ok=True)
    os.makedirs(os.path.join(config.path, "templates"), exist_ok=True)


@app.on_event("shutdown")
def clear_directories() -> None:
    """
    if no files exist in the directory, delete them
    """

    def rmdir(dirpath: str) -> None:
        try:
            os.rmdir(dirpath)
        except OSError:
            pass

    rmdir(os.path.join(config.path, "views"))
    rmdir(os.path.join(config.path, "static"))
    rmdir(os.path.join(config.path, "templates"))
