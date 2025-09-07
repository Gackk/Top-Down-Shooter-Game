import pygame
import random

pygame.init()

# =====================
# --- Base Classes ---
# =====================
class Character:
    def __init__(self, name, health, speed):
        self.name = name
        self.health = health
        self.speed = speed
        self.x = 300
        self.y = 300
        self.weapon = None

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def set_weapon(self, weapon):
        self.weapon = weapon

class Light(Character):
    def __init__(self):
        super().__init__("Light", health=50, speed=5)

class Medium(Character):
    def __init__(self):
        super().__init__("Medium", health=75, speed=3)

class Heavy(Character):
    def __init__(self):
        super().__init__("Heavy", health=100, speed=2)

# =====================
# --- Enemy Classes ---
# =====================
class Enemy:
    def __init__(self, name, health, speed):
        self.name = name
        self.health = health
        self.speed = speed
        self.x = random.randint(50, 550)
        self.y = random.randint(50, 430)

class SmallMonster(Enemy):
    def __init__(self):
        super().__init__("Small Monster", health=20, speed=2)

class Monster(Enemy):
    def __init__(self):
        super().__init__("Monster", health=50, speed=1)

class Boss(Enemy):
    def __init__(self):
        super().__init__("Boss", health=200, speed=0.5)

# =====================
# --- Weapon Classes ---
# =====================
class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

class Sword(Weapon):
    def __init__(self):
        super().__init__("Sword", damage=10)

class Pistol(Weapon):
    def __init__(self):
        super().__init__("Pistol", damage=5)

class MachineGun(Weapon):
    def __init__(self):
        super().__init__("Machine Gun", damage=3)

# =====================
# --- Game Setup ---
# =====================
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Class Structure Example")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

clock = pygame.time.Clock()

# Player (you can change to Light(), Medium(), Heavy())
player = Light()
player.set_weapon(Sword())

# One enemy for demo
enemy = SmallMonster()

# =====================
# --- Game Loop ---
# =====================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_a:]:
        dx = -1
    if keys[pygame.K_d]:
        dx = 1
    if keys[pygame.K_w]:
        dy = -1
    if keys[pygame.K_s]:
        dy = 1
    player.move(dx, dy)

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, (player.x, player.y, 20, 20))  # Player
    pygame.draw.rect(screen, RED, (enemy.x, enemy.y, 20, 20))      # Enemy

    # Display text (character + weapon)
    font = pygame.font.SysFont(None, 24)
    info = f"{player.name} | HP Gael: {player.health} | Weapon: {player.weapon.name}"
    text_surface = font.render(info, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
