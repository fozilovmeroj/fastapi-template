import sys
from types import ModuleType

from app.core.utils.alembic import import_all_models


def test_import_all_models(tmp_path, monkeypatch):
    # Setup: create a fake Python package
    pkg = tmp_path / "mypkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")

    # Create modules
    (pkg / "mod1.py").write_text("x = 1")
    (pkg / "mod2.py").write_text("y = 2")

    # Create nested module
    nested = pkg / "sub"
    nested.mkdir()
    (nested / "__init__.py").write_text("")
    (nested / "mod3.py").write_text("z = 3")

    # Add tmp path to sys.path for import resolution
    monkeypatch.syspath_prepend(str(tmp_path))

    # Run the import function
    import_all_models("mypkg", str(pkg))

    # Check that modules were imported
    assert isinstance(sys.modules.get("mypkg.mod1"), ModuleType)
    assert isinstance(sys.modules.get("mypkg.mod2"), ModuleType)
    assert isinstance(sys.modules.get("mypkg.sub.mod3"), ModuleType)

    # __init__ files should not be imported as modules
    assert "mypkg.__init__" not in sys.modules
    assert "mypkg.sub.__init__" not in sys.modules
