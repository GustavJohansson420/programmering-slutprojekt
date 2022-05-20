import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

clock = pygame.time.Clock()
FPS = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Prebens Äventyr')

tile_size = 30
game_over = 0
main_menu = True

Bakgrund_Himmel = pygame.image.load('bilder/Bakgrund_Himmel.png')
restart_img = pygame.image.load('bilder/Börja_Om.png')
start_img = pygame.image.load('bilder/Start.png')
quit_img = pygame.image.load('bilder/Quit.png')

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        screen.blit(self.image, self.rect)

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
    
        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 3

        if game_over == 0:

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 4
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 4
                self.counter += 1
                self.direction = 1
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -13
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right [self.index]
                if self.direction == -1:
                    self.image = self.images_left [self.index]
            if key[pygame.K_LEFT] == True and key[pygame.K_RIGHT] == True:
                self.counter = 0
                self.index = 0
                self.image = self.images_right[self.index]

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right [self.index]
                if self.direction == -1:
                    self.image = self.images_left [self.index]

            self.vel_y += 1
            if self.vel_y > 7:
                self.vel_y = 7
            dy += self.vel_y

            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height): 
                    dx = 0           
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            if pygame.sprite.spritecollide(self, DevilShit_group, False):
                game_over = -1
            
            if pygame.sprite.spritecollide(self, Spikar_group, False):
                game_over = -1

            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 30:
                self.rect.y -= 3

        
        screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f'bilder/Gubbe{num}.png')
            img_right = pygame.transform.scale(img_right, (24, 48))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('bilder/Död_Gubbe.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

class World():
    def __init__(self, data):
        self.tile_list = []
        Gräs_Block = pygame.image.load('bilder/Gräs_Block.png')
        Jord_Block = pygame.image.load('bilder/Jord_Block.png')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(Gräs_Block, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(Jord_Block, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    DevilShit = Enemy(col_count * tile_size, row_count * tile_size + 11)
                    DevilShit_group.add(DevilShit)
                if tile == 4:
                    Spikar = Spikes(col_count * tile_size, row_count * tile_size)
                    Spikar_group.add(Spikar)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bilder/DevilShit.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 29:
            self.move_direction *= -1
            self.move_counter *= -1

class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bilder/Spikar.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

world_data = [
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 2, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 4, 4, 4, 1, 2, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 3, 0, 2, 2, 2, 1, 1, 1, 2, 2, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2,],
[2, 1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 3, 0, 0, 0, 3, 0, 1, 1, 4, 4, 2, 4, 4, 4, 4, 2,],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2,],
]

player = Player(60, screen_height - 198)
DevilShit_group = pygame.sprite.Group()
Spikar_group = pygame.sprite.Group()
world = World(world_data)
restart_buttom = Button(screen_width // 2 - 85, screen_height // 2, restart_img)
start_button = Button(screen_width // 2 - 110, screen_height // 2 - 130, start_img)
quit_button = Button(screen_width // 2 - 95, screen_height // 2, quit_img)

run = True
while run:

    clock.tick(FPS)

    screen.blit(Bakgrund_Himmel, (0, 0))

    if main_menu == True:
        if quit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()
        if game_over == 0:
            DevilShit_group.update()

        DevilShit_group.draw(screen)
        Spikar_group.draw(screen)
        game_over = player.update(game_over)

        if game_over == -1:
            if restart_buttom.draw():
                player.reset(60, screen_height - 198)
                game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                run = False


    pygame.display.update()

pygame.quit()