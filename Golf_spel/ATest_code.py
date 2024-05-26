import pygame
import sys
import math

class Ball:
    def __init__(self, position, radius):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = "white"
        self.velocity = pygame.math.Vector2(0, 0)

    def move(self, bunkers):
        self.position += self.velocity
        self.velocity *= 0.97  # Friction effect

        # Check if the ball is in a bunker
        for bunker in bunkers:
            if bunker.rect.collidepoint(self.position):
                self.velocity *= 0.5  # Slow down the ball

        if self.velocity.length() < 0.1:  # Stop the ball completely if velocity is very low
            self.velocity = pygame.math.Vector2(0, 0)

class Object:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Bunker:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (210, 180, 140)  # Sand color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def create_hole(screen, x, y, radius):
    pygame.draw.circle(screen, BLACK, (x, y), radius)

def draw_distance_line(screen, ball_position, mouse_position):
    distance = ball_position.distance_to(mouse_position)
    if distance > 200:
        line_color = (255, 0, 0)
    elif distance > 100:
        line_color = (255, 165, 0)
    else:
        line_color = (0, 255, 0)
    pygame.draw.line(screen, line_color, ball_position, mouse_position, 2)

def collision(ball, width, height):
    if ball.position.x - ball.radius <= 0 or ball.position.x + ball.radius >= width:
        ball.velocity.x *= -1
    if ball.position.y - ball.radius <= 0 or ball.position.y + ball.radius >= height:
        ball.velocity.y *= -1

def object_collision(ball, objects):
    for obj in objects:
        if ball.position.y + ball.radius >= obj.rect.top and ball.position.y <= obj.rect.top:
            if obj.rect.left <= ball.position.x <= obj.rect.right:
                ball.position.y = obj.rect.top - ball.radius
                ball.velocity.y *= -1
        elif ball.position.y - ball.radius <= obj.rect.bottom and ball.position.y >= obj.rect.bottom:
            if obj.rect.left <= ball.position.x <= obj.rect.right:
                ball.position.y = obj.rect.bottom + ball.radius
                ball.velocity.y *= -1
        elif ball.position.x + ball.radius >= obj.rect.left and ball.position.x <= obj.rect.left:
            if obj.rect.top <= ball.position.y <= obj.rect.bottom:
                ball.position.x = obj.rect.left - ball.radius
                ball.velocity.x *= -1
        elif ball.position.x - ball.radius <= obj.rect.right and ball.position.x >= obj.rect.right:
            if obj.rect.top <= ball.position.y <= obj.rect.bottom:
                ball.position.x = obj.rect.right + ball.radius
                ball.velocity.x *= -1

def display_shot_count(screen, font, shot_count):
    shot_text = font.render(f"Shots: {shot_count}", True, WHITE)
    screen.blit(shot_text, (10, 10))

pygame.init()

WIDTH, HEIGHT = 1400, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Golf Game')
background_img = pygame.image.load("Golf_spel/map.png")

ball_image = pygame.image.load("Golf_spel/Golf_Ball.png")
ball_radius = 15
ball_image = pygame.transform.scale(ball_image, (2 * ball_radius, 2 * ball_radius))

golf_ball = Ball(pygame.Vector2(1200, 700), ball_radius)

objects = [
    Object(70, 50, 1300, 30),   # Övre ram 
    Object(70, 50, 30, 700 ),  # Vänster ram 
    Object(1340, 70, 30, 700),   # höger ram 
    Object(70, 740, 1300, 30),  # nedre ram 
    Object(600, 500, 300, 100), # object på Banan 1 
    Object(700, 600, 30, 150),  # object på banan 2 
    Object(600, 200, 300, 100)
]

# Define bunkers
bunkers = [
    Bunker(300, 400, 100, 50),
    Bunker(800, 300, 150, 75)
]

hole_x, hole_y = 200, 700
hole_radius = 17

dragging = False
drag_start_pos = None

font = pygame.font.Font(None, 36)
shot_count = 0  # Initialize shot counter

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if golf_ball.velocity.length() == 0 and golf_ball.position.distance_to(mouse_pos) <= ball_radius:
                dragging = True
                drag_start_pos = mouse_pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                mouse_pos = pygame.mouse.get_pos()
                drag_direction = pygame.Vector2(mouse_pos) - pygame.Vector2(drag_start_pos)
                velocity_magnitude = min(drag_direction.length() * 0.1, 35)
                golf_ball.velocity = drag_direction.normalize() * -velocity_magnitude
                shot_count += 1  # Increment shot counter

    golf_ball.move(bunkers)
    collision(golf_ball, WIDTH, HEIGHT)
    object_collision(golf_ball, objects)

    if math.hypot(golf_ball.position.x - hole_x, golf_ball.position.y - hole_y) <= hole_radius:
        popup_text = font.render("Congratulations! You win! you made it in " f"Shots: {shot_count}" , True, WHITE)
        popup_rect = popup_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        popup_bg_rect = pygame.Rect(popup_rect.left - 10, popup_rect.top - 10, popup_rect.width + 20, popup_rect.height + 20)
        
        # Draw the background rectangle
        pygame.draw.rect(screen, BLACK, popup_bg_rect)
        
        # Draw the popup text
        screen.blit(popup_text, popup_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    screen.blit(background_img, (0, 0))
    ball_rect = ball_image.get_rect(center=golf_ball.position)
    screen.blit(ball_image, ball_rect)
    
    for obj in objects:
        obj.draw(screen)
    
    for bunker in bunkers:
        bunker.draw(screen)
        screen.blit(ball_image, ball_rect)
        
    create_hole(screen, hole_x, hole_y, hole_radius)
    display_shot_count(screen, font, shot_count)  # Display the shot count

    if dragging:
        mouse_pos = pygame.mouse.get_pos()
        draw_distance_line(screen, golf_ball.position, mouse_pos)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
