import pytweening
import source.variables as v
import source.registry as reg
import typing

class Tween:
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

    def __init__(self, name: str, sprite: 'Sprite', valueName: str, toValue: float | int, duration: float, tweenType:
    str,
                 onCompleted: typing.Callable[[], None] = lambda: None):
        if not tweenType in self.tween_types:
            raise ValueError(f'{tweenType} is not a valid tween type!')
        if duration <= 0:
            raise ValueError(f'{duration} must be above 0!')

        self.name = name or getattr(sprite, 'name', 'GenericTween')
        self.spriteRef = sprite
        self.valueName = valueName
        self.baseValue = getattr(sprite, valueName)
        self.toValue = toValue
        self.startTime = v.clock.get_ticks()
        self.endTime = self.startTime+duration
        self.tweenType = tweenType
        #self.easingType = easingType
        self.onCompleted = onCompleted
        reg.add('Tween', self)

    def update(self):
        currentTime = v.clock.get_ticks()
        t = (currentTime - self.startTime) / (self.endTime - self.startTime)
        t = min(max(t, 0), 1)

        start = self.baseValue
        end = self.toValue
        newValue = start + (end - start) * getattr(pytweening, self.tweenType)(t)
        setattr(self.spriteRef, self.valueName, newValue)

        if currentTime >= self.endTime and self.onCompleted:
            self.onCompleted()
            reg.remove('Tween', self)