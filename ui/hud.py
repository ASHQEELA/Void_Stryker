from constants import (
    SCREEN_W, SCREEN_H,
    CYAN, YELLOW, WHITE, RED, GREEN, ORANGE, GRAY, PINK
)
from gl_utils import draw_rect_filled, draw_rect_outline


def draw_hud(font, player, score, wave, combo, boss_active):
    hud_y = SCREEN_H - 120

    draw_rect_filled(8, hud_y, 220, 120, (0.0, 0.0, 0.0, 0.55))
    draw_rect_outline(8, hud_y, 220, 120, CYAN, 1)

    font.draw("VOID STRYKER", 18, SCREEN_H - 24, CYAN, "small")

    # HP pips
    font.draw("HULL", 18, SCREEN_H - 108, GRAY, "small")
    for i in range(player.max_hp):
        color = RED if i < player.hp else (0.2, 0.2, 0.2, 1.0)
        draw_rect_filled(18 + i * 26, SCREEN_H - 92, 20, 12, color)
        draw_rect_outline(18 + i * 26, SCREEN_H - 92, 20, 12, WHITE, 1)

    font.draw(f"SCORE  {score:>08}", 18, SCREEN_H - 72, WHITE, "normal")
    font.draw(f"WAVE   {wave}", 18, SCREEN_H - 52, YELLOW, "normal")

    if combo > 1:
        font.draw(f"COMBO  x{combo}", 18, SCREEN_W - 32, ORANGE, "normal")

    # Active power-up icons
    py_icons = SCREEN_H - 140
    icons = []
    if player.shield > 0: icons.append(("SHD", CYAN,   player.shield))
    if player.rapid  > 0: icons.append(("RPD", YELLOW, player.rapid))
    if player.spread > 0: icons.append(("SPR", GREEN,  player.spread))
    if player.laser  > 0: icons.append(("LZR", PINK,   player.laser))

    for i, (lbl, col, _rem) in enumerate(icons):
        bx = 18 + i * 58
        draw_rect_filled(bx, py_icons - 18, 52, 18,
                         (col[0] * 0.15, col[1] * 0.15, col[2] * 0.15, 0.9))
        draw_rect_outline(bx, py_icons - 18, 52, 18, col, 1)
        font.draw(lbl, bx + 26, py_icons - 14, col, "small", center=True)

    if boss_active:
        font.draw("BOSS", SCREEN_W // 2, 34, RED, "bold", center=True)
