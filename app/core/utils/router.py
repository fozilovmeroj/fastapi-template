import importlib
import pkgutil
from pathlib import Path

from fastapi import FastAPI, APIRouter

from app.schemas.base import DBModel


def load_routers(
        app: FastAPI, path: Path, base_module: str = "app.api", prefix: str = ""
) -> None:
    """
    Recursively load all FastAPI routers from a given package.
    """
    for finder, name, is_pkg in pkgutil.iter_modules([str(path)]):
        module_name = f"{base_module}.{name}"
        full_path = path / name

        module = importlib.import_module(module_name)
        if hasattr(module, "router"):
            router = getattr(module, "router")
            app.include_router(router, prefix=prefix + f"/{name.split('.')[0]}")
        if is_pkg:
            load_routers(app, full_path, module_name, prefix + f"/{name}")


def crud_routes(router: APIRouter, model: DBModel) -> None:
    # TODO: make crud routes maker
    pass
