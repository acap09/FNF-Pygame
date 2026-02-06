import importlib.util
from pathlib import Path
import xmltodict as xtd
import json
#print(importlib.__file__)

def getPathIfExists(path: str):
    filePath = Path(path)
    if filePath.exists():
        return filePath
    return None
gpie = getPathIfExists
def sensitiveGetPathIfExists(path: str):
    filePath = getPathIfExists(path)
    if filePath is None:
        raise FileNotFoundError(f'File {path} not found')
    return filePath
sgpie = sensitiveGetPathIfExists

def importModule(path: str, custom_name: str = None):
    filePath = Path(path)
    if custom_name is None:
        custom_name = filePath.stem
    if not filePath.exists():
        raise FileNotFoundError(f'{filePath} does not exist!')

    spec = importlib.util.spec_from_file_location(custom_name, filePath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def readFile(path: str, keep_open = False):
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

def parseTxt(path: str):
    filePath = gpie(path)
    content = readFile(path)[0]
    if filePath.suffix == '.xml':
        content = xtd.parse(content)
    elif filePath.suffix == '.json':
        content = json.loads(content)
    else:
        print(f'{path} is not .xml or .json, so content is not parsed.')
        return None
    return content