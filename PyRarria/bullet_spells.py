import pygame
import random
from settings import *
from spritesheet import *
from items.item import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.sheet = SpriteSheet(SPELL_SHEETS["collision_explosion"], 10, 6, 60)
        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.position = pos + (self.sheet.shift[4][0], self.sheet.shift[4][1])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.start = pygame.time.get_ticks()
        self.frame = 0

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[cell_index])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        if self.frame == 56:
            self.kill()

        self.draw(self.frame)
        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.position.x + main_stage_position.x
        self.rect.y = self.position.y + main_stage_position.y


class BulletSpell(pygame.sprite.Sprite):
    """Super class for spells"""

    def __init__(self, game, name, damage):
        self.groups = game.magics
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.damage = damage + PLAYER_VALUES["DAMAGE"]

    def check_collision(self):
        # Detekcja kolizji z przeciwnikami
        hits = pygame.sprite.spritecollide(self, self.game.all_creatures, False)
        if hits:
            for hit in hits:
                hit.hit(self, self.damage)
            self.explode()

        # Detekcja kolizji ze środowiskiem
        hits = pygame.sprite.spritecollide(self, Item.get_neighbours(self.position, (5, 5), self.game.grid), False)
        if hits:
            self.explode()

    def explode(self):
        """Make explosion after colliding with object (should override)"""
        self.kill()


# Klasa zaklęcia fireball, czyli lecący ognisty pocisk
class Fireball(BulletSpell):
    def __init__(self, game, pos, speed_y, direction):
        super().__init__(game, "fireball", 50)
        if direction == 1:
            self.sheet = SpriteSheet(SPELL_SHEETS["fireball_right"], 8, 8, 64)
        else:
            self.sheet = SpriteSheet(SPELL_SHEETS["fireball_left"], 8, 8, 64)

        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.frame = random.randint(0, 63)
        self.position = pos
        self.rect = self.image.get_rect()
        self.speed_x = 3
        self.speed_y = speed_y
        self.accuracy = 0.95
        self.direction = direction
        self.duration = 4000
        self.start = pygame.time.get_ticks()

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[int(cell_index)])
        self.frame += 1

    # Sprawdzanie czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.kill()

        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.position.x + main_stage_position.x
        self.rect.y = self.position.y + main_stage_position.y
        self.position.x += self.speed_x * self.direction
        self.rect.x += self.speed_x * self.direction
        self.position.y += self.speed_y
        self.rect.y += self.speed_y

        if self.frame == 64:
            self.frame = 0

        self.draw(self.frame)
        self.check_collision()

    def explode(self):
        vect = pygame.math.Vector2(self.position.x, self.position.y)
        if self.direction == 1:
            vector = pygame.math.Vector2(self.position[0] + 50, self.position[1] + 10)
            new_explosion = Explosion(self.game, vector)
        else:
            vector = pygame.math.Vector2(self.position[0], self.position[1] + 10)
            new_explosion = Explosion(self.game, vector)

        self.game.explosions.add(new_explosion)
        self.kill()


# Klasa zaklęcia frostbullet, czyli lecący lodowy pocisk
class FrostBullet(BulletSpell):
    def __init__(self, game, pos, speed_y, direction):
        super().__init__(game, "frostbullet", 50)
        if direction == 1:
            self.sheet = SpriteSheet(SPELL_SHEETS["frostbullet_right"], 8, 1, 8)
        else:
            self.sheet = SpriteSheet(SPELL_SHEETS["frostbullet_left"], 8, 1, 8)

        self.image = pygame.Surface((self.sheet.cell_width, self.sheet.cell_height), pygame.SRCALPHA).convert_alpha()
        self.position = pos
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed_x = 3
        self.speed_y = speed_y
        self.accuracy = 0.95
        self.direction = direction
        self.duration = 3000
        self.start = pygame.time.get_ticks()
        self.frame = 0

    # Rysowanie kolejnej klatki tego efektu
    def draw(self, cell_index):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet.sheet, (0, 0), self.sheet.cells[int(cell_index)])
        self.frame += 1

    # Sprawdzanie, czy czas trwania upłynął, aktualizacja pozycji
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start > self.duration:
            self.kill()

        main_stage_position = self.game.get_main_stage_position()
        self.rect.x = self.position.x + main_stage_position.x
        self.rect.y = self.position.y + main_stage_position.y
        self.position.x += self.speed_x * self.direction
        self.rect.x += self.speed_x * self.direction
        self.position.y += self.speed_y
        self.rect.y += self.speed_y

        if self.frame == 8:
            self.frame = 0

        self.draw(self.frame)
        self.check_collision()
