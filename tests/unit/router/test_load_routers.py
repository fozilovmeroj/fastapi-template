import shutil
import tempfile
import textwrap
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.utils.router import load_routers


def create_router_file(path: Path, name: str, route_path: str, response: str):
    file_path = path / f"{name}.py"
    file_path.write_text(
        textwrap.dedent(
            f"""
        from fastapi import APIRouter

        router = APIRouter()

        @router.get("/")
        def route():
            return {response}
    """
        )
    )
    return file_path


def test_load_routers():
    temp_dir = tempfile.mkdtemp()
    api_path = Path(temp_dir) / "api"
    api_path.mkdir(parents=True)

    # Simulate a module package
    (api_path / "__init__.py").touch()

    # Create router modules
    create_router_file(api_path, "users", "/", '[{"name": "John"}]')
    admin_path = api_path / "admin"
    admin_path.mkdir()
    (admin_path / "__init__.py").touch()
    create_router_file(admin_path, "dashboard", "/", '{"admin": True}')

    # Add temp_dir to sys.path for dynamic import
    import sys

    sys.path.insert(0, temp_dir)

    # Create FastAPI app and load routers
    app = FastAPI()
    load_routers(app, api_path, base_module="api", prefix="")

    client = TestClient(app)

    # Test if endpoints were mounted correctly
    users_resp = client.get("/users/")
    assert users_resp.status_code == 200
    assert users_resp.json() == [{"name": "John"}]

    dashboard_resp = client.get("/admin/dashboard/")
    assert dashboard_resp.status_code == 200
    assert dashboard_resp.json() == {"admin": True}

    # Cleanup
    shutil.rmtree(temp_dir)
    sys.path.pop(0)
