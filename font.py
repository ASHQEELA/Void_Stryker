import pygame
from OpenGL.GL import *
from constants import WHITE


class BitmapFont:
    def __init__(self, size=18):
        pygame.font.init()
        self.fonts = {
            "small":  pygame.font.SysFont("consolas,monospace", 14, bold=False),
            "normal": pygame.font.SysFont("consolas,monospace", size, bold=False),
            "bold":   pygame.font.SysFont("consolas,monospace", size, bold=True),
            "large":  pygame.font.SysFont("consolas,monospace", 28, bold=True),
            "title":  pygame.font.SysFont("consolas,monospace", 52, bold=True),
            "sub":    pygame.font.SysFont("consolas,monospace", 22, bold=True),
        }
        self._cache = {}

    def _make_texture(self, text, font_key, color_rgba):
        key = (text, font_key, color_rgba)
        if key in self._cache:
            return self._cache[key]
        pg_color = tuple(int(c * 255) for c in color_rgba[:3])
        surf = self.fonts[font_key].render(text, True, pg_color)
        w, h = surf.get_size()
        data = pygame.image.tobytes(surf, "RGBA", True)
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        self._cache[key] = (tex, w, h)
        return tex, w, h

    def draw(self, text, x, y, color=WHITE, font_key="normal", center=False, right=False):
        tex, w, h = self._make_texture(text, font_key, color)
        if center:
            x -= w / 2
        elif right:
            x -= w
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex)
        glColor4f(1, 1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x,     y + h)
        glTexCoord2f(1, 0); glVertex2f(x + w, y + h)
        glTexCoord2f(1, 1); glVertex2f(x + w, y)
        glTexCoord2f(0, 1); glVertex2f(x,     y)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        return w, h

    def size(self, text, font_key="normal"):
        return self.fonts[font_key].size(text)
