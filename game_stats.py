import pygame

class GameStats:
    """Monitorowanie danych statystycznych"""

    def __init__(self, ai_game):
        """Inicjalizacja danych statystcznych"""
        self.settings = ai_game.settings
        self.reset_stats()

        #Uruchomienie gry "Inwazja Obcych" w stanie aktywnym
        self.game_active = False

    def reset_stats(self):
        """Inicjalizacja danych statystycznych, które mogą zmienić się w trakcie gry"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        
        