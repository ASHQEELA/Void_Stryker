from constants import YELLOW


class ScorePopup:
    def __init__(self, text, x, y, color=YELLOW):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.life = 1.0

    def update(self, dt):
        self.y -= 0.5 * dt * 60
        self.life -= dt

    def draw(self, font):
        alpha_color = (self.color[0], self.color[1], self.color[2], self.life)
        font.draw(self.text, self.x, self.y, alpha_color, "bold", center=True)

    @property
    def alive(self):
        return self.life > 0
