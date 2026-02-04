class Sprite:
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.dataType = None
        for key, value in kwargs.items():
            setattr(self, key, value)
    def __repr__(self):
        return f'<Sprite {self.name}>'
    def get(self, value, fallback = None):
        return getattr(self, value, fallback)
    def set(self, value):
        return setattr(self, value)