import pygame
import sys
import math

# Ball class is in Ball.py file
from Ball import Ball

def draw_distance_line(screen, ball_position, mouse_position):
    # Define colors based on distance
    distance = ball_position.distance_to(mouse_position)
    if distance > 200:
        line_color = (255, 0, 0)  # Red
    elif distance > 100:
        line_color = (255, 165, 0)  # Orange
    else:
        line_color = (0, 255, 0)  # Green
    
    # Draw the line
    pygame.draw.line(screen, line_color, ball_position, mouse_position, 2)

def collision(ball, border_pos_x, border_pos_y):
    # Check left and right borders
    if ball.position.x - ball.radius <= 0 or ball.position.x + ball.radius >= border_pos_x:
        ball.velocity.x *= -1  # Reverse horizontal velocity
    
    # Check top and bottom borders
    if ball.position.y - ball.radius <= 0 or ball.position.y + ball.radius >= border_pos_y:
        ball.velocity.y *= -1  # Reverse vertical velocity

def create_borders(screen, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    

def create_hole(screen, x, y, radius):
    pygame.draw.circle(screen, (0, 0, 0), (x, y), radius)

pygame.init()  # Initialize pygame

# --------variables---------
WIDTH, HEIGHT = 1400, 800
BORDER_WIDTH = 20
BORDER_HEIGHT = 30

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
# ----------stop variables--------

# ---------screen info ---------
# Define the background colour
# using RGB color coding.
background_colour = (0, 255, 0)
# Define the dimensions of
# screen object(width,height)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Set the caption of the screen
pygame.display.set_caption('Golf Game')
# Fill the background colour to the screen
screen.fill(background_colour)
# Update the display using flip
pygame.display.flip()
# ----------Screen info stop----------

# Load ball image
ball_image = pygame.image.load("Golf_spel\Golf_Ball.png")  # Replace "ball_image.png" with the path to your image
ball_radius = 15
ball_image = pygame.transform.scale(ball_image, (2 * ball_radius, 2 * ball_radius))

# Create a Golf Ball instance
golf_ball = Ball(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), ball_radius)

# Create hole coordinates and radius
hole_x, hole_y = 200, 700
hole_radius = 17

# Flag to indicate if the ball is currently being dragged
dragging = False

running = True

# Variables to store the start position of the drag
drag_start_pos = None

# Font settings
font = pygame.font.Font(None, 36)

# game loop
while running:

    for event in pygame.event.get():
        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()
            # Check if mouse click is within the ball's bounding rectangle
            if golf_ball.position.distance_to(mouse_pos) <= ball_radius:
                dragging = True
                drag_start_pos = mouse_pos  # Store the start position of the drag

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                mouse_pos = pygame.mouse.get_pos()
                # Calculate the direction of the drag
                drag_direction = pygame.Vector2(mouse_pos[0] - drag_start_pos[0], mouse_pos[1] - drag_start_pos[1]) * -1
                # Calculate the velocity based on the distance of the drag
                velocity_magnitude = min(drag_direction.length() * 0.1, 35)  # Adjust multiplier and maximum velocity
                golf_ball.velocity = drag_direction.normalize() * velocity_magnitude

    # Border collisions
    collision(golf_ball, WIDTH, HEIGHT)

    # Check if the ball enters the hole
    if math.sqrt((golf_ball.position.x - hole_x) ** 2 + (golf_ball.position.y - hole_y) ** 2) <= hole_radius:
        # Display a pop-up message
        popup_text = font.render("Congratulations! You win!", True, (255, 255, 255))
        popup_rect = popup_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(popup_text, popup_rect)
        pygame.display.flip()
        # Wait for a moment before exiting or moving to the next level
        pygame.time.delay(2000)
        # Close the game window
        running = False

    # Clear the screen
    screen.fill(background_colour)

    # Draw borders
    create_borders(screen, BLACK, WIDTH // 2 - 350, 150, BORDER_WIDTH, BORDER_HEIGHT)

    # Draw the ball
    ball_rect = ball_image.get_rect(center=golf_ball.position)
    golf_ball.move()
    screen.blit(ball_image, ball_rect)

    # Draw the hole
    create_hole(screen, hole_x, hole_y, hole_radius)

    # Draw distance line from ball to mouse position only when dragging
    if dragging:
        mouse_pos = pygame.mouse.get_pos()
        draw_distance_line(screen, golf_ball.position, mouse_pos)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
