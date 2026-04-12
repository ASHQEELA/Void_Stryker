import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from constants import (
    SCREEN_W, SCREEN_H, FPS, TITLE,
    CYAN, YELLOW, ORANGE, RED,
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_DEAD, STATE_WIN,
)
from font import BitmapFont
from entities.particle import explode
from entities.player import Player
from systems.starfield import StarField
from systems.wave_manager import WaveManager
from systems.score_popup import ScorePopup
from ui.hud import draw_hud
from ui.screens import draw_menu, draw_paused, draw_dead, draw_win


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), DOUBLEBUF | OPENGL)
        self._setup_gl()
        pygame.mixer.music.load("bgm.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.font = BitmapFont()
        self.clock = pygame.time.Clock()
        self.state = STATE_MENU
        self._reset()

    def _setup_gl(self):
        glViewport(0, 0, SCREEN_W, SCREEN_H)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, SCREEN_W, SCREEN_H, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glClearColor(0.01, 0.01, 0.04, 1.0)

    def _reset(self):
        self.player = Player()
        self.particles = []
        self.powerups = []
        self.score = 0
        self.combo = 1
        self.combo_timer = 0
        self.popups = []
        self.stars = StarField(150)
        self.wave_manager = WaveManager()
        self.wave_transition_timer = 0
        self.wave_banner_timer = 0
        self.wave_banner_text = ""

    def _score_callback(self, val, x, y):
        val = int(val * self.combo)
        self.score += val
        self.combo = min(self.combo + 1, 8)
        self.combo_timer = 2.5
        color = ORANGE if self.combo > 2 else YELLOW
        self.popups.append(ScorePopup(f"+{val}", x, y, color))

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    self._handle_key(event.key)

            self._update(dt)
            self._draw()
            pygame.display.flip()

    def _handle_key(self, key):
        if self.state == STATE_MENU:
            if key == K_RETURN:
                self.state = STATE_PLAYING
        elif self.state == STATE_PLAYING:
            if key in (K_ESCAPE, K_p):
                self.state = STATE_PAUSED
        elif self.state == STATE_PAUSED:
            if key in (K_ESCAPE, K_p):
                self.state = STATE_PLAYING
        elif self.state in (STATE_DEAD, STATE_WIN):
            if key == K_RETURN:
                self._reset()
                self.state = STATE_PLAYING
            elif key == K_ESCAPE:
                self.state = STATE_MENU

    def _update(self, dt):
        if self.state != STATE_PLAYING:
            return

        keys = pygame.key.get_pressed()
        self.stars.update(dt)

        if self.combo_timer > 0:
            self.combo_timer -= dt
        else:
            self.combo = 1

        self.player.update(dt, keys)
        if not self.player.alive:
            self.state = STATE_DEAD
            return

        self.wave_manager.update(
            dt, self.player.x, self.player.y,
            self.particles, self._score_callback, self.powerups,
        )

        if self.wave_banner_timer > 0:
            self.wave_banner_timer -= dt

        if self.wave_manager.wave_complete:
            self.wave_transition_timer += dt
            if self.wave_transition_timer > 2.5:
                self.wave_transition_timer = 0
                if self.wave_manager.wave >= self.wave_manager.boss_wave:
                    self.state = STATE_WIN
                    return
                self.wave_manager.next_wave()
                self.wave_banner_text = f"WAVE {self.wave_manager.wave}"
                self.wave_banner_timer = 2.0
        else:
            self.wave_transition_timer = 0

        self._update_powerups(dt)
        self._resolve_collisions()

        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update(dt)

        self.popups = [p for p in self.popups if p.alive]
        for p in self.popups:
            p.update(dt)

    def _update_powerups(self, dt):
        for pu in self.powerups:
            pu.update(dt)
            if pu.alive and pu.rect().colliderect(self.player.rect()):
                result = self.player.apply_powerup(pu.kind, self.particles)
                if result == "bomb":
                    for e in self.wave_manager.all_enemies():
                        for b in e.bullets:
                            b.alive = False
                    explode(self.particles, self.player.x, self.player.y, RED, 50, 6.0, 6)
                pu.alive = False
        self.powerups = [p for p in self.powerups if p.alive]

    def _resolve_collisions(self):
        import pygame as _pygame

        # Player bullets vs enemies
        for b in self.player.bullets:
            if not b.alive:
                continue
            br = _pygame.Rect(b.x - b.size, b.y - b.size, b.size * 2, b.size * 2)
            for e in self.wave_manager.all_enemies():
                if not e.alive:
                    continue
                if br.colliderect(e.rect()):
                    e.hit(b.damage)
                    if not b.piercing:
                        b.alive = False
                    explode(self.particles, b.x, b.y, b.color, 6, 2.0, 2)
                    break

        # Enemy bullets vs player
        for b in self.wave_manager.all_bullets():
            if not b.alive:
                continue
            br = _pygame.Rect(b.x - b.size, b.y - b.size, b.size * 2, b.size * 2)
            if br.colliderect(self.player.rect()):
                b.alive = False
                self.player.take_damage(b.damage, self.particles)
                self.combo = 1

        # Enemy ramming vs player
        for e in self.wave_manager.all_enemies():
            if not e.alive:
                continue
            if e.rect().colliderect(self.player.rect()):
                self.player.take_damage(1, self.particles)
                e.hp -= 2
                if e.hp <= 0:
                    e.alive = False

    def _draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        self.stars.draw()

        if self.state == STATE_MENU:
            draw_menu(self.font)
            return

        for p in self.particles:
            p.draw()

        for pu in self.powerups:
            pu.draw(self.font)

        for e in self.wave_manager.all_enemies():
            e.draw()

        self.player.draw()

        for popup in self.popups:
            popup.draw(self.font)

        boss_active = self.wave_manager.boss is not None
        draw_hud(self.font, self.player, self.score,
                 self.wave_manager.wave, self.combo, boss_active)

        if self.wave_banner_timer > 0:
            alpha = min(1.0, self.wave_banner_timer)
            col = (CYAN[0], CYAN[1], CYAN[2], alpha)
            self.font.draw(self.wave_banner_text, SCREEN_W // 2, SCREEN_H // 2,
                           col, "title", center=True)

        if self.state == STATE_PAUSED:
            draw_paused(self.font)
        elif self.state == STATE_DEAD:
            draw_dead(self.font, self.score, self.wave_manager.wave)
        elif self.state == STATE_WIN:
            draw_win(self.font, self.score)
