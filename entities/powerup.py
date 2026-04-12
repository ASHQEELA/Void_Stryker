import math
import pygame
from constants import SCREEN_H, POWERUP_COLORS, POWERUP_LABELS
from gl_utils import draw_circle_filled, draw_circle_outline


class PowerUp:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.color = POWERUP_COLORS[kind]
        self.label = POWERUP_LABELS[kind]
        self.vy = 1.5
        self.alive = True
        self.t = 0
        self.r = 14

    def update(self, dt):
        self.y += self.vy * dt * 60
        self.t += dt
        if self.y > SCREEN_H + 30:
            self.alive = False

    def draw(self, font):
        pulse = 0.85 + 0.15 * math.sin(self.t * 4)
        r = self.r * pulse
        draw_circle_outline(self.x, self.y, r + 4, (self.color[0], self.color[1], self.color[2], 0.3), 20, 1)
        draw_circle_filled(self.x, self.y, r, (self.color[0] * 0.3, self.color[1] * 0.3, self.color[2] * 0.3, 0.9), 20)
        draw_circle_outline(self.x, self.y, r, self.color, 20, 2)
        font.draw(self.label, self.x, self.y - 6, self.color, "small", center=True)

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)
