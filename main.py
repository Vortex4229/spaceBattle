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
UFOs = []
explosions = []


class Explosion:
    def __init__(self, position, boss=False):
        self.position = position
        self.images = [pygame.image.load(f"explosion{i}.png") for i in range(1, 4)]
        if boss:
            self.images = [pygame.transform.scale(image, (400, 400)) for image in self.images]
        else:
            self.images = [pygame.transform.scale(image, (200, 200)) for image in self.images]
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
        if self.lives == 0:
            explosions.append(Explosion(self.player_position))
            self.dead = True
            self.player_position = pygame.Vector2(1000, 1000)
            self.hitbox = pygame.Rect(self.player_position.x + 26, self.player_position.y + 30, 50, 38)
        else:
            self.lives -= 1


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
        self.enemy_lasers.append(
            screen.blit(self.enemy_laser, (self.enemy_position.x - 100, self.enemy_position.y + 3)))

    def explode(self):
        explosions.append(Explosion(self.enemy_position))


class Boss:
    def __init__(self, lives):
        self.enemy_position = pygame.Vector2(800, 300)
        self.lives = lives

        self.boss_ship = pygame.image.load("ufo.png")
        self.boss_ship = pygame.transform.scale(self.boss_ship, (300, 300))
        self.boss_laser = pygame.image.load("enemy_laser.png")
        self.boss_laser = pygame.transform.scale(self.boss_laser, (200, 180))
        #self.hitbox = pygame.Rect(self.enemy_position.x + 5, self.enemy_position.y + 35, 90, 37)
        self.boss_dead = False

        self.boss_lasers = []

        screen.blit(self.boss_ship, self.enemy_position)
        
    def move(self):
        self.enemy_position.x -= 2
        if self.enemy_position.x < 0:
            player.lives = 0
            player.explode()

    def draw(self):
        screen.blit(self.boss_ship, self.enemy_position)

    def shoot(self):
        self.boss_lasers.append(
            screen.blit(self.boss_laser, (self.enemy_position.x - 100, self.enemy_position.y + 3)))

    def explode(self):
        explosions.append(Explosion(self.enemy_position, boss=True))
        self.boss_dead = True

create_min = 3000
create_max = 5000
shoot_max = 3000

UFO_CREATE = pygame.USEREVENT + 1
UFO_SHOOT = pygame.USEREVENT + 2
BULLET_GET = pygame.USEREVENT + 3

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
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 40))
    bullets_text = font.render(f"Bullets: {player.bullets}", True, (255, 255, 255))
    screen.blit(bullets_text, (10, 70))

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

                if score % 10 == 0:
                    if create_min > 1000:
                        create_min -= 500
                    if create_max > 1000:
                        create_max -= 500
                    if shoot_max > 1000:
                        shoot_max -= 500
                    pygame.time.set_timer(UFO_CREATE, random.randint(create_min, create_max))
                    pygame.time.set_timer(UFO_SHOOT, random.randint(1000, shoot_max))

                break

    for ufo in UFOs:
        for laser in ufo.enemy_lasers:
            enemy_laser_rect = pygame.Rect(laser.x + 35, laser.y + 40, 35, 14)
            # pygame.draw.rect(screen, (255, 0, 0), enemy_laser_rect, 2)
            ufo_rect = pygame.Rect(ufo.enemy_position.x + 5, ufo.enemy_position.y + 35, 90, 37)
            # pygame.draw.rect(screen, (255, 0, 0), ufo_rect, 2)
            if enemy_laser_rect.colliderect(player.hitbox):
                ufo.enemy_lasers.remove(laser)
                player.explode()

    for ufo in UFOs:
        ufo_rect = pygame.Rect(ufo.enemy_position.x + 5, ufo.enemy_position.y + 35, 90, 37)
        # pygame.draw.rect(screen, (255, 0, 0), ufo_rect, 2)
        if player.hitbox.colliderect(ufo_rect):
            UFOs.remove(ufo)
            player.explode()

    for explosion in explosions:
        explosion.update()
        screen.blit(explosion.image, explosion.rect)

    if player.dead and len(explosions) == 0:
        game_over_text = large_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over_text, (280, 300))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
