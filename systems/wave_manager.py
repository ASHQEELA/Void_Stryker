import random
from constants import SCREEN_W, POWERUP_TYPES
from entities.enemies import ScoutEnemy, TankEnemy, SniperEnemy, SwarmerEnemy
from entities.boss import BossEnemy
from entities.particle import explode
from entities.powerup import PowerUp


class WaveManager:
    def __init__(self):
        self.wave = 1
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_queue = []
        self.wave_clear_timer = 0
        self.boss = None
        self.boss_wave = 5
        self.wave_complete = False
        self._build_wave()

    def _build_wave(self):
        self.wave_complete = False
        self.spawn_queue = []
        w = self.wave

        if w >= self.boss_wave:
            self.spawn_queue = [("boss", 0)]
            return

        n_scouts   = 3 + w * 2
        n_swarmers = 2 + w
        n_tanks    = max(0, w - 1)
        n_snipers  = max(0, w - 2)

        t = 0.5
        for _ in range(n_scouts):
            self.spawn_queue.append(("scout", t))
            t += random.uniform(0.4, 0.9)
        for _ in range(n_swarmers):
            self.spawn_queue.append(("swarmer", t))
            t += random.uniform(0.3, 0.7)
        for _ in range(n_tanks):
            self.spawn_queue.append(("tank", t))
            t += random.uniform(1.0, 1.8)
        for _ in range(n_snipers):
            self.spawn_queue.append(("sniper", t))
            t += random.uniform(0.8, 1.4)

        random.shuffle(self.spawn_queue)

    def update(self, dt, player_x, player_y, particles, score_callback, powerups):
        self.spawn_timer += dt

        while self.spawn_queue and self.spawn_timer >= self.spawn_queue[0][1]:
            kind, _ = self.spawn_queue.pop(0)
            x = random.uniform(60, SCREEN_W - 60)
            if kind == "scout":
                self.enemies.append(ScoutEnemy(x, -30))
            elif kind == "swarmer":
                self.enemies.append(SwarmerEnemy(x, -30))
            elif kind == "tank":
                self.enemies.append(TankEnemy(x, -60))
            elif kind == "sniper":
                self.enemies.append(SniperEnemy(x, -40))
            elif kind == "boss":
                self.boss = BossEnemy()

        for e in self.enemies:
            e.update(dt, player_x, player_y)

        if self.boss:
            self.boss.update(dt, player_x, player_y)
            if not self.boss.alive:
                explode(particles, self.boss.x, self.boss.y, self.boss.color, 60, 6.0, 8)
                score_callback(self.boss.score_val, self.boss.x, self.boss.y)
                self.boss = None
                self.wave_complete = True
                return

        for e in self.enemies:
            if not e.alive:
                explode(particles, e.x, e.y, e.color, 20, 4.0)
                score_callback(e.score_val, e.x, e.y)
                if random.random() < 0.22:
                    kind = random.choice(POWERUP_TYPES)
                    powerups.append(PowerUp(e.x, e.y, kind))

        self.enemies = [e for e in self.enemies if e.alive]

        if not self.spawn_queue and not self.enemies and not self.boss and not self.wave_complete:
            self.wave_complete = True

    def next_wave(self):
        self.wave += 1
        self.spawn_timer = 0
        self.enemies = []
        self.boss = None
        self.wave_complete = False
        self._build_wave()

    def all_enemies(self):
        result = list(self.enemies)
        if self.boss:
            result.append(self.boss)
        return result

    def all_bullets(self):
        bullets = []
        for e in self.enemies:
            bullets.extend(e.bullets)
        if self.boss:
            bullets.extend(self.boss.bullets)
        return bullets
