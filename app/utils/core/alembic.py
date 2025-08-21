import importlib
import pathlib


def import_all_models(package_name: str, package_path: str) -> None:
    """
    Recursively import all Python modules in a given package.
    """
    for path in pathlib.Path(package_path).rglob("*.py"):
        module_path = path.with_suffix("").relative_to(package_path)
        module_str = ".".join((package_name,) + module_path.parts)
        importlib.import_module(module_str)
