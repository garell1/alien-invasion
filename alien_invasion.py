import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry."""

    def __init__(self):
        """Inicjalizacji gry i utworzenie jej zasobów"""
        pygame.init()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        #self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
        #pygame.display.toggle_fullscreen()
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Inwazja obcych")

        #Utworzenie egzemplarza przechowującego dane statystycze gry
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

        self._create_fleet()

        #Utworzenie przycisku Gra
        self.play_button = Button(self, "Graj")

    
    def run_game(self):
        """Rozpoczęcie pętli głownej gry."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self.clock.tick(300)
            self._update_screen()

    def _check_events(self):
        """Reakacja na zdarzenia generowane przez klawiaturę i mysz"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Rozpoczęcie nowej gry po kliknięciu przycisku Gra przez użytkownika."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #wyzerowanie danych statystycznych gry
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            #Ususnięcie zawartości listy aliens i bullets
            self.aliens.empty()
            self.bullets.empty()

            #Utworzenie nowej floty i wyśrodkowanie statku
            self._create_fleet()
            self.ship.center_ship()

            #Ukrycie kursora myszy
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Utworzenie nowego pocisku i dodanie go do grupy pocisków"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Uaktualnienie położenia pocisków i usunięcie tych niewidocznych na ekranie"""
        #uaktualnienie położenia pocisków
        self.bullets.update()
        #usunięcie pocisków, które znajdują się poza ekraniem
        #rysowanie pocisków na ekranie
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):            
        #Sprawdzenie, czy którykolwiek pocisk trafił obcego. Jeżeli tak, usuwamy zarówno pocisk, jak i obcego
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Pozbycie się istniejących pocisków i utworzenie nowej floty
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_spped()

    def _ship_hit(self):
        """Reakcja na uderzenie obcego statku"""
        if self.stats.ship_left > 0:
            #Zmieniejszenie wartości przechowywanej w ship_left
            self.stats.ship_left -= 1

            #Usunięcie zawartości list aliens i bullets
            self.aliens.empty()
            self.bullets.empty()
            
            #Utworzenie nowej floty i wyśrodkowanie statku
            self._create_fleet()
            self.ship.center_ship()
    
            #Pauza
            sleep(1.0)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Uaktualnienie położenia wszystkich obcych we flocie"""
        self._check_fleet_edges()
        self.aliens.update()

        #Wykrywanie kolizji między obcymi i statkiem
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Wyszukiwanie obcych docierających do dolnej krawędzi ekranu
        self._check_aliens_bottom()
    
    def _create_fleet(self):
        """Utworzenie pełnej floty obcych"""
        #utworzenie obcego
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - 
                             ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
    def _create_alien(self, alien_number, row_number):
            """Utworzenie obcego i umieszczenie go w rzędzie"""
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien_height + 2 * alien_height * row_number
            self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu"""
        for alien in self.aliens.sprites():
            if alien.check_edges(): 
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Przesunięcie całej floty w dól i zmiana kierunku, w którym się ona
        porusza"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Sprawdzanie, czy którykolwiek obcy dotarł do dolnej krawędzi ekranu"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #tak samo jak w przypadku zderzenia statku z obcym
                self._ship_hit()
                break

    def _update_screen(self):
        """Uaktualnieni obrazów na ekranie i przejście do nowego ekranu"""
        #self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.settings.bg_image, (0,0))
        self.ship.blitme()
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #Wyświetlanie informacji o punktacji
        self.sb.show_score() 
        #Wyświetlanie przycisku tylko wtedy, gdy gra jest nieaktywna
        if not self.stats.game_active:
            self.play_button.draw_button() 
        #wyświetlenie ostatnio zmodyfikowanego ekranu
        pygame.display.flip()
        
if __name__ == '__main__':
    #Utworzenie egzemplarza gry i jej uruchomienie
    ai = AlienInvasion()
    ai.run_game()