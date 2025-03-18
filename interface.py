import pygame
import sys

# Inicializar o pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Dimensões da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
MENU_WIDTH = 150

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu Pygame")

# Fonte
font = pygame.font.SysFont('Arial', 12)

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

class InputField:
    def __init__(self, x, y, width, label, value="XXX"):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20
        self.label = label
        self.value = value
        self.active = False
        self.button = pygame.Rect(x + width - 25, y, 20, 20)
        self.button_color = RED
        self.text_rect = pygame.Rect(x + 75, y, 30, 20)
    
    def draw(self, surface):
        # Desenhar o label
        text = font.render(self.label, True, BLACK)
        surface.blit(text, (self.x, self.y + 5))
        
        # Desenhar o campo de texto
        pygame.draw.rect(surface, WHITE, self.text_rect)
        pygame.draw.rect(surface, BLACK, self.text_rect, 1)
        value_text = font.render(self.value, True, BLACK)
        surface.blit(value_text, (self.x + 80, self.y + 5))
        
        # Desenhar o botão
        pygame.draw.rect(surface, self.button_color, self.button)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Verificar se o botão foi clicado
                if self.button.collidepoint(event.pos):
                    if self.button_color == RED:
                        self.button_color = GREEN
                    else:
                        self.button_color = RED
                    self.active = self.button_color == GREEN
                    return True
                # Verificar se o campo de texto foi clicado
                elif self.text_rect.collidepoint(event.pos):
                    self.active = True
                    return True
                else:
                    self.active = False
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            else:
                # Limitar a entrada a 3 caracteres
                if len(self.value) < 3:
                    self.value += event.unicode
            return True
        return False

class ActionButton:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 1)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.color == GRAY:
                    self.color = GREEN
                else:
                    self.color = GRAY
                self.active = (self.color == GREEN)
                return True
            else:
                self.active = False
        return False

# Função para desenhar o menu lateral
def draw_menu(surface):
    # Área do menu
    pygame.draw.rect(surface, GRAY, (0, 0, MENU_WIDTH, SCREEN_HEIGHT))
    
    # Título do menu
    menu_text = font.render("Menu", True, BLACK)
    surface.blit(menu_text, (10, 10))

def main():
    clock = pygame.time.Clock()
    running = True
    
    # Criar seletor de cores usando a classe Color fornecida
    color_selector = Color(20, 30, MENU_WIDTH, 15)
    
    # Criar campos de entrada com botões
    input_fields = [
        InputField(10, 60, 130, "eixo x:"),
        InputField(10, 85, 130, "eixo y:"),
        InputField(10, 110, 130, "raio:"),
        InputField(10, 135, 130, "largura:"),
        InputField(10, 160, 130, "inclinação:")
    ]
    
    # Criar botões de ação
    action_buttons = [
        ActionButton(20, 195, 110, 25, "Reta"),
        ActionButton(20, 225, 110, 25, "Circunferência"),
        ActionButton(20, 255, 110, 25, "Janela"),
        ActionButton(20, 285, 110, 25, "Inclinar"),
        ActionButton(20, 315, 110, 25, "Limpar")
    ]
    
    while running:
        screen.fill(WHITE)
        
        # Desenhar a área de separação do menu
        draw_menu(screen)
        
        # Atualizar e desenhar o seletor de cores
        color_selector.update()
        color_selector.draw(screen)
        
        # Desenhar os campos de entrada com botões
        for field in input_fields:
            field.draw(screen)
        
        # Desenhar os botões de ação
        for button in action_buttons:
            button.draw(screen)
        
        # Desenhar a área principal (branca)
        pygame.draw.rect(screen, WHITE, (MENU_WIDTH, 0, SCREEN_WIDTH - MENU_WIDTH, SCREEN_HEIGHT))
        
        # Linha divisória entre o menu e a área principal
        pygame.draw.line(screen, BLACK, (MENU_WIDTH, 0), (MENU_WIDTH, SCREEN_HEIGHT), 1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            # Manipular eventos dos campos de entrada
            for field in input_fields:
                field.handle_event(event)
            
            # Manipular eventos dos botões de ação
            for i, button in enumerate(action_buttons):
                if button.handle_event(event):
                    print(f"Botão '{button.text}' foi clicado!")
                    # Funções específicas para cada botão
                    if button.text == "Limpar":
                        # Função para o botão Limpar
                        for field in input_fields:
                            field.value = "XXX"
                    elif button.text == "Reta":
                        # Exemplo de função para desenhar uma reta
                        print("Função para desenhar reta")
                    elif button.text == "Circunferência":
                        # Exemplo de função para desenhar uma circunferência
                        print("Função para desenhar circunferência")
                    elif button.text == "Janela":
                        # Exemplo de função para ajustar a janela
                        print("Função para ajustar janela")
                    elif button.text == "Inclinar":
                        # Exemplo de função para inclinar
                        print("Função para inclinar")
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()