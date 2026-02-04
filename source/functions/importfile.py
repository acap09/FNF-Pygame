import importlib
from pathlib import Path

def importModule(path: str, custom_name: str = None):
    filePath = Path(path)
    if custom_name is None:
        custom_name = filePath.stem

    spec = importlib.util.spec_from_file_location(custom_name, filePath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod