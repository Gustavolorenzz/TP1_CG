import pygame
import sys
import numpy as np

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

class Interface:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Paint")
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(WHITE)
        self.font = pygame.font.SysFont('Arial', 20)
        self.loop = True
        self.meu_vetor = []
    def Botao():
        print("Botao")
    def inicialize_tela(self):
        while self.loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for i,j in self.meu_vetor:
                        print(i,j)
                    self.loop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event)
                    if event.button == 1:
                        x,y = pygame.mouse.get_pos()
                        pygame.draw.circle(self.screen, RED, (x, y), 5)
                        self.meu_vetor.append((x, y))
                        print(x,y)
                if len(self.meu_vetor) > 1:
                    for i in range(len(self.meu_vetor)-1):
                        x1, y1 = self.meu_vetor[i]
                        x2, y2 = self.meu_vetor[i+1]
                        reta = Reta(x1, y1, x2, y2)
                        reta.draw(self.screen, RED)
                    reta = Reta(self.meu_vetor[0][0],self.meu_vetor[0][1],self.meu_vetor[i+1][0], self.meu_vetor[i+1][1])
                    reta.draw(self.screen, RED)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.meu_vetor = []
                        self.screen.fill(WHITE)
                    
            pygame.display.update()
            pygame.display.flip()
        pygame.quit()

class Botao:
    def __init__(self, x, y, width, height, color, texts, functions):
        self.font = pygame.font.SysFont('Arial', 20)
        self.buttons = []
        for i, text in enumerate(texts):
            button_text = self.font.render(text, True, BLACK)
            button_rect = pygame.Rect(x, y + i * (height + 10), width, height)
            self.buttons.append((button_text, button_rect, functions[i]))
        self.color = color

    def draw(self, surface):
        for button_text, button_rect, _ in self.buttons:
            pygame.draw.rect(surface, self.color, button_rect)
            surface.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for _, button_rect, function in self.buttons:
                if button_rect.collidepoint(mouse_pos):
                    function()

class Reta:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
    def draw(self, surface, color):
        dx = abs(self.x2 - self.x1)
        dy = abs(self.y2 - self.y1)
        sx = 1 if self.x1 < self.x2 else -1
        sy = 1 if self.y1 < self.y2 else -1
        err = dx - dy
        while True:
            surface.set_at((self.x1, self.y1), color)
            if self.x1 == self.x2 and self.y1 == self.y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                self.x1 += sx
            if e2 < dx:
                err += dx
                self.y1 += sy
    

if __name__ == "__main__":
    interface = Interface()
    interface.inicialize_tela()




