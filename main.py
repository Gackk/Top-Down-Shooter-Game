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
player = Medium()

# Main Loop

running = True
while running:
    screen.fill(WHITE)

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_a]:
        dx = -1
    if keys[pygame.K_d]:
        dx = 1
    if keys[pygame.K_w]:
        dy = -1
    if keys[pygame.K_s]:
        dy = 1
    player.move(dx, dy)

# Keep player within bounds

    if player.x < 0:
        player.x = 0
    if player.y < 0:
        player.y = 0
    if player.x > WIDTH - 20:
        player.x = WIDTH - 20
    if player.y > HEIGHT - 20:
        player.y = HEIGHT - 20

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle button clicks based on screen
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
        screen.fill(BLACK)
        if isinstance(player, Light):
         pygame.draw.circle(screen, CYAN, (player.x, player.y), 15)
        elif isinstance(player, Medium):
         pygame.draw.rect(screen, GREEN, (player.x, player.y, 20, 20))
        elif isinstance(player, Heavy):
         points = [
            (player.x, player.y - 15),  # top
            (player.x - 15, player.y + 15),  # bottom-left
            (player.x + 15, player.y + 15)   # bottom-right
        ]
         pygame.draw.polygon(screen, YELLOW, points)
    pygame.display.flip()
    clock.tick(60)
