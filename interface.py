import pygame
import sys
from menu import Menu



class Interface():
    def __init__(self):
        # Inicializa o pygame
        pygame.init()
        # Define as dimensões da tela
        self.screen_width = 800
        self.screen_height = 600
        self.menu_width = 200
        # Cria a tela
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # Nomeia tela
        pygame.display.set_caption('Interface com Menu')

        # Define as cores
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BLACK = (0, 0, 0)

        # Variáveis de controle
        self.offset_x = self.screen_width // 2
        self.offset_y = self.screen_height
        self.zoom = 1

        # Posição do clique
        self.click_position = (0, 0)
        self.click_positions = []

        self.menu = Menu(self.screen, self.screen_width, self.screen_height, self.menu_width)

    def draw_quadro(self):
        quadro_width = self.screen_width - self.menu_width
        pygame.draw.rect(self.screen, self.WHITE, (self.menu_width, 0, quadro_width, self.screen_height))
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] > self.menu_width:
                        position = (event.pos[0] - self.menu_width, event.pos[1])
                        self.click_positions.append(position)
                        print(f"Posição clicada: {position}")
                

            # Limpa a tela
            self.screen.fill(self.WHITE)

            # Desenha o menu
            self.menu.draw_menu()

            # Desenha o quadro
            self.draw_quadro()

            # Atualiza a tela
            pygame.display.flip()

        # Encerra o pygame
        pygame.quit()
        sys.exit()

# Cria uma instância da interface e executa
if __name__ == "__main__":
    interface = Interface()
    interface.run()
        

