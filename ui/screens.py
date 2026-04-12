from constants import (
    SCREEN_W, SCREEN_H,
    CYAN, YELLOW, WHITE, RED, GREEN, ORANGE, GRAY, PINK, PURPLE
)
from gl_utils import draw_rect_filled, draw_rect_outline


def draw_menu(font):
    pw, ph = 600, 620
    px = SCREEN_W // 2 - pw // 2
    py = SCREEN_H // 2 - ph // 2

    draw_rect_filled(px, py, pw, ph, (0.02, 0.02, 0.08, 0.92))
    draw_rect_outline(px, py, pw, ph, CYAN, 2)
    draw_rect_outline(px + 4, py + 4, pw - 8, ph - 8, (0.0, 0.5, 1.0, 0.4), 1)

    cx = SCREEN_W // 2
    padding = 40
    left_x  = px + padding
    right_x = px + pw - padding

    y = py + 40
    font.draw("VOID STRIKER", cx, y, CYAN, "title", center=True)
    y += 50
    font.draw("A SPACE COMBAT EXPERIENCE", cx, y, (0.5, 0.8, 1.0, 1.0), "sub", center=True)

    y += 50
    font.draw("CONTROLS", cx, y, YELLOW, "bold", center=True)
    y += 30
    for key, action in [("WASD / ARROWS", "Move"), ("SPACE", "Shoot"), ("ESC / P", "Pause")]:
        font.draw(key, left_x, y, WHITE, "normal")
        font.draw(action, right_x, y, WHITE, "normal", right=True)
        y += 26

    y += 20
    font.draw("ENEMIES", cx, y, YELLOW, "bold", center=True)
    y += 28
    for name, desc, col in [
        ("SCOUT",   "Fast, zigzag, 100 pts",       RED),
        ("TANK",    "Slow, 3-way shot, 400 pts",    ORANGE),
        ("SNIPER",  "Aims at you, 250 pts",          PURPLE),
        ("SWARMER", "Rushes you, 75 pts",            GREEN),
        ("BOSS",    "Appears wave 5, 2000 pts",      (1.0, 0.3, 0.0, 1.0)),
    ]:
        font.draw(name, left_x, y, col, "small")
        font.draw(desc, right_x, y, col, "small", right=True)
        y += 24

    y += 20
    font.draw("POWER-UPS", cx, y, YELLOW, "bold", center=True)
    y += 28
    for lbl, desc, col in [
        ("SHD", "Shield - absorbs one hit",         CYAN),
        ("RPD", "Rapid Fire - faster shooting",      YELLOW),
        ("SPR", "Spread - 5-way shot",               GREEN),
        ("LZR", "Laser - pierce, high damage",       PINK),
        ("BMB", "Bomb - clears all bullets",         ORANGE),
        ("HP+", "Health - restore 2 HP",             (0.2, 1.0, 0.4, 1.0)),
    ]:
        font.draw(lbl, left_x, y, col, "small")
        font.draw(desc, right_x, y, col, "small", right=True)
        y += 24

    font.draw("PRESS ENTER TO START", cx, py + ph - 20,
              (0.8, 1.0, 0.8, 1.0), "bold", center=True)


def draw_paused(font):
    draw_rect_filled(0, 0, SCREEN_W, SCREEN_H, (0, 0, 0, 0.5))
    font.draw("PAUSED", SCREEN_W // 2, SCREEN_H // 2 + 20, YELLOW, "title", center=True)
    font.draw("Press P or ESC to resume", SCREEN_W // 2, SCREEN_H // 2 - 10,
              WHITE, "sub", center=True)


def draw_dead(font, score, wave):
    draw_rect_filled(0, 0, SCREEN_W, SCREEN_H, (0, 0, 0, 0.65))
    font.draw("HULL BREACH", SCREEN_W // 2, SCREEN_H // 2 + 60, RED, "title", center=True)
    font.draw("You were destroyed.", SCREEN_W // 2, SCREEN_H // 2 + 20, WHITE, "sub", center=True)
    font.draw(f"Final Score:  {score}", SCREEN_W // 2, SCREEN_H // 2 - 15, YELLOW, "bold", center=True)
    font.draw(f"Wave Reached: {wave}", SCREEN_W // 2, SCREEN_H // 2 - 40, CYAN, "bold", center=True)
    font.draw("ENTER to play again    ESC to quit", SCREEN_W // 2, SCREEN_H // 2 - 75,
              GRAY, "normal", center=True)


def draw_win(font, score):
    draw_rect_filled(0, 0, SCREEN_W, SCREEN_H, (0, 0, 0, 0.65))
    font.draw("SECTOR CLEARED", SCREEN_W // 2, SCREEN_H // 2 + 60, CYAN, "title", center=True)
    font.draw("The boss has been defeated.", SCREEN_W // 2, SCREEN_H // 2 + 20,
              WHITE, "sub", center=True)
    font.draw(f"Final Score:  {score}", SCREEN_W // 2, SCREEN_H // 2 - 15, YELLOW, "bold", center=True)
    font.draw("ENTER to play again    ESC to quit", SCREEN_W // 2, SCREEN_H // 2 - 55,
              GRAY, "normal", center=True)
