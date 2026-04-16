SCREEN_W, SCREEN_H = 900, 700
FPS = 60
TITLE = "VOID STRYKER"

# Colors (RGBA floats)
BLACK   = (0.0, 0.0, 0.0, 1.0)
WHITE   = (1.0, 1.0, 1.0, 1.0)
CYAN    = (0.0, 1.0, 1.0, 1.0)
YELLOW  = (1.0, 0.95, 0.0, 1.0)
RED     = (1.0, 0.15, 0.15, 1.0)
GREEN   = (0.1, 1.0, 0.3, 1.0)
ORANGE  = (1.0, 0.55, 0.0, 1.0)
PURPLE  = (0.7, 0.0, 1.0, 1.0)
BLUE    = (0.1, 0.4, 1.0, 1.0)
GRAY    = (0.4, 0.4, 0.4, 1.0)
PINK    = (1.0, 0.3, 0.8, 1.0)
DARKRED = (0.6, 0.0, 0.0, 1.0)

# Game states
STATE_MENU    = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED  = "paused"
STATE_DEAD    = "dead"
STATE_WIN     = "win"

# Power-up definitions
POWERUP_TYPES = ["shield", "rapid", "spread", "laser", "bomb", "health"]
POWERUP_COLORS = {
    "shield": CYAN,
    "rapid":  YELLOW,
    "spread": GREEN,
    "laser":  PINK,
    "bomb":   ORANGE,
    "health": (0.2, 1.0, 0.4, 1.0),
}
POWERUP_LABELS = {
    "shield": "SHD",
    "rapid":  "RPD",
    "spread": "SPR",
    "laser":  "LZR",
    "bomb":   "BMB",
    "health": "HP+",
}
