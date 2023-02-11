import random
import pygame as pg
from record_syst import RecordSystem
from pygame import mixer

mixer.init()

# Load the audio effects
crash = pg.mixer.Sound('sounds/sound_crash_explosion.mp3')
crash.set_volume(0.3)
pg.mixer.music.load('sounds/bg_music_01.mp3')
pg.mixer.music.set_volume(0.2)
pg.mixer.music.play(-1, 0, 2000)


class Asteroid(pg.sprite.Sprite):
    # Creates an instance of Asteroid
    def __init__(self, x, y):
        super().__init__()
        self.speed = random.randint(3, 5)  # Sets a random speed
        # Sets a random image
        self.image = random.choice([pg.image.load('images/asteroid_01.png').convert_alpha(),
                                    pg.image.load('images/asteroid_02.png').convert_alpha()])
        self.size = random.uniform(0.05, 0.15)  # Sets a random size
        self.image = pg.transform.scale(self.image, (self.image.get_width()*self.size, self.image.get_height()*self.size))
        self.rect = self.image.get_rect(topleft=(x, y))

    # Paints the SpaceShip on the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # Moves the asteroid to the left
    def update(self, ship):
        # Move the asteroid to the left. If its off the screen, kill it and add the score to the player
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            if ship.lives > 0:
                ship.points += 5
            self.kill()


class Spaceship(pg.sprite.Sprite):
    # Creates an instance of SpaceShip
    def __init__(self, x, y):
        super().__init__()
        self.speed = 3  # Sets up the speed
        self.size = 0.1  # Size of the spaceship on screen
        # Load the spaceship images
        self.spaceship_images = [pg.image.load('images/spaceship_straight.png').convert_alpha(),
                                 pg.image.load('images/spaceship_down.png').convert_alpha(),
                                 pg.image.load('images/spaceship_up.png').convert_alpha(),
                                 pg.image.load('images/spaceship_explosion.png').convert_alpha()]

        for x in range(0, len(self.spaceship_images)):  # Resize all images
            self.spaceship_images[x] = pg.transform.scale(self.spaceship_images[x], (
                self.spaceship_images[x].get_width()*self.size, self.spaceship_images[x].get_height()*self.size))

        self.image = self.spaceship_images[0]  # Set the image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.lives = 3
        self.points = 0
        # Use mask for more accurate collisions
        self.mask = pg.mask.from_surface(self.image)
        self.control_ship = True  # When player has no control of ship
        self.flip = False

    # Moves the SpaceShip up and down within a limit
    def move(self):
        key_status = pg.key.get_pressed()
        if key_status[pg.K_UP] and self.rect.y > 20:
            self.image = self.spaceship_images[2]
            self.rect.y -= self.speed
        elif key_status[pg.K_DOWN] and self.rect.y < 580:
            self.image = self.spaceship_images[1]
            self.rect.y += self.speed
        else:
            self.image = self.spaceship_images[0]

    # Paints the SpaceShip on the screen
    def draw(self, screen):
        screen.blit(pg.transform.flip(self.image, self.flip, False), self.rect)

    def update(self, asteroids):
        if self.lives <= 0:
            self.lives = 0
            self.image = self.spaceship_images[3]
        # Player can control the spaceship if it has more >= 1 life
        if self.lives >= 1 and self.control_ship:
            self.move()
        if pg.sprite.spritecollide(self, asteroids, True, pg.sprite.collide_mask):
            if self.lives > 0:
                crash.play()  # Sound of the crashing spaceship
            self.lives -= 1

# Planet class
class Planet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = 12  # Set the size of the planet on the screen
        self.speed = 2  # Set the speed at which the planet moves towards the player
        self.image = pg.image.load(f'images/planet_0{random.randint(1,4)}.png') # Random image for the planet
        self.image = pg.transform.scale(self.image, (self.image.get_width()*self.size, self.image.get_height()*self.size))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pg.mask.from_surface(self.image)

    # Draw the planet
    def draw(self, display):
        display.blit(self.image, self.rect)

    # Update the planet status
    def update(self, ship):
        # Stop moving the planet if it collides with the player
        if self.rect.colliderect(ship.rect):
            self.speed = 0
        else:
            self.rect.x -= self.speed
