import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Klasa przedstawiającego pojedyńczego obcego we flocie""" 
    
    def __init__(self, ai_game):
        """Inicjalizacja obcego i zdefiniowanie jego położenia początkowego"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Wczytanie obrazu obcego i zdefiniowanie jego atrybutów rect
        self.alien_width = 40
        self.alien_height = 33
        self.image = pygame.image.load('images/enemy.png')
        self.image = pygame.transform.scale(self.image, (self.alien_width, self.alien_height))
        self.rect = self.image.get_rect()
        
        #Wczytywanie obrazu obcego w pobliżu lewego górnego rogu ekranu
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #przechowywanie dokładnego poziomego położenia obcego
        self.x = float(self.rect.x)
    def check_edges(self):
        """Zwraca wartość True, jeśli obcy znajduje się przy krawędzi ekranu."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Przsuniecie obcego w prawo lub w lewo"""
        self.x += (self.settings.alien_speed *
                    self.settings.fleet_direction)
        self.rect.x = self.x
