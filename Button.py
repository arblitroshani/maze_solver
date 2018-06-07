import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, text, color):
        super(Button, self).__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont('Arial', 25)

    def show(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h])
        screen.blit(self.font.render(self.text, True, (255, 255, 255)), (self.x + 25, self.y + 10))

