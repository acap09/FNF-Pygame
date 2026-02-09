# Inspired by: https://create.roblox.com/docs/reference/engine/datatypes/RBXScriptSignal
# Makes hooking events easier
import typing as t
import warnings

class ScriptSignal:
    def __init__(self):
        self.listeners = {}

    def connect(self, listener: t.Callable[..., None]):
        if not callable(listener):
            raise TypeError(f'Provided listener must be callable!')
        name = listener.__name__
        if name in self.listeners:
            warnings.warn(f'Listener {name} already exists and therefore is being replaced!')
        self.listeners[name] = listener

    def disconnect(self, name: str):
        if name in self.listeners:
            self.listeners.pop(name)
            return
        raise KeyError(f'Listener {name} does not exist!')

    def fire(self, *args, **kwargs):
        for listener in self.listeners.values():
            listener(*args, **kwargs)