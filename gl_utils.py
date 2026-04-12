import math
from OpenGL.GL import *


def set_color(c):
    glColor4f(*c)


def draw_rect_filled(x, y, w, h, color):
    set_color(color)
    glBegin(GL_QUADS)
    glVertex2f(x,     y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x,     y + h)
    glEnd()


def draw_rect_outline(x, y, w, h, color, thickness=1):
    set_color(color)
    glLineWidth(thickness)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x,     y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x,     y + h)
    glEnd()


def draw_circle_filled(cx, cy, r, color, segments=24):
    set_color(color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    for i in range(segments + 1):
        a = 2 * math.pi * i / segments
        glVertex2f(cx + r * math.cos(a), cy + r * math.sin(a))
    glEnd()


def draw_circle_outline(cx, cy, r, color, segments=24, thickness=1):
    set_color(color)
    glLineWidth(thickness)
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        a = 2 * math.pi * i / segments
        glVertex2f(cx + r * math.cos(a), cy + r * math.sin(a))
    glEnd()


def draw_line(x1, y1, x2, y2, color, thickness=1):
    set_color(color)
    glLineWidth(thickness)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


def draw_triangle(cx, cy, size, color, angle=0):
    set_color(color)
    glBegin(GL_TRIANGLES)
    for i in range(3):
        a = angle + math.pi / 2 + 2 * math.pi * i / 3
        glVertex2f(cx + size * math.cos(a), cy + size * math.sin(a))
    glEnd()


def draw_diamond(cx, cy, w, h, color):
    set_color(color)
    glBegin(GL_QUADS)
    glVertex2f(cx,         cy - h / 2)
    glVertex2f(cx + w / 2, cy)
    glVertex2f(cx,         cy + h / 2)
    glVertex2f(cx - w / 2, cy)
    glEnd()
