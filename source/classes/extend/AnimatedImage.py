import source.classes.base.Sprite as Sprite
import source.functions.file_funcs as ff
from path import Path
import pygame

class Animation:
    def __init__(self):
        self.name = ''
        self.playing = False
        self.frame = 0
        self.numFrames = 0

class AnimatedImage(Sprite):
    def __init__(self, name, imagePath):
        super().__init__(name, dataType = 'AnimatedImage')
        self.filePath = Path(imagePath)
        self.animType = 'gif' if self.filePath.suffix == '.gif' else None
        if self.filePath.suffix == '.png':
            for fileType in ['xml', 'json']:
                self.animData = self.filePath.path.with_suffix(f'.{fileType}')
                if self.animData.exists():
                    self.animType = fileType
                    self.animData = ff.parseTxt(self.animData)
                    break
            if self.animType == 'json':
                print(f'json format is not supported yet! <class AnimatedImage:{name}>')
        self.img = pygame.image.load(self.filePath).convert_alpha()

        self.animations = {}
        self.curAnim = Animation()
        self.animQueue = []

    # Adding animation with same name replaces the old animation! (Not a bug)
    def addAnimation(self, name, prefix, fps, loop):
        if self.animType == 'gif':
            return
        elif self.animType == 'xml':
            subtexture = self.animData['SubTexture']
            prefix = str(prefix or name)
            if name in self.animations:
                print(f'Animation {name} is being replaced!')
            self.animations[name] = []
            for subtext in subtexture:
                if isinstance(subtext, dict) and '@name' in subtext and subtext['@name'].startswith(prefix):
                    data = {
                        'order': int(subtext['@name'][-4:]),
                        'atlas': {
                            'x': int(subtext['@x']),
                            'y': int(subtext['@y']),
                            'width': int(subtext['@width']),
                            'height': int(subtext['@height'])
                        },
                        'frame': {
                            'x': int(subtext['@frameX']),
                            'y': int(subtext['@frameY']),
                            'width': int(subtext['@frameWidth']),
                            'height': int(subtext['@frameHeight'])
                        }
                    }
                    self.animations[name].append(data)
            self.animations[name].sort(key=lambda frame: frame['order'])
        elif self.animType == 'json':
            raise NotImplementedError

    def playAnim(self, name, forced = False):
        if name in self.animations:
            if forced:
                self.animQueue.insert(0, name)
            else:
                self.animQueue.append(name)
    def update(self):
        if self.animQueue[0] != getattr(self.curAnim, 'name'):
            setattr(self.curAnim, 'name', self.animQueue[0])
            setattr(self.curAnim, 'playing', True)
            setattr(self.curAnim, 'frame', 0)
            setattr(self.curAnim, 'numFrames', len(self.animations[self.animQueue[0]]))
