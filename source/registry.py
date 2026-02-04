import source.variables as v


def add(dataType, name, value):
    v.registry.setdefault(dataType, {})[name] = value
addRegistry = add

def remove(dataType, name):
    try:
        del v.registry[dataType][name]
    except KeyError:
        raise KeyError(f"{dataType}/{name} does not exist!")
removeRegistry = remove

def update(dataType, name, value):
    #if dataType not in v.registry or name not in v.registry[dataType]:
        #raise KeyError(f"{dataType}/{name} does not exist!")
    if dataType not in v.registry:
        raise KeyError(f"{dataType} does not exist!")
    v.registry[dataType][name] = value
updateRegistry = update

def get(dataType, name):
    if dataType not in v.registry or name not in v.registry[dataType]:
        raise KeyError(f"{dataType}/{name} does not exist!")
    return v.registry[dataType][name]
getRegistry = get