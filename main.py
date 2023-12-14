import pygame
import random

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Battle")
pygame.display.set_icon(pygame.image.load("ufo.png"))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
score = 0

player_lasers = []
UFOs = []
explosions = []

class Explosion:
    def __init__(self, position):
        self.position = position
        self.images = [pygame.image.load(f"explosion{i}.png") for i in range(1, 4)]
        self.images = [pygame.transform.scale(image, (200, 200)) for image in self.images]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center = position)
        self.rect = self.rect.move(+50, +50)
        self.framecount = 0

    def update(self):
        self.framecount += 1
        if self.framecount % 20 == 0:
            self.index += 1
            if self.index >= len(self.images):
                explosions.remove(self)
            else:
                self.image = self.images[self.index]

class Player:
    def __init__(self):
        self.player_position = pygame.Vector2(50, 300)
        self.lives = 2

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

    def explode(self):
        if self.lives == 0:
            return True
        else:
            self.lives -= 1
            return False


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
        explosions.append(Explosion(self.enemy_position))

UFO_CREATE = pygame.USEREVENT + 1
UFO_SHOOT = pygame.USEREVENT + 2

pygame.time.set_timer(UFO_CREATE, random.randint(3000, 5000))
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

    lives_text = font.render(f"Lives: {player.lives + 1}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 40))

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

    for ufo in UFOs:
        for laser in ufo.enemy_lasers:
            laser.x -= 7
            if laser.x < 0:
                ufo.enemy_lasers.remove(laser)
            else:
                screen.blit(ufo.enemy_laser, laser)

    for laser in player_lasers:
        laser_rect = pygame.Rect(laser.x + 35, laser.y + 40, 35, 14)
        # pygame.draw.rect(screen, (255, 0, 0), laser_rect, 2)
        for ufo in UFOs:
            ufo_rect = pygame.Rect(ufo.enemy_position.x + 5, ufo.enemy_position.y + 35, 90, 37)
            # pygame.draw.rect(screen, (255, 0, 0), ufo_rect, 2)
            if laser_rect.colliderect(ufo_rect):
                player_lasers.remove(laser)
                ufo.explode()
                UFOs.remove(ufo)
                score += 1
                break

    player_rect = pygame.Rect(player.player_position.x + 26, player.player_position.y + 30, 50, 38)
    # pygame.draw.rect(screen, (255, 0, 0), player_rect, 2)

    for ufo in UFOs:
        for laser in ufo.enemy_lasers:
            enemy_laser_rect = pygame.Rect(laser.x + 35, laser.y + 40, 35, 14)
            # pygame.draw.rect(screen, (255, 0, 0), enemy_laser_rect, 2)
            ufo_rect = pygame.Rect(ufo.enemy_position.x + 5, ufo.enemy_position.y + 35, 90, 37)
            # pygame.draw.rect(screen, (255, 0, 0), ufo_rect, 2)
            if enemy_laser_rect.colliderect(player_rect):
                ufo.enemy_lasers.remove(laser)
                if player.explode() == True:
                    running = False

    for ufo in UFOs:
        ufo_rect = pygame.Rect(ufo.enemy_position.x + 5, ufo.enemy_position.y + 35, 90, 37)
        # pygame.draw.rect(screen, (255, 0, 0), ufo_rect, 2)
        if player_rect.colliderect(ufo_rect):
            UFOs.remove(ufo)
            if player.explode() == True:
                running = False

    for explosion in explosions:
        explosion.update()
        screen.blit(explosion.image, explosion.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

