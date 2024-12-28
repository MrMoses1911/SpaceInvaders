import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Bruno Bortoletto")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 30)  # Default font, size 36

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 60
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(80, 200)
        self.speed = 2

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.speed *= -1
            self.rect.y += 30

# Sprite groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create aliens
for _ in range(10):
    alien = Alien()
    all_sprites.add(alien)
    aliens.add(alien)

# Game variables
shots_fired = 0
aliens_eliminated = 0
game_over = False
win = False

# Function to display text on the screen
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Game loop
running = True
while running:
    # Keep the loop running at the right speed
    clock.tick(60)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
                shots_fired += 1  # Increment shots fired

    # Update
    all_sprites.update()

    # Check for collisions between bullets and aliens
    hits = pygame.sprite.groupcollide(aliens, bullets, True, True)

    for hit in hits:
        aliens_eliminated += 1  # Increment aliens eliminated

    # Check if all aliens are defeated
    if len(aliens) == 0:
        game_over = True
        win = True
        running = False

    # Check for collisions between player and aliens
    if pygame.sprite.spritecollide(player, aliens, False):
        game_over = True
        win = False
        running = False

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display shots fired and aliens eliminated
    draw_text(f"Shots Fired: {shots_fired}", RED, 10, 10)
    draw_text(f"Aliens Eliminated: {aliens_eliminated}", RED, 10, 50)

# Display win/lose message
    if game_over:
        if win:
            draw_text("You Win! Congratulations!", GREEN, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
            draw_text("Press Enter to Exit the Game", WHITE, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50)
        else:
            draw_text("Game Over! You were hit by an alien!", RED, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2)
            draw_text("Press Enter to Exit the Game", WHITE, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50)

        pygame.display.flip()

        # Wait for the player to press Enter
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_input = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Enter key
                        waiting_for_input = False
                        running = False

    # Flip the display
    pygame.display.flip()

# Quit the game
pygame.quit()