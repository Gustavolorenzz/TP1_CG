import pygame
from color_picker import Color

class Menu:
    def __init__(self, screen, screen_width, screen_height, menu_width):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu_width = menu_width
        self.x = 20
        self.y = 50
        self.cp = Color(self.x,self.y,self.menu_width-20,20)
        self.button_image = pygame.image.load('arrow-left-square.svg')
        self.button_image = pygame.transform.scale(self.button_image, (100, 40))
        self.button_rect1 = self.button_image.get_rect(topleft=(20, 100))
        self.button_rect2 = self.button_image.get_rect(topleft=(20, 100))
        self.button_active = False
        self.mouse_pos_text = ""
        
        # Define as cores
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.LIGHT_BLUE = (173, 216, 230)
        self.YELLOW = (255, 255, 0)
        self.CYAN = (0, 255, 255)
        self.MAGENTA = (255, 0, 255)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (128, 0, 128)
        self.BROWN = (165, 42, 42)
        self.PINK = (255, 192, 203)
        self.LIGHT_GREEN = (144, 238, 144)

        self.buttons = []
        for i in range(7):
            button_rect = self.button_image.get_rect(topleft=(20, 100 + i * 50))
            self.buttons.append(button_rect)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button_rect in enumerate(self.buttons):
                    if button_rect.collidepoint(event.pos):
                        if i == 0:
                            self.button_active = True
                            self.buttons[1].active = False
                        elif i == 1:
                            self.button_active = False
                            self.buttons[0].active = False
                        else:
                            self.buttons[i].active = not self.buttons[i].active
            self.mouse_pos_text = f"X: {event.pos[0]}, Y: {event.pos[1]}"

    def draw_menu(self):
        pygame.draw.rect(self.screen, self.GRAY, (0, 0, self.menu_width, self.screen_height))
        font = pygame.font.Font(None, 36)
        text = font.render('Menu', True, self.BLACK)
        self.screen.blit(text, (10, 10))
        
        self.cp.update()
        self.cp.draw(self.screen)
        pygame.draw.rect(self.screen, self.GREEN if self.button_active else self.RED, self.button_rect1)
        
        button_label = font.render("Ativar", True, self.BLACK)
        self.screen.blit(button_label, (self.button_rect1.x+5, self.button_rect1.y+5))

        pos_text = font.render(self.mouse_pos_text, True, self.BLACK)
        self.screen.blit(pos_text, (20, 150))
    