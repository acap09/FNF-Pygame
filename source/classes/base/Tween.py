import pytweening
import source.variables as v
import source.registry as reg
import typing
import pygame
from source.classes.BaseInstance import BaseInstance

def cusSetAttr(obj, name, value):
    if isinstance(obj, pygame.mixer.Sound) and name == 'volume':
        return obj.set_volume(value)
    elif isinstance(obj, pygame.Surface) and name == 'alpha':
        return obj.set_alpha(value)
    return setattr(obj, name, value)

def cusGetAttr(obj, name):
    if isinstance(obj, pygame.mixer.Sound) and name == 'volume':
        return obj.get_volume()
    elif isinstance(obj, pygame.Surface) and name == 'alpha':
        return obj.get_alpha()
    return getattr(obj, name)

class Tween(BaseInstance):
    tween_types = [
        'linear',
        'easeInQuad', 'easeOutQuad', 'easeInOutQuad',
        'easeInCubic', 'easeOutCubic', 'easeInOutCubic',
        'easeInQuart', 'easeOutQuart', 'easeInOutQuart',
        'easeInQuint', 'easeOutQuint', 'easeInOutQuint',
        'easeInSine', 'easeOutSine', 'easeInOutSine',
        'easeInExpo', 'easeOutExpo', 'easeInOutExpo',
        'easeInCirc', 'easeOutCirc', 'easeInOutCirc',
        'easeInElastic', 'easeOutElastic', 'easeInOutElastic',
        'easeInBack', 'easeOutBack', 'easeInOutBack',
        'easeInBounce', 'easeOutBounce', 'easeInOutBounce',
        'easeInPoly', 'easeOutPoly', 'easeInOutPoly'
    ]
    PLAYING = '##PLAYING##'
    COMPLETED = '##COMPLETED##'
    PAUSED = '##PAUSE##'
    STOPPED = '##STOPPED##'
    IDLE = '##IDLE##'

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
        self.startTime = 0
        self.duration = duration
        self.endTime = self.duration
        self.tweenType = tweenType
        #self.easingType = easingType
        self.on_complete = onCompleted
        self.playbackState = self.IDLE
        reg.add('Tween', self.name, self)

        self._pauseTime = 0

    def play(self):
        if self.playbackState == self.PAUSED:
            self.startTime += v.elapsed-self._pauseTime
        else:
            self.startTime = v.elapsed
            self.baseValue = cusGetAttr(self.spriteRef, self.valueName)
            reg.add('Tween', self.name, self)  # maybe the tween finished and we wanted it to run again

        #self.baseValue = cusGetAttr(self.obj, self.valueName)
        self.endTime = self.startTime + self.duration
        self.playbackState = self.PLAYING
        self.completed = False
    resume = play

    def pause(self):
        if self.playbackState == self.PLAYING:
            self._pauseTime = v.elapsed
            self.playbackState = self.PAUSED

    def stop(self, call_complete: bool = False):
        if self.playbackState in [self.PLAYING, self.PAUSED]:
            self.playbackState = self.STOPPED
            self.completed = True
            if call_complete and callable(self.on_complete):
                self.on_complete()

    def update(self):
        if self.playbackState == self.PLAYING:
            currentTime = v.elapsed
            t = (currentTime - self.startTime) / (self.endTime - self.startTime)
            t = min(max(t, 0), 1)

            #print(self.name, t, currentTime)
            #print(self.startTime, self.endTime)

            start = self.baseValue
            end = self.toValue
            newValue = start + (end - start) * getattr(pytweening, self.tweenType)(t)
            #setattr(self.spriteRef, self.valueName, newValue)
            #if isinstance(self.spriteRef, pygame.mixer.Sound):
            cusSetAttr(self.spriteRef, self.valueName, newValue)

            if t >= 1:
                self.completed = True
                self.playbackState = self.COMPLETED
                if callable(self.on_complete):
                    self.on_complete()
                reg.remove('Tween', self.name)