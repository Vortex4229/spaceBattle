import pygame
import random

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Battle")
pygame.display.set_icon(pygame.image.load("ufo.png"))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
large_font = pygame.font.SysFont("Arial", 50)

score = 0

player_sprite = []
player_lasers = []
enemy_lasers = []
UFOs = []
explosions = []

create_min = 3000
create_max = 5000
shoot_max = 3000

UFO_CREATE = pygame.USEREVENT + 1
UFO_SHOOT = pygame.USEREVENT + 2
BULLET_GET = pygame.USEREVENT + 3

class Explosion:
    def __init__(self, position, size=1):
        self.position = position
        self.images = [pygame.image.load(f"explosion{i}.png") for i in range(1, 4)]
        if size == 1:
            self.images = [pygame.transform.scale(image, (200, 200)) for image in self.images]
        elif size == 2:
            self.images = [pygame.transform.scale(image, (400, 400)) for image in self.images]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=position)
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
        self.laser = pygame.image.load("player_laser.png")
        self.laser = pygame.transform.scale(self.laser, (100, 90))
        self.hitbox = pygame.Rect(self.player_position.x + 26, self.player_position.y + 30, 50, 38)
        self.moving = False
        self.dead = False
        self.bullets = 5

        self.player_ship = screen.blit(self.ship_idle, self.player_position)
        player_sprite.append(self.player_ship)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.player_position.y < 0:
                return
            else:
                self.player_position.y -= 5
                self.moving = True
        elif keys[pygame.K_s]:
            if self.player_position.y > 500:
                return
            else:
                self.player_position.y += 5
                self.moving = True
        else:
            self.moving = False

    def draw(self):
        if not self.dead:
            if self.moving:
                screen.blit(self.ship_active, self.player_position)
                self.hitbox = pygame.Rect(self.player_position.x + 26, self.player_position.y + 30, 50, 38)
                # pygame.draw.rect(screen, (255, 0, 0), player_rect, 2)
            else:
                screen.blit(self.ship_idle, self.player_position)

    def shoot(self):
        if self.bullets == 0:
            return
        else:
            player_lasers.append(
                screen.blit(self.laser, (self.player_position.x + 20, self.player_position.y + 3)))
            self.bullets -= 1

    def explode(self):
        if self.lives <= 0:
            explosions.append(Explosion(self.player_position))
            self.dead = True
            self.player_position = pygame.Vector2(1000, 1000)
            self.hitbox = pygame.Rect(self.player_position.x + 26, self.player_position.y + 30, 50, 38)
        else:
            self.lives -= 1

class Ufo:
    def __init__(self, boss=False, lives=0):
        self.boss = boss

        if self.boss:
            UFOs.clear()

            self.enemy_position = pygame.Vector2(800, 300)
            self.enemy_ship = pygame.image.load("ufo.png")
            self.enemy_ship = pygame.transform.scale(self.enemy_ship, (300, 300))
            self.enemy_laser = pygame.image.load("enemy_laser.png")
            self.enemy_laser = pygame.transform.scale(self.enemy_laser, (100, 90))

            self.boss_active = True
            self.lives = lives
            self.going_up = True
            self.going_down = False
            self.hitbox = pygame.Rect(self.enemy_position.x + 15, self.enemy_position.y + 105, 270, 111)

            pygame.time.set_timer(UFO_SHOOT, random.randint(1000, 1500))
            pygame.time.set_timer(UFO_CREATE, 0)

        else:
            self.enemy_position = pygame.Vector2(800, random.randint(100, 500))
            self.enemy_ship = pygame.image.load("ufo.png")
            self.enemy_ship = pygame.transform.scale(self.enemy_ship, (100, 100))
            self.enemy_laser = pygame.image.load("enemy_laser.png")
            self.enemy_laser = pygame.transform.scale(self.enemy_laser, (100, 90))
            self.hitbox = pygame.Rect(self.enemy_position.x + 5, self.enemy_position.y + 35, 90, 37)

        screen.blit(self.enemy_ship, self.enemy_position)

    def move(self):
        if self.boss:
            self.enemy_position.x -= 1
            if self.enemy_position.y == -100:
                self.going_up = False
                self.going_down = True
            if self.enemy_position.y == 400:
                self.going_up = True
                self.going_down = False

            if self.going_up:
                self.enemy_position.y -= 2
                self.hitbox = pygame.Rect(self.enemy_position.x + 15, self.enemy_position.y + 105, 270, 111)
            if self.going_down:
                self.enemy_position.y += 2
                self.hitbox = pygame.Rect(self.enemy_position.x + 15, self.enemy_position.y + 105, 270, 111)
        else:
            self.enemy_position.x -= 2
            self.hitbox = pygame.Rect(self.enemy_position.x + 5, self.enemy_position.y + 35, 90, 37)

        if not self.boss and self.enemy_position.x < -100 or self.boss and self.enemy_position.x < -300:
            if self.boss:
                player.lives = -1
                player.explode()
            else:
                player.explode()

            UFOs.remove(self)

    def draw(self):
        screen.blit(self.enemy_ship, self.enemy_position)
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def shoot(self):
        if self.boss:
            enemy_lasers.append(screen.blit(self.enemy_laser, (self.enemy_position.x - 30, self.enemy_position.y + 100)))
        else:
            enemy_lasers.append(screen.blit(self.enemy_laser, (self.enemy_position.x - 50, self.enemy_position.y + 3)))

    def explode(self):
        if self.boss:
            if self.lives > 0:
                self.lives -= 1
            else:
                explosions.append(Explosion((self.enemy_position.x + 150, self.enemy_position.y + 150), 2))
                pygame.time.set_timer(UFO_SHOOT, random.randint(1000, shoot_max))
                pygame.time.set_timer(UFO_CREATE, random.randint(create_min, create_max))
                UFOs.remove(self)
        else:
            explosions.append(Explosion(self.enemy_position))
            UFOs.remove(self)

pygame.time.set_timer(UFO_CREATE, random.randint(create_min, create_max))
pygame.time.set_timer(UFO_SHOOT, random.randint(1000, 3000))

UFOs.append(Ufo())
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
            pygame.time.set_timer(BULLET_GET, 1000)
        if event.type == UFO_CREATE:
            UFOs.append(Ufo())
        if event.type == UFO_SHOOT:
            if UFOs:
                random.choice(UFOs).shoot()
        if event.type == BULLET_GET:
            if player.bullets == 5:
                player.bullets = 5
            else:
                player.bullets += 1

    screen.fill((0, 0, 0))

    lives_text = font.render(f"Lives: {player.lives + 1}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    bullets_text = font.render(f"Bullets: {player.bullets}", True, (255, 255, 255))
    screen.blit(bullets_text, (10, 40))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 70))


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
            screen.blit(player.laser, laser)

    for laser in enemy_lasers:
        laser.x -= 7
        if laser.x < -100:
            enemy_lasers.remove(laser)
        else:
            screen.blit(ufo.enemy_laser, laser)

    for laser in player_lasers:
        laser_rect = pygame.Rect(laser.x + 35, laser.y + 40, 35, 14)
        # pygame.draw.rect(screen, (255, 0, 0), laser_rect, 2)
        for ufo in UFOs:
            # pygame.draw.rect(screen, (255, 0, 0), ufo.hitbox, 2)
            if laser_rect.colliderect(ufo.hitbox):
                player_lasers.remove(laser)
                ufo.explode()
                score += 1

                if score % 10 == 0:
                    if create_min > 1000:
                        create_min -= 500
                    if create_max > 1000:
                        create_max -= 500
                    if shoot_max > 1000:
                        shoot_max -= 500
                    pygame.time.set_timer(UFO_CREATE, random.randint(create_min, create_max))
                    pygame.time.set_timer(UFO_SHOOT, random.randint(1000, shoot_max))

                if score % 25 == 0:
                    boss_lives = (score // 25) + 1
                    UFOs.append(Ufo(True, boss_lives))
                    pygame.time.set_timer(UFO_SHOOT, 1000)

    for laser in enemy_lasers:
        enemy_laser_rect = pygame.Rect(laser.x + 35, laser.y + 40, 35, 14)
        # pygame.draw.rect(screen, (255, 0, 0), enemy_laser_rect, 2)
        if enemy_laser_rect.colliderect(player.hitbox):
            enemy_lasers.remove(laser)
            player.explode()

    for ufo in UFOs:
        # pygame.draw.rect(screen, (255, 0, 0), ufo.hitbox, 2)
        if player.hitbox.colliderect(ufo.hitbox):
            player.explode()

    for explosion in explosions:
        explosion.update()
        screen.blit(explosion.image, explosion.rect)

    if player.dead and len(explosions) == 0:
        game_over_text = large_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over_text, (280, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
