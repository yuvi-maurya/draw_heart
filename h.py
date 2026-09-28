import pygame
import random
import math
import sys

pygame.init()

WIDTH, HEIGHT = 800, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Love.exe")
clock = pygame.time.Clock()

CENTER = (WIDTH // 2, HEIGHT // 2 + 40)
NUM_LAYERS = 5            # kitne nested hearts
BUTTERFLIES_PER_HEART = 34
CYCLE_SECONDS = 9         # ek heart ko bahar se andar aane me kitna time
MAX_HEART_SCALE = 21      # sabse bada heart ka size


# ---------- Butterfly shape ----------
UPPER_WING = [(0.05, -0.05), (0.55, -0.60), (1.00, -0.65), (0.95, -0.15), (0.10, 0.05)]
LOWER_WING = [(0.05, 0.05), (0.75, 0.10), (0.80, 0.65), (0.35, 0.60), (0.05, 0.15)]


def make_color():
    """Pink se purple ke beech ka random neon color."""
    t = random.random()
    r = int(255 - 90 * t)
    g = int(70 + 30 * t)
    b = 255
    return (r, g, b)


def draw_butterfly(surface, x, y, size, flap, angle, color):
    """Ek butterfly draw karta hai. flap: 0..1 (wings kitne khule hain)."""
    if size < 1.5:
        pygame.draw.circle(surface, color, (int(x), int(y)), 1)
        return

    cos_a, sin_a = math.cos(angle), math.sin(angle)

    def transform(px, py, mirror):
        px = px * flap * (-1 if mirror else 1)
        px, py = px * size, py * size
        rx = px * cos_a - py * sin_a
        ry = px * sin_a + py * cos_a
        return (x + rx, y + ry)

    dim = tuple(int(c * 0.45) for c in color)

    for mirror in (False, True):
        for wing in (UPPER_WING, LOWER_WING):
            pts = [transform(px, py, mirror) for px, py in wing]
            pygame.draw.polygon(surface, color, pts)
            pygame.draw.polygon(surface, dim, pts, 1)

    # body
    top = transform(0, -0.25, False)
    bottom = transform(0, 0.35, False)
    pygame.draw.line(surface, (255, 220, 255), top, bottom, max(1, int(size * 0.08)))


# ---------- Heart shape ----------
def heart_point(t, scale):
    """Classic parametric heart. Screen coordinates return karta hai."""
    hx = 16 * math.sin(t) ** 3
    hy = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return (CENTER[0] + hx * scale, CENTER[1] - hy * scale)


class Layer:
    def __init__(self, index):
        self.offset = index / NUM_LAYERS          # har layer ka alag phase
        self.direction = 1 if index % 2 == 0 else -1
        self.butterflies = []
        for i in range(BUTTERFLIES_PER_HEART):
            self.butterflies.append({
                't': 2 * math.pi * i / BUTTERFLIES_PER_HEART,
                'phase': random.uniform(0, 2 * math.pi),
                'tilt': random.uniform(-0.5, 0.5),
                'color': make_color(),
            })

    def draw(self, surface, time):
        # s: 1 se 0 tak (bahar se andar ki taraf)
        s = 1 - ((time / CYCLE_SECONDS + self.offset) % 1)
        scale = MAX_HEART_SCALE * s

        # fade in/out taaki achanak gayab na ho
        fade = min(1, s * 5) * min(1, (1 - s) * 5)

        for b in self.butterflies:
            t = b['t'] + self.direction * time * 0.12
            x, y = heart_point(t, scale)
            size = 4 + 20 * s
            flap = 0.3 + 0.7 * abs(math.sin(time * 6 + b['phase']))
            color = tuple(int(c * fade) for c in b['color'])
            draw_butterfly(surface, x, y, size, flap, b['tilt'], color)


# ---------- Random floating butterflies ----------
class Floater:
    def __init__(self):
        self.reset(initial=True)

    def reset(self, initial=False):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT) if initial else HEIGHT + 20
        self.size = random.uniform(8, 16)
        self.speed = random.uniform(15, 40)
        self.drift = random.uniform(0.5, 1.5)
        self.phase = random.uniform(0, 2 * math.pi)
        self.color = make_color()

    def draw(self, surface, time, dt):
        self.y -= self.speed * dt
        self.x += math.sin(time * self.drift + self.phase) * 0.6
        if self.y < -20:
            self.reset()
        flap = 0.3 + 0.7 * abs(math.sin(time * 7 + self.phase))
        color = tuple(int(c * 0.75) for c in self.color)
        draw_butterfly(surface, self.x, self.y, self.size, flap, math.sin(time + self.phase) * 0.4, color)


# ---------- Title ----------
def draw_title(surface, time):
    font = pygame.font.SysFont("arial", 72, bold=True)
    text = font.render("Love.exe", True, (170, 110, 255))
    glow = font.render("Love.exe", True, (110, 60, 200))
    bob = math.sin(time * 2) * 4
    rect = text.get_rect(center=(WIDTH // 2 - 40, 70 + bob))
    surface.blit(glow, rect.move(3, 3))
    surface.blit(text, rect)
    draw_butterfly(surface, rect.right + 55, rect.centery - 5, 42,
                   0.3 + 0.7 * abs(math.sin(time * 4)), 0.3, (150, 90, 255))


layers = [Layer(i) for i in range(NUM_LAYERS)]
floaters = [Floater() for _ in range(28)]

fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.set_alpha(70)   # halka trail effect
fade_surface.fill((0, 0, 0))


def draw_frame(surface, time, dt):
    surface.blit(fade_surface, (0, 0))
    for f in floaters:
        f.draw(surface, time, dt)
    for layer in layers:
        layer.draw(surface, time)
    draw_title(surface, time)


def main():
    screen.fill((0, 0, 0))
    running = True
    while running:
        dt = clock.tick(60) / 1000
        time = pygame.time.get_ticks() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        draw_frame(screen, time, dt)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()