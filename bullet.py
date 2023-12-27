import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Klasa przeznaczona do zarządzania pociskami wystrzeliwanymi przez statek"""

    
    def __init__(self, ai_game):
        """Utworzenie obiektu pocisku w aktualnym położeniu statku"""

        super().__init__()
        
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #utworzenie prostokąta w punkcie (0,0), a następnie 
        #zdefiniowanie dla niego odpowiedniego położenia
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        #Położenie pocisku jest zdefiniowanie za pomocą wartości zmiennoprzcinkowej
        self.y = float(self.rect.y)
        
        #self.image = pygame.Surface(self.rect.size)
        #self.image.fill(self.color)
        
    def update(self):
        #uaktualnienie położenia pocisku
        self.y -= self.settings.bullet_speed
        #uaktualnienie położenia prostokąta pocisku
        self.rect.y = self.y

    def draw_bullet(self):
        """Wyświetlanie pocisku na ekranie"""
        pygame.draw.rect(self.screen, self.color, self.rect)