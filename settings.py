import pygame


class Settings():
    """Klasa przeznaczona do przechowywania wszystkich ustawień gry"""

    
    def __init__(self):
        """Inicjalizacja ustawień gry"""
        #Ustawienia ekranu
        self.screen_width = 800
        self.screen_height = 500
        self.bg_color = (230, 230, 255)
        self.bg_image = pygame.image.load("images/bg5.jpg")
        self.bg_image = pygame.transform.scale(
            self.bg_image,(self.screen_width, self.screen_height))

        #Ustawienia statku
        self.ship_limit = 3

        #ustawienia pocisku
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 120, 60)
        self.bullets_allowed = 3

        #ustawienia obcego
        self.fleet_drop_speed = 10
        #Wartość fleet_direction = 1 ruch w PRAWO, a -1 W LEWO
        self.fleet_direction = 1

        #Łatwa zmiana szybkości gry
        self.speedup_scale = 0.8

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """"Inicjalizacja ustawień, które ulegają zmianie w trakcie gry."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        
    def increase_spped(self):
        """Zmiana ustawień dotycząca szybości"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale