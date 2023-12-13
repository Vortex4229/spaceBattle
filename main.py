import pygame
import random

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Battle")
clock = pygame.time.Clock()

player_lasers = []
UFOs = []

explosion1 = pygame.image.load("explosion1.png")
explosion1 = pygame.transform.scale(explosion1, (100, 100))
explosion2 = pygame.image.load("explosion2.png")
explosion2 = pygame.transform.scale(explosion2, (100, 100))
explosion3 = pygame.image.load("explosion3.png")
explosion3 = pygame.transform.scale(explosion3, (100, 100))

class Player:
    def __init__(self):
        self.player_position = pygame.Vector2(50, 300)
        self.lives = 3

        self.ship_idle = pygame.image.load("spaceship_idle.png")
        self.ship_idle = pygame.transform.scale(self.ship_idle, (100, 100))
        self.ship_active = pygame.image.load("spaceship_active.png")
        self.ship_active = pygame.transform.scale(self.ship_active, (100, 100))
        self.player_laser = pygame.image.load("player_laser.png")
        self.player_laser = pygame.transform.scale(self.player_laser, (100, 90))
        self.moving = False

        screen.blit(self.ship_idle, self.player_position)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_position.y -= 5
            self.moving = True
        elif keys[pygame.K_s]:
            self.player_position.y += 5
            self.moving = True
        else:
            self.moving = False


    def draw(self):
        if self.moving:
            screen.blit(self.ship_active, self.player_position)
        else:
            screen.blit(self.ship_idle, self.player_position)

    def shoot(self):
        player_lasers.append(screen.blit(self.player_laser, (self.player_position.x, self.player_position.y + 3)))


class Ufo:
    def __init__(self):
        self.enemy_position = pygame.Vector2(800, random.randint(100, 500))

        self.enemy_ship = pygame.image.load("ufo.png")
        self.enemy_ship = pygame.transform.scale(self.enemy_ship, (100, 100))
        self.enemy_laser = pygame.image.load("enemy_laser.png")
        self.enemy_laser = pygame.transform.scale(self.enemy_laser, (100, 90))

        self.enemy_lasers = []

        screen.blit(self.enemy_ship, self.enemy_position)

    def move(self):
        self.enemy_position.x -= 2
        if self.enemy_position.x < 0:
            UFOs.remove(self)

    def draw(self):
        screen.blit(self.enemy_ship, self.enemy_position)

    def shoot(self):
        self.enemy_lasers.append(screen.blit(self.enemy_laser, (self.enemy_position.x - 100, self.enemy_position.y + 3)))

    def explode(self):

        screen.blit(explosion1, (self.enemy_position.x, self.enemy_position.y))
        pygame.time.delay(100)
        screen.blit(explosion2, (self.enemy_position.x, self.enemy_position.y))
        pygame.time.delay(100)
        screen.blit(explosion3, (self.enemy_position.x, self.enemy_position.y))

UFO_CREATE = pygame.USEREVENT + 1
pygame.time.set_timer(UFO_CREATE, random.randint(3000, 5000))

UFO_SHOOT = pygame.USEREVENT + 2
pygame.time.set_timer(UFO_SHOOT, random.randint(1000, 3000))


player = Player()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            player.shoot()
        if event.type == UFO_CREATE:
            UFOs.append(Ufo())
        if event.type == UFO_SHOOT:
            if UFOs:
                random.choice(UFOs).shoot()

    screen.fill((0, 0, 0))

    player.move()
    player.draw()

    for ufo in UFOs:
        ufo.move()
        ufo.draw()

    for laser in player_lasers:
        laser.x += 7
        if laser.x > 800:
            player_lasers.remove(laser)
        else:
            screen.blit(player.player_laser, laser)

    for laser in player_lasers:
        laser_rect = pygame.Rect(laser.x, laser.y, 100, 90)
        for ufo in UFOs:
            ufo_rect = pygame.Rect(ufo.enemy_position.x, ufo.enemy_position.y, 100, 100)
            if laser_rect.colliderect(ufo_rect):
                player_lasers.remove(laser)
                ufo.explode()
                UFOs.remove(ufo)
                break

    for ufo in UFOs:
        for laser in ufo.enemy_lasers:
            laser.x -= 7
            if laser.x < 0:
                ufo.enemy_lasers.remove(laser)
            else:
                screen.blit(ufo.enemy_laser, laser)



    pygame.display.flip()
    clock.tick(60)
