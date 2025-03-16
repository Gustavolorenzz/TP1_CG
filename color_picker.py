import pygame

class Color:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w - 20, h)  # Ajusta a largura para não ultrapassar o limite do menu
        self.image = pygame.Surface((w - 20, h))
        self.image.fill((200, 200, 200))
        self.rad = h // 2
        self.pwidth = w - self.rad * 2 - 20
        for i in range(self.pwidth):
            color = pygame.Color(0)
            color.hsla = (int(360 * i / self.pwidth), 100, 50, 100)
            pygame.draw.rect(self.image, color, (i + self.rad, h // 3, 1, h - 2 * h // 3))
        self.p = 0

    def get_color(self):
        color = pygame.Color(0)
        color.hsla = (int(self.p * 360), 100, 50, 100)
        return color

    def update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = max(0, min(self.p, 1))

    def draw(self, surf):
        surf.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surf, self.get_color(), center, self.rect.height // 2)