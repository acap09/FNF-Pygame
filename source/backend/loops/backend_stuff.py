import source.registry as reg
import source.variables as v

def update():
    for dataType, objects in v.registry.items():
        for name, obj in objects.copy().items():
            if hasattr(obj, 'update') and callable(obj.update):
                obj.update()