import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Spaceship
ship_width = 50
ship_height = 50
ship_x = SCREEN_WIDTH // 2 - ship_width // 2
ship_y = SCREEN_HEIGHT - 60
ship_speed = 5

# Asteroids
asteroid_width = 40
asteroid_height = 40
asteroid_speed = 5
asteroid_spawn_rate = 30  # Lower value means more frequent
asteroids = []

# Bullets
bullet_width = 5
bullet_height = 10
bullet_speed = 10
bullets = []

# Score
score = 0

# Game loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                # Shoot bullet
                bullets.append({"x": ship_x + ship_width // 2, "y": ship_y})

    if not game_over:
        # Move spaceship
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ship_x > 0:
            ship_x -= ship_speed
        if keys[pygame.K_RIGHT] and ship_x < SCREEN_WIDTH - ship_width:
            ship_x += ship_speed

        # Update bullets
        bullets = [{"x": b["x"], "y": b["y"] - bullet_speed} for b in bullets if b["y"] > 0]

        # Spawn asteroids
        if random.randint(1, asteroid_spawn_rate) == 1:
            asteroids.append({"x": random.randint(0, SCREEN_WIDTH - asteroid_width), "y": 0})

        # Update asteroids
        asteroids = [{"x": a["x"], "y": a["y"] + asteroid_speed} for a in asteroids]

        # Check for bullet-asteroid collisions
        new_asteroids = []
        for asteroid in asteroids:
            hit = False
            for bullet in bullets:
                if (bullet["x"] >= asteroid["x"] and bullet["x"] <= asteroid["x"] + asteroid_width and
                        bullet["y"] >= asteroid["y"] and bullet["y"] <= asteroid["y"] + asteroid_height):
                    bullets.remove(bullet)  # Remove bullet after hitting asteroid
                    hit = True
                    score += 10  # Increase score when asteroid is destroyed
                    break
            if not hit:
                new_asteroids.append(asteroid)
        asteroids = new_asteroids

        # Check for ship-asteroid collisions
        for asteroid in asteroids:
            if (asteroid["x"] < ship_x + ship_width and
                    asteroid["x"] + asteroid_width > ship_x and
                    asteroid["y"] < ship_y + ship_height and
                    asteroid["y"] + asteroid_height > ship_x):
                game_over = True
                break

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (ship_x, ship_y, ship_width, ship_height))  # Draw ship
        for bullet in bullets:
            pygame.draw.rect(screen, RED, (bullet["x"], bullet["y"], bullet_width, bullet_height))  # Draw bullets
        for asteroid in asteroids:
            pygame.draw.rect(screen, WHITE,
                             (asteroid["x"], asteroid["y"], asteroid_width, asteroid_height))  # Draw asteroids

        # Draw the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))  # Display score in the top-left corner

    if game_over:
        # Display "Game Over" message and final score
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

        final_score_text = pygame.font.Font(None, 36).render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score_text, text_rect.move(0, 60))  # Display final score under "Game Over"

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(60)

pygame.quit()
