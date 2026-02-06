import importlib.util
from pathlib import Path
import xmltodict as xtd
import json
#print(importlib.__file__)

def get_path_if_exists(path: str):
    filePath = Path(path)
    if filePath.exists():
        return filePath
    return None
gpie = get_path_if_exists
def sensitive_get_path_if_exists(path: str):
    filePath = get_path_if_exists(path)
    if filePath is None:
        raise FileNotFoundError(f'File {path} not found')
    return filePath
sgpie = sensitive_get_path_if_exists

def import_module(path: str, custom_name: str = None):
    filePath = Path(path)
    if custom_name is None:
        custom_name = filePath.stem
    if not filePath.exists():
        raise FileNotFoundError(f'{filePath} does not exist!')

    spec = importlib.util.spec_from_file_location(custom_name, filePath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
importModule = import_module #backwards compatibility

def read_file(path: str, keep_open = False):
    filePath = sgpie(path)
    file = open(filePath, 'r', encoding='utf-8')
    try:
        content = file.read()
        if keep_open:
            return content, file
    finally:
        if not keep_open:
            file.close()
    return content, None
readFile = read_file

def parse_txt(path: str):
    filePath = gpie(path)
    content = read_file(path)[0]
    if filePath.suffix == '.xml':
        content = xtd.parse(content)
    elif filePath.suffix == '.json':
        content = json.loads(content)
    else:
        print(f'{path} is not .xml or .json, so content is not parsed.')
        return None
    return content
parseTxt = parse_txt