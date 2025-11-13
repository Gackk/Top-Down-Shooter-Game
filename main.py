print(" RIGHt NOWWWWWWW YOU ARE Running:", __file__)

import pygame
import sys

pygame.init()

#   Setup

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top down shooter")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

small_font = pygame.font.SysFont(None, 20)
medium_font = pygame.font.SysFont(None, 40)
large_font = pygame.font.SysFont(None, 80)
clock = pygame.time.Clock()

#   World/Room constants
TILE = 32
DOOR_W = WIDTH // 5  # right-edge door is 1/5 of the screen width
SPAWN_POS = (32, HEIGHT // 2 - 10)  # where the player appears each room
ROOM_ORDER = ["spawn", "enemy", "loot", "enemy", "portal"]  # list of the room order

def make_border_walls():
    walls = []
    # top & bottom
    walls.append(pygame.Rect(0, 0, WIDTH, TILE))
    walls.append(pygame.Rect(0, HEIGHT - TILE, WIDTH, TILE))
    # left wall
    walls.append(pygame.Rect(0, 0, TILE, HEIGHT))
    # right wall EXCEPT for door gap
    gap_x = WIDTH - DOOR_W
    # upper part of right wall
    walls.append(pygame.Rect(WIDTH - TILE, 0, TILE, (HEIGHT - DOOR_W) // 2))
    # lower part of right wall
    lower_y = (HEIGHT + DOOR_W) // 2
    walls.append(pygame.Rect(WIDTH - TILE, lower_y, TILE, HEIGHT - lower_y))
    return walls

# door trigger area (open space on the right)
DOOR_TRIGGER = pygame.Rect(WIDTH + 99 - DOOR_W, (HEIGHT - DOOR_W)//2, DOOR_W, DOOR_W)

class RoomData:
    def __init__(self, kind, walls):
        self.kind = kind          # "spawn" | "enemy" | "loot" | "portal"
        self.walls = walls        # list[pygame.Rect]
        self.locked = (kind == "enemy")  # step 1: ignore this, door acts open for now



#   Button Class 

class Button1:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback  # function to call when clicked

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, DARK_GRAY, self.rect)
        else:
            pygame.draw.rect(screen, GRAY, self.rect)

        pygame.draw.rect(screen, BLACK, self.rect, 2)  # border

        text_surface = medium_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


#   Screen Handlers

def main_menu():
    global current_screen
    current_screen = "mainmenu"

def settings_menu():
    global current_screen
    current_screen = "settings"

def game_screen():
    global current_screen
    current_screen = "game"

# Start on the main menu
current_screen = "mainmenu"

# Create buttons
menu_buttons = [
    Button1("Start Game", 220, 150, 200, 50, game_screen),
    Button1("Settings", 220, 220, 200, 50, settings_menu),
    Button1("Quit", 220, 290, 200, 50, sys.exit)
]

settings_buttons = [
    Button1("Back", 220, 350, 200, 50, main_menu)
]

# Character Classes
class Character:
    def rect(self, size=20):
        return pygame.Rect(int(self.x), int(self.y), size, size)

    def try_move(self, dx, dy, walls, size=20):
        # Move X first
        r = self.rect(size)
        r.x += dx * self.speed
        if not any(r.colliderect(w) for w in walls):
            self.x = r.x

        # Then move Y
        r.y = int(self.y) + dy * self.speed
        if not any(r.colliderect(w) for w in walls):
            self.y = r.y
            
    def __init__(self, name, maxhealth, speed):
        self.name = name
        self.maxplayerhealth = maxhealth
        self.health = maxhealth
        self.speed = speed
        self.x = 300
        self.y = 300
# Movement method
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
# Keep character within screen bounds  
    def clamp_position(self, width, height, size=20):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > width - size:
            self.x = width - size
        if self.y > height - size:
            self.y = height - size

class Light(Character):
    def __init__(self):
        super().__init__("Light", maxhealth=50, speed=5)

class Medium(Character):
    def __init__(self):
        super().__init__("Medium", maxhealth=75, speed=3)

class Heavy(Character):
    def __init__(self):
        super().__init__("Heavy",maxhealth=100, speed=2)

# Example player character
player = Heavy()

#   Multi-room state
rooms = [RoomData(k, make_border_walls()) for k in ROOM_ORDER]
current_room_idx = 0

def current_room():
    return rooms[current_room_idx]

# Set player to spawn position for first room
player.x, player.y = SPAWN_POS

# Main Loop

running = True
while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_a]: dx = -1
    if keys[pygame.K_d]: dx = 1
    if keys[pygame.K_w]: dy = -1
    if keys[pygame.K_s]: dy = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if current_screen == "mainmenu":
            for button in menu_buttons:
                button.check_click(event)
        elif current_screen == "settings":
            for button in settings_buttons:
                button.check_click(event)

    # Draw based on current screen
    if current_screen == "mainmenu":
        text_surface = large_font.render("Main Menu", True, BLACK)
        text_rect = text_surface.get_rect(center=(320, 100))
        screen.blit(text_surface, text_rect)
        for button in menu_buttons:
            button.draw(screen)

    elif current_screen == "settings":
        text_surface = medium_font.render("Settings Menu", True, BLACK)
        screen.blit(text_surface, (220, 150))
        for button in settings_buttons:
            button.draw(screen)

    elif current_screen == "game":
        # World background
        screen.fill((40, 40, 40))

        # Move only in game and collide with current room walls
        room = current_room()
        player.try_move(dx, dy, room.walls, size=20)

        # Draw walls
        for w in room.walls:
            pygame.draw.rect(screen, (80, 80, 80), w)
            pygame.draw.rect(screen, (20, 20, 20), w, 2)

        # Draw door area (right-edge window). For Step 1 it's always open.
        pygame.draw.rect(screen, (150, 200, 255), DOOR_TRIGGER, 2)  # outline so it's visible

        # Draw player
        if isinstance(player, Light):
            pygame.draw.circle(screen, CYAN, (int(player.x), int(player.y)), 15)
        elif isinstance(player, Medium):
            pygame.draw.rect(screen, GREEN, (int(player.x), int(player.y), 20, 20))
        elif isinstance(player, Heavy):
            points = [
                (int(player.x), int(player.y) - 15),
                (int(player.x) - 15, int(player.y) + 15),
                (int(player.x) + 15, int(player.y) + 15)
            ]
            pygame.draw.polygon(screen, YELLOW, points)

        # Room transition: if player reaches the door area, go to next room
        player_rect = pygame.Rect(int(player.x), int(player.y), 20, 20)
        if player_rect.colliderect(DOOR_TRIGGER):
            if current_room_idx < len(rooms) - 1:
                current_room_idx += 1
                # reset player near left side
                player.x, player.y = SPAWN_POS
            else:
                # reached end (portal room). For now, loop back to main menu
                current_screen = "mainmenu"

    pygame.display.flip()
    clock.tick(60)
