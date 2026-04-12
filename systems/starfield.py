import random
from OpenGL.GL import *
from constants import SCREEN_W, SCREEN_H


class StarField:
    def __init__(self, count=120):
        self.stars = []
        for _ in range(count):
            x = random.uniform(0, SCREEN_W)
            y = random.uniform(0, SCREEN_H)
            speed = random.uniform(0.3, 2.0)
            size  = random.uniform(0.5, 2.0)
            brightness = random.uniform(0.3, 1.0)
            self.stars.append([x, y, speed, size, brightness])

    def update(self, dt):
        for s in self.stars:
            s[1] += s[2] * dt * 60
            if s[1] > SCREEN_H:
                s[1] = 0
                s[0] = random.uniform(0, SCREEN_W)

    def draw(self):
        for s in self.stars:
            b = s[4]
            glColor4f(b, b, b * 1.2, 1.0)
            glPointSize(s[3])
            glBegin(GL_POINTS)
            glVertex2f(s[0], s[1])
            glEnd()
