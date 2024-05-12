import pygame
import sys
import math

# Ball class is in Ball.py file
from Ball import Ball

pygame.init()  # Initialize pygame

# --------variables---------
WIDTH, HEIGHT = 1200, 700

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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

# Flag to indicate if the ball is currently being dragged
dragging = False

running = True

# game loop
while running:

    # for loop through the event queue
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
                # Calculate the offset to adjust the ball position while dragging
                offset_x = golf_ball.position.x - mouse_pos[0]
                offset_y = golf_ball.position.y - mouse_pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            mouse_pos = pygame.mouse.get_pos()
            golf_ball.velocity.x = math.cos(math.atan2(offset_y, offset_x))*math.sqrt(offset_x**2+offset_y**2)
            golf_ball.velocity.y = math.sin(math.atan2(offset_y, offset_x))*math.sqrt(offset_x**2+offset_y**2)


       

    # Clear the screen
    screen.fill(background_colour)

    # Draw the ball
    ball_rect = ball_image.get_rect(center=golf_ball.position)
    golf_ball.move()
    screen.blit(ball_image, ball_rect)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
