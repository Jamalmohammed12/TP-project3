import pygame

# class GolfBall(pygame.sprite.Sprite):
#  def __init__(self):
#         super().__init__()
#         self.image = pygame.Surface((20, 20))
#         self.image.fill(255, 255, 255)
#         self.rect = self.image.get_rect()
#         self.rect.center = (WIDTH // 2, HEIGHT // 2)
#         self.velocity = pygame.math.Vector2(0, 0)





class Ball:
    def __init__(self, position, radius) -> None:
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = "white"
        self.velocity = pygame.math.Vector2(0, 0)

    def move(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

        self.velocity.x = self.velocity.x*0.97
        self.velocity.y = self.velocity.y*0.97






