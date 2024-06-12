import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PlanetSimulator")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Body:
    def __init__(self, x, y, vx, vy, mass, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.color = color
        self.path = [(self.x, self.y)]

    # 가속도 계산
    def calculate_gravity(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist == 0:
            return 0, 0
        force = (self.mass * other.mass) / (dist**2)
        angle = math.atan2(dy, dx)
        ax = force * math.cos(angle) / self.mass
        ay = force * math.sin(angle) / self.mass
        return ax, ay

    # 위치 속도 업데이트
    def update(self, dt, bodies):
        ax_total = 0
        ay_total = 0
        for body in bodies:
            if body != self:
                ax, ay = self.calculate_gravity(body)
                ax_total += ax
                ay_total += ay
        self.vx += ax_total * dt
        self.vy += ay_total * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.path.append((self.x, self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), math.log10(self.mass) * 3)
        pygame.draw.lines(screen, self.color, False, self.path, 1)

# 물체 생성
num_bodies = int(input("Enter the number of bodies: "))

bodies = []
colors = [RED, GREEN, BLUE]
for i in range(num_bodies):
    print(f"Enter details for body {i + 1}:")
    x = int(input(f"x(0 ~ {WIDTH}): "))
    y = int(input(f"y(0 ~ {HEIGHT}): "))
    vx = float(input("vx: "))
    vy = float(input("vy: "))
    mass = int(input("mass: "))
    color = colors[i % len(colors)]
    bodies.append(Body(x, y, vx, vy, mass, color))

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for body in bodies:
        body.update(0.1, bodies)
        body.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
