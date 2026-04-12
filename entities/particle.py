import math
import random
from gl_utils import draw_circle_filled


class Particle:
    def __init__(self, x, y, vx, vy, color, life, size=3):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size

    def update(self, dt):
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.life -= dt
        self.vx *= 0.97
        self.vy *= 0.97

    def draw(self):
        ratio = max(0, self.life / self.max_life)
        c = (self.color[0], self.color[1], self.color[2], ratio * 0.9)
        draw_circle_filled(self.x, self.y, self.size * ratio, c)

    @property
    def alive(self):
        return self.life > 0


def explode(particles, x, y, color, count=18, speed=3.0, size=3):
    for _ in range(count):
        a = random.uniform(0, 2 * math.pi)
        v = random.uniform(0.5, speed)
        life = random.uniform(0.3, 0.8)
        sz = random.uniform(size * 0.5, size)
        particles.append(Particle(x, y, math.cos(a) * v, math.sin(a) * v, color, life, sz))
