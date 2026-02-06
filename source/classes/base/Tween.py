import pytweening
import source.variables as v
import source.registry as reg
import typing
import pygame
from source.classes.BaseInstance import BaseInstance

def cusSetAttr(obj, name, value):
    if isinstance(obj, pygame.mixer.Sound) and name == 'volume':
        return obj.set_volume(value)
    return setattr(obj, name, value)

def cusGetAttr(obj, name):
    if isinstance(obj, pygame.mixer.Sound) and name == 'volume':
        return obj.get_volume()
    return getattr(obj, name)

class Tween(BaseInstance):
    tween_types = [
        "linear",
        "easeInQuad", "easeOutQuad", "easeInOutQuad",
        "easeInCubic", "easeOutCubic", "easeInOutCubic",
        "easeInQuart", "easeOutQuart", "easeInOutQuart",
        "easeInQuint", "easeOutQuint", "easeInOutQuint",
        "easeInSine", "easeOutSine", "easeInOutSine",
        "easeInExpo", "easeOutExpo", "easeInOutExpo",
        "easeInCirc", "easeOutCirc", "easeInOutCirc",
        "easeInElastic", "easeOutElastic", "easeInOutElastic",
        "easeInBack", "easeOutBack", "easeInOutBack",
        "easeInBounce", "easeOutBounce", "easeInOutBounce",
        "easeInPoly", "easeOutPoly", "easeInOutPoly"
    ]

    def __init__(self, name: str, obj: object, valueName: str, toValue: float | int, duration: float, tweenType:
    str, onCompleted: typing.Callable[[], None] = lambda: None):
        if not tweenType in self.tween_types:
            raise ValueError(f'{tweenType} is not a valid tween type!')
        if duration <= 0:
            raise ValueError(f'{duration} must be above 0!')

        super().__init__(name or getattr(obj, 'name', 'GenericTween'), 'Tween')
        self.spriteRef = obj
        self.valueName = valueName
        self.baseValue = cusGetAttr(obj, valueName)
        self.toValue = toValue
        self.startTime = v.clock.get_time()/1000 if v.clock is not None else 0
        self.endTime = self.startTime+duration
        self.tweenType = tweenType
        #self.easingType = easingType
        self.onCompleted = onCompleted
        reg.add('Tween', self.name, self)

    def update(self):
        currentTime = v.elapsed
        t = (currentTime - self.startTime) / (self.endTime - self.startTime)
        t = min(max(t, 0), 1)

        start = self.baseValue
        end = self.toValue
        newValue = start + (end - start) * getattr(pytweening, self.tweenType)(t)
        #setattr(self.spriteRef, self.valueName, newValue)
        if isinstance(self.spriteRef, pygame.mixer.Sound):
            cusSetAttr(self.spriteRef, 'volume', newValue)

        if currentTime >= self.endTime and callable(self.onCompleted):
            self.onCompleted()
            reg.remove('Tween', self.name)