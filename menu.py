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

    def draw_menu(self):
        pygame.draw.rect(self.screen, self.GRAY, (0, 0, self.menu_width, self.screen_height))
        font = pygame.font.Font(None, 36)
        text = font.render('Menu', True, self.BLACK)
        self.screen.blit(text, (10, 10))
        
        self.cp.update()
        self.cp.draw(self.screen)