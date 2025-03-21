import pygame
import sys
import numpy as np

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
        self.estrutura = []
        self.poligonos = []
        self.cor = RED
        self.poligono = ""
        self.modo_atual = ""
        self.state = False
        self.selecao_inicio = None
        self.obj_selected = []
    
    

    def desenhar_reta(self):
        # Será chamado quando o botão "Reta" for clicado
        if not self.state:
            print("Modo: Reta selecionado")
            self.poligono = "reta"

    def desenhar_circulo(self):
        # Será chamado quando o botão "Círculo" for clicado
        if not self.state:
            print("Modo: Círculo selecionado")
            self.poligono = "circulo"
        
    def modo_dda(self):
        # Será chamado quando o botão "DDA" for clicado
        if not self.state:
            print("Algoritmo: DDA selecionado")
            self.modo_atual = "DDA"
        
    def modo_bresenham(self):
        # Será chamado quando o botão "Bresenham" for clicado
        if not self.state:
            print("Algoritmo: Bresenham selecionado")
            self.modo_atual = "Bresenham"
    
    def handle_event(self):
        if self.modo_atual == "DDA"  and self.poligono == "reta":
            if len(self.meu_vetor) > 1:
                for i in range(len(self.meu_vetor) - 1):
                    x1, y1 = self.meu_vetor[i]
                    x2, y2 = self.meu_vetor[i + 1]
                    reta = Reta(x1, y1, x2, y2)
                    reta.drawDDA(self.screen, self.cor)
                if len(self.meu_vetor) > 2:    
                    reta = Reta(self.meu_vetor[-1][0], self.meu_vetor[-1][1], self.meu_vetor[0][0], self.meu_vetor[0][1])
                    reta.drawDDA(self.screen, self.cor)
                self.estrutura.append(self.meu_vetor)
                self.poligonos.append("retaDDA")
                self.meu_vetor = []
            else:
                print("É necessário ter mais de 1 ponto para desenhar uma reta")
        elif self.modo_atual == "Bresenham" and self.poligono == "reta":
            if len(self.meu_vetor) > 1:
                for i in range(len(self.meu_vetor) - 1):
                    x1, y1 = self.meu_vetor[i]
                    x2, y2 = self.meu_vetor[i + 1]
                    reta = Reta(x1, y1, x2, y2)
                    reta.drawBreseham(self.screen, self.cor)
                if len(self.meu_vetor) > 2:
                    reta = Reta(self.meu_vetor[-1][0], self.meu_vetor[-1][1], self.meu_vetor[0][0], self.meu_vetor[0][1])
                    reta.drawBreseham(self.screen, self.cor)
                self.estrutura.append(self.meu_vetor)
                self.poligonos.append("retaBresenham")
                self.meu_vetor = []

            else:
                print("É necessário ter mais de 1 ponto para desenhar uma reta")
        elif self.poligono == "circulo":
            if len(self.meu_vetor) == 2:
                x1, y1 = self.meu_vetor[0]
                x2, y2 = self.meu_vetor[1]
                circulo = Circulo(x1, x2, y1, y2)
                circulo.draw(self.screen, self.cor)
                self.estrutura.append(self.meu_vetor)
                self.poligonos.append("circulo")
                self.meu_vetor = []
            else:
                print("É necessário ter apenas 2 pontos para desenhar um círculo")
        self.poligono = ""


    def inicialize_tela(self):
        #adiciona os botoes
        botao = Botao(10, 10, 150, 30, GRAY, 
                     ["Reta", "Circunferência", "DDA", "Bresenham"], 
                     [self.desenhar_reta, self.desenhar_circulo, self.modo_dda, self.modo_bresenham])
        while self.loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    m=0
                    for estrutura in self.estrutura:
                        for i, j in estrutura:
                            print(i, j)
                        print(self.poligonos[m])
                        m+=1
                        print("-----")  # Separador entre elementos de self.estrutura
                    self.loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and botao.handle_event(event):
                        
                        x, y = pygame.mouse.get_pos()
                        pygame.draw.circle(self.screen, RED, (x, y), 3)
                        self.meu_vetor.append((x, y))
                        print(f"Ponto adicionado:{x}, {y}")
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not(botao.handle_event(event)):
                    self.handle_event()
                #funcao limpar tela(tela e retas)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.meu_vetor = []
                        self.estrutura = []
                        self.poligonos = []
                        self.screen.fill(WHITE)
            #desenha os botoes
            botao.draw(self.screen)
            
            pygame.display.update()
            pygame.display.flip()
        pygame.quit()

class Botao:
    def __init__(self, x, y, width, height, color, texts, functions):
        self.font = pygame.font.SysFont('Arial', 16)
        self.buttons = []
        for i, text in enumerate(texts):
            button_text = self.font.render(text, True, BLACK)
            button_rect = pygame.Rect(x, y + i * (height + 5), width, height)
            self.buttons.append((button_text, button_rect, functions[i], False))
        self.color = color
        self.highlight_color = (min(color[0] + 50, 255), 
                               min(color[1] + 50, 255), 
                               min(color[2] + 50, 255))
    
    def draw(self, surface):
        for button_text, button_rect, _, is_active in self.buttons:
            current_color = self.highlight_color if is_active else self.color
            pygame.draw.rect(surface, current_color , button_rect)
            pygame.draw.rect(surface, BLACK, button_rect, 1)  # Borda
            text_rect = button_text.get_rect(center=button_rect.center)
            surface.blit(button_text, text_rect)

    def handle_event(self, event):
        mouse_pos = event.pos
        for i, (_, button_rect, function, _) in enumerate(self.buttons):
            if button_rect.collidepoint(mouse_pos):
                if i > 1:
                    self.buttons = [(text, rect, func, False) for text, rect, func, _ in self.buttons]
                    self.buttons[i] = (self.buttons[i][0], self.buttons[i][1], self.buttons[i][2], True)
                function()  # Call the function directly, not through event
                return False
        return True

class Circulo:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.raio = int(np.sqrt((self.x2-self.x1)**2 + (self.y2-self.y1)**2))

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
                surface.set_at((x, y), color)
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
                surface.set_at((x, y), color)     

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




