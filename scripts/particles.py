import pygame
from .engine import import_sprite_sheets
from enum import Enum
import random

class ParticleEnum(Enum):

    FLOAT = 0
    FADE = 1

class ParticleManeger:

    def __init__(self, master):
        self.master = master
        master.particle = self
        self.particle_grp = pygame.sprite.Group()
        self.screen = pygame.display.get_surface()
        
        self.animations = {}
        self.animations.update(import_sprite_sheets("graphics/particles"))

    def spawn_blood(self, pos, swallow=False):

        if swallow: anim, speed = "blood_swallow", 0.03
        else: anim, speed = "blood_bite", 0.1

        AnimatedParticle(self.master, [self.particle_grp], pos, self.animations[anim], speed, 0, set())

    def spawn_bubbles(self, pos):

        AnimatedParticle(self.master, [self.particle_grp], pos, self.animations['bubbles'], 0.1, 0, set())

    def spawn_dash(self, player):

        offset = player.direction * player.head_offset

        for i in range(1,6):
            pos = player.bite_rect.center - offset - offset/5*i
            speed = random.choice((0.1, 0.08, 0.12, 0.14))*3

            AnimatedParticle(self.master, [self.particle_grp], pos, self.animations["dash_particles"], speed, player.angle, set())

    def draw(self):
        self.particle_grp.draw(self.screen)

    def update(self):
        self.particle_grp.update()



class Particle(pygame.sprite.Sprite):

    def __init__(self, master, grps, pos, image, duration, types:set) -> None:
        super().__init__(grps)
        self.master = master

        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(center=self.pos + self.master.world.offset)
        self.duration = duration
        self.types = types

    def update(self):
        pass



class AnimatedParticle(Particle):

    def __init__(self, master, grps, pos, animation, speed, angle, types:set) -> None:

        self.animtion = animation
        self.anim_frame = 0
        self.anim_speed = speed
        self.angle = angle

        super().__init__(master, grps, pos, animation[0], 0, types)

    def update_image(self):

        try:
            self.image = self.animtion[int(self.anim_frame)]
        except IndexError:
            self.kill()
            return
            self.anim_frame = 0
            self.image = self.animtion[0]

        self.anim_frame += self.anim_speed *self.master.dt
        if self.angle:
            self.image = pygame.transform.rotate(self.image,self.angle)
        self.rect = self.image.get_rect(center=self.pos + self.master.world.offset)

    def update(self):

        super().update()
        self.update_image()
    