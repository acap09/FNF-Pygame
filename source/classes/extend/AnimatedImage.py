from source.classes.datatypes.UDims import UDim2
from source.classes.extend.Image import Image
import source.functions.file_funcs as ff
import source.variables as v
import pygame

class Animation():
    def __init__(self):
        self.name = ''
        self.playing = False
        self.paused = False
        self.frame = 0
        self.frame_surf = None
        self.num_frames = 0
        self.fps = 32
        self.spf = 1/self.fps
        self.loop = False

class AnimatedImage(Image):
    #PLAYING = '##PLAYING##'
    #IDLE = '##IDLE##'
    def __init__(self, name, imagePath, position = None):
        super().__init__(name, imagePath, position)
        self.animType = 'gif' if self.filePath.suffix == '.gif' else None
        if self.filePath.suffix == '.png':
            for fileType in ['xml', 'json']:
                self.animData = self.filePath.with_suffix(f'.{fileType}')
                if self.animData.exists():
                    self.animType = fileType
                    self.animData = ff.parseTxt(self.animData)
                    break
            if self.animType == 'json':
                print(f'json format is not supported yet! <class AnimatedImage:{name}>')
        self.originalImg = self.originalImg.convert_alpha()
        self.img = self.originalImg
        self.scaleSize = UDim2(1, 0, 1, 0)

        self.curAnim = Animation()
        if self.animType == 'gif':
            self.animations = pygame.image.load_animation(self.filePath)
            return
        self.animations = {}
        self.animQueue = []

        self._lastFrameTime = 0
        #self._lastFrame: pygame.Surface = None

    # Adding animation with same name replaces the old animation! (Not a bug)
    def add_animation(self, name: str, prefix: str, fps: int = 32, indices: list[int] = None, loop: bool = False):
        #if not isinstance(indices, list):
        #    raise TypeError('Indices must be a list!')
        if self.animType == 'gif':
            self.curAnim.fps = fps
            self.curAnim.loop = loop
            self.curAnim.name = 'GIF_ANIMATION'
        elif self.animType == 'xml':
            #print(self.animData)
            subtexture = self.animData['TextureAtlas']['SubTexture']
            #print(subtexture)
            prefix = str(prefix or name)
            if name in self.animations:
                print(f'Animation {name} is being replaced!')
            self.animations[name] = {
                'data': {
                    'fps': fps,
                    'loop': loop
                },
                'index_map': [],
                'sub_textures': []
            }

            for subtext in subtexture:
                if isinstance(subtext, dict) and '@name' in subtext and subtext['@name'].startswith(prefix):
                    order = int(subtext['@name'][-4:])
                    if indices is not None and order not in indices:
                        continue
                    if '@frameX' not in subtext:
                        subtext['@frameX'] = 0
                    if '@frameY' not in subtext:
                        subtext['@frameY'] = 0
                    if '@frameWidth' not in subtext:
                        subtext['@frameWidth'] = subtext['@width']
                    if '@frameHeight' not in subtext:
                        subtext['@frameHeight'] = subtext['@height']
                    data = {
                        'order': order,
                        'surface': None,
                        'frameUDim': UDim2(),
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
                    data['surface'] = self.get_frame(data)
                    frameSize = data['frame']
                    data['frameUDim'] = UDim2(frameSize['width']/2000, 0, frameSize['height']/1125, 0)
                    self.animations[name]['sub_textures'].append(data)

            self.animations[name]['sub_textures'].sort(key=lambda frame: frame['order'])
            self.animations[name]['index_map'] = {n: frame['order'] for n, frame in enumerate(self.animations[name][
                                                                                         'sub_textures'])}
            #print(self.animations[name])

        elif self.animType == 'json':
            raise NotImplementedError

    def play_anim(self, anim: str = None, forced: bool = False):
        self.paused = False
        if self.animType == 'gif':
            pass
        else:
            if anim is None:
                raise TypeError('Animation name must be given!')
            elif anim not in self.animations:
                raise KeyError(f'Animation {anim} does not exist!')

            #print('yes', anim)

            if forced:
                self.animQueue.insert(0, anim)
            else:
                self.animQueue.append(anim)

    def resume_anim(self):
        self.curAnim.paused = False

    def pause_anim(self):
        self.curAnim.paused = True

    def clear_queue(self):
        self.animQueue = []

    def stop_anim(self, clearQueue = True):
        if clearQueue:
            self.clear_queue()
        self.curAnim.playing = False

    def get_frame(self, animData = None) -> pygame.Surface:
        if animData is not None:

            atlasInfo = animData['atlas']
            ax, ay = atlasInfo['x'], atlasInfo['y']
            aw, ah = atlasInfo['width'], atlasInfo['height']
            frameInfo = animData['frame']
            fx, fy = frameInfo['x'], frameInfo['y']
            fw, fh = frameInfo['width'], frameInfo['height']
        else:
            curAnim = self.curAnim
            if not curAnim.playing or curAnim.name not in self.animations:
                return curAnim.frame_surf

            animData = self.animations[curAnim.name]
            frames = animData['sub_textures']

            curFrame = min(curAnim.frame, len(frames) - 1)

            atlasInfo = frames[curFrame]['atlas']
            ax, ay = atlasInfo['x'], atlasInfo['y']
            aw, ah = atlasInfo['width'], atlasInfo['height']
            frameInfo = frames[curFrame]['frame']
            fx, fy = frameInfo['x'], frameInfo['y']
            fw, fh = frameInfo['width'], frameInfo['height']

        extractSurf = self.originalImg.subsurface(pygame.Rect(ax, ay, aw, ah)).copy()
        frameSurf = pygame.Surface((fw, fh), pygame.SRCALPHA)
        frameSurf.blit(extractSurf, (-fx, -fy))
        return frameSurf

    '''def updateAnim(self):
        if not self.curAnim.playing:
            return

        while v.elapsed - self._lastFrameTime >= self.curAnim.spf:
            if self.curAnim.frame > self.curAnim.num_frames:
                if self.curAnim.loop:
                    self.curAnim.frame = 0
                else:
                    self.curAnim.playing = False
                    return
            self.curAnim.frame += 1
            self._lastFrameTime += self.curAnim.spf
        self.curAnim.frame_surf = self.getFrameAnim()'''
    def update_anim(self):
        if (not self.curAnim.playing) or self.curAnim.paused:
            return
        isDone = False
        while v.elapsed - self._lastFrameTime >= self.curAnim.spf:
            self.curAnim.frame += 1
            self._lastFrameTime += self.curAnim.spf
            if self.curAnim.frame >= self.curAnim.num_frames:
                if self.curAnim.loop:
                    self.curAnim.frame = 0
                else:
                    self.curAnim.playing = False
                    isDone = True
                    break

        frameSurf = None
        frameSize = UDim2()
        #logicalIdx = self.animations[self.curAnim.name]['index_map']
        #print(self.animations[self.curAnim.name])
        try:
            frameSurf = self.animations[self.curAnim.name]['sub_textures'][self.curAnim.frame]['surface']
            #frameSize = self.animations[self.curAnim.name]['sub_textures'][self.curAnim.frame]['frameUDim']
        except IndexError:
            isDone = True
        if isinstance(frameSurf, pygame.Surface):
            #print(frameSurf.get_size())
            #print('scale', self.scaleSize.absPos(frameSurf, True))
            frameSurf = pygame.transform.smoothscale(frameSurf, self.scaleSize.absPos(frameSurf, True))
            frameSize = UDim2(frameSurf.get_width()/1000, 0, frameSurf.get_height()/562.5, 0)
            self.curAnim.frame_surf = pygame.transform.smoothscale(frameSurf, frameSize.absPos(tupleify=True))
            #print(self.curAnim.frame_surf.get_size())
        if isDone:
            self.curAnim.playing = False


    def update(self, dt=None):
        if not self.curAnim.paused and (len(self.animQueue) > 0 and (self.curAnim.name != self.animQueue[0] or not
        self.curAnim.playing) and self.animQueue[0] in self.animations):
            name = self.animQueue.pop(0)
            #print(name)
            self.curAnim.name = name
            self.curAnim.frame = 0
            self.curAnim.playing = True
            self.curAnim.num_frames = len(self.animations[name]['sub_textures'])-1
            self.curAnim.fps = self.animations[name]['data']['fps']
            self.curAnim.spf = 1/self.curAnim.fps
            self.curAnim.loop = self.animations[name]['data']['loop']
            self._lastFrameTime = v.elapsed-self.curAnim.spf

        #print(self.curAnim.name)

        #self.update_anim()
        if self.animType != 'gif':
            self.update_anim()
            self.img = self.curAnim.frame_surf or self.originalImg
