import pygame
import source.variables as v
from source.classes.BaseInstance import BaseInstance

class Sound(pygame.mixer.Sound, BaseInstance):
    def __init__(self, filename, bpm):
        pygame.mixer.Sound.__init__(self, filename)
        BaseInstance.__init__(self, filename, 'Sound')

        self.bpm = int(bpm) or 100
        self.secondsPerBeat = 60 / self.bpm
        self.secondsPerStep = self.secondsPerBeat / 4

        self._last = {'beat': 0.0, 'step': 0.0}
        self.beatHit = False
        self.stepHit = False
        self.playing = False

        self.beatsCount = 0
        self.stepsCount = 0

        self._playStartTime = 0
        self._trimSound: pygame.mixer.Sound | None = None
        self._array = pygame.sndarray.array(self)

    def play(self, loops: int = 0, pos_ms: int = 0, maxtime_ms: int = -1, fade_ms: int = 0):
        pos_sec = pos_ms/1000
        self.stepsCount = 0
        self.beatsCount = 0
        self.playing = True
        self.beatHit = True
        self.stepHit = True
        self._playStartTime = v.elapsed-pos_sec
        self._last = {'beat': self._playStartTime, 'step': self._playStartTime}

        playFully = False
        if maxtime_ms == -1:
            maxtime_ms = 0
            playFully = True
        elif maxtime_ms-pos_ms < 0:
            raise ValueError(f'Ending position ({maxtime_ms}ms) cannot be negative!')
        if pos_sec > self.get_length():
            raise ValueError(f'Starting position ({pos_ms}ms) cannot be further than the length of the audio file ('
                             f'{self.get_length()*1000}ms)!')

        if pos_ms > 0:
            trimmed_arr = self._array[int(pos_ms*v.sampleRate/1000):, :]
            self._trimSound = pygame.sndarray.make_sound(trimmed_arr)
            self._trimSound.play(loops, 0 if playFully else maxtime_ms-pos_ms, fade_ms)
        elif pos_ms == 0:
            super().play(loops, maxtime_ms, fade_ms)
        else:
            raise ValueError(f'Starting position ({pos_ms}ms) cannot be negative!')


    def stop(self):
        self.playing = False
        if isinstance(self._trimSound, pygame.mixer.Sound):
            self._trimSound.stop()
            self._trimSound = None
        super().stop()

    def set_volume(self, value):
        super().set_volume(value)
        if isinstance(self._trimSound, pygame.mixer.Sound):
            self._trimSound.set_volume(value)

    def get_volume(self):
        if isinstance(self._trimSound, pygame.mixer.Sound):
            return self._trimSound.get_volume()
        else:
            return super().get_volume()

    def change_bpm(self, newBPM):
        self.bpm = int(newBPM) or self.bpm
        self.secondsPerBeat = 60 / self.bpm
        self.secondsPerStep = self.secondsPerBeat / 4

    def get_sound_position(self):
        return v.elapsed-self._playStartTime

    def update(self):
        self.beatHit = False
        self.stepHit = False

        while v.elapsed - self._last['beat'] >= self.secondsPerBeat:
            self._last['beat'] += self.secondsPerBeat
            if self.playing:
                self.beatHit = True
                self.beatsCount += 1

        while v.elapsed - self._last['step'] >= self.secondsPerStep:
            self._last['step'] += self.secondsPerStep
            if self.playing:
                self.stepHit = True
                self.stepsCount += 1