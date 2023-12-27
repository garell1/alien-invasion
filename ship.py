import pygame


class Ship():
    """Klasa przeznaczona do zarządaniem stakiem kosmicznym"""

    def __init__(self, ai_game):
        """Inicjalizacja staku kosmicznego i jego położenie początkowe"""
        self.screen = ai_game.screen #1
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() #2
        
        #Wczytanie obrazu statku kosmicznego
        self.image = pygame.image.load("images/space_ship.png") #3
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()

        #Każdy nowy statek kosmiczny pojawia się na dole ekranu
        self.rect.midbottom = self.screen_rect.midbottom #4

        #Opcje wskazujące na poruszanie się statku
        self.moving_right = False
        self.moving_left = False

        #Położenie poziomu statku jest przechowywane w postaci liczby zmiennoprzecinkowej.
        self.x = float(self.rect.x)


    def update(self):
        """Uaktualnienienie położenia staku na podstawie opcji wskazującej na jego ruch"""
        #uaktualnienie wartości współrzędnych X statku, a nie jego prostokata
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            
        self.rect.x = self.x

    def blitme(self):
        """Wyświetlanie statku kosmicznego w jego aktualnym położeniu."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Umieszczenie statku na środku przy dolnej krawędzi ekranu."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)