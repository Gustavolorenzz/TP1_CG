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

    def Botao(self):
        print("Botaoooooo")

    def inicialize_tela(self):
        #adiciona os botoes
        botao = Botao(10, 10, 50, 20, GRAY, ["Botao"], [self.Botao])
        while self.loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for i, j in self.meu_vetor:
                        print(i, j)
                    self.loop = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        botao.handle_event(event)
                        x, y = pygame.mouse.get_pos()
                        pygame.draw.circle(self.screen, RED, (x, y), 5)
                        self.meu_vetor.append((x, y))
                        print(x, y)
                # DDA(retas) - funcao de desenhar retas a partir do vetor de pontos self.meu_vetor
                if len(self.meu_vetor) > 1:
                    for i in range(len(self.meu_vetor) - 1):
                        x1, y1 = self.meu_vetor[i]
                        x2, y2 = self.meu_vetor[i + 1]
                        reta = Reta(x1, y1, x2, y2)
                        reta.drawDDA(self.screen, RED)
                    reta = Reta(self.meu_vetor[0][0], self.meu_vetor[0][1], self.meu_vetor[i + 1][0], self.meu_vetor[i + 1][1])
                    reta.drawDDA(self.screen, RED)
                #Bresenham(retas)
                '''if len(self.meu_vetor) > 1:
                    for i in range(len(self.meu_vetor) - 1):
                        x1, y1 = self.meu_vetor[i]
                        x2, y2 = self.meu_vetor[i + 1]
                        reta = Reta(x1, y1, x2, y2)
                        reta.drawDDA(self.screen, RED)
                    reta = Reta(self.meu_vetor[0][0], self.meu_vetor[0][1], self.meu_vetor[i + 1][0], self.meu_vetor[i + 1][1])
                    reta.drawDDA(self.screen, RED)'''
                #funcao limpar tela(tela e retas)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.meu_vetor = []
                        self.screen.fill(WHITE)
            #desenha os botoes
            botao.draw(self.screen)
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
            surface.blit(button_text, (button_rect.x + 3, button_rect.y))

    def handle_event(self, event):
        mouse_pos = event.pos
        for _, button_rect, function in self.buttons:
            if button_rect.collidepoint(mouse_pos):
                function()  # Call the function directly, not through event
class Circulo:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.raio = np.sqrt((self.x2-self.x1)**2 + (self.y2-self.y1)**2)

    def plotaSimetricos(self, surface, x, y, color):
        surface.set_at((x + self.x1, y + self.y1), color)
        surface.set_at((-x + self.x1, y + self.y1), color)
        surface.set_at((x + self.x1, -y + self.y1), color)
        surface.set_at((-x + self.x1, -y + self.y1), color)
        surface.set_at((y + self.x1, x + self.y1), color)
        surface.set_at((-y + self.x1, x + self.y1), color)
        surface.set_at((y + self.x1, -x + self.y1), color)
        surface.set_at((-y + self.x1, -x + self.y1), color)

    def draw(self, surface, color):
        x, y, p = 0, self.raio, 3-2*self.raio
        self.plotaSimetricos(surface, x, y, color)
        while x < y:#2° OCTANTE
            x += 1
            if p < 0:
                p += 4*x + 6
            else:
                y -= 1
                p += 4*(x-y) + 10
            self.plotaSimetricos(surface, x, y, color)
        

        

class Reta:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def drawBreseham(self, surface, color):
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        x, y = self.x1, self.y1
        surface.set_at((int(np.round(x)), int(np.round(y))), color)
        if(dx>0):
            xInc = 1
        else:
            xInc = -1
            dx = -dx
        if(dy>0):
            yInc = 1
        else:
            yInc = -1
            dy = -dy
        if dx > dy:#1° CASO
            p = 2*dy-dx
            c1 = 2*dy
            c2 = 2*(dy-dx)
            for i in range(dx):
                x += xInc
                if p < 0:
                    p += c1
                else:
                    y += yInc
                    p += c2
                surface.set_at(x, y, color)
        else:#2° CASO
            p = 2*dx-dy
            c1 = 2*dx
            c2 = 2*(dx-dy)
            for i in range(dy):
                y += yInc
                if p < 0:
                    p += c1
                else:
                    x += xInc
                    p += c2
                surface.set_at(x, y, color)        

        
    def drawDDA(self, surface, color):
        dx = float(self.x2 - self.x1)
        dy = float(self.y2 - self.y1)
        x, y = float(self.x1), float(self.y1)
        
        if abs(dx) > abs(dy):
            steps = abs(dx)
        else:
            steps = abs(dy)
        xInc = dx / steps
        yInc = dy / steps
        for i in range(int(steps)):
            x += xInc
            y += yInc
            surface.set_at((int(np.round(x)), int(np.round(y))), color)
        
    

if __name__ == "__main__":
    interface = Interface()
    interface.inicialize_tela()




