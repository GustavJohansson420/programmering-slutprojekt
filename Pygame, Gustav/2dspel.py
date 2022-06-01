#inporterar pygame
from turtle import delay
import pygame
from pygame.locals import *
#importerar mixer så vi kan ha ljud
from pygame import mixer

#initierar mixer
mixer.init()

#initierar pygame
pygame.init()

#Gör ints som bestämmer bredden och höjden på spelfönstret
screen_width = 600
screen_height = 600

#Gör så att spelet är i 60fps
clock = pygame.time.Clock()
FPS = 60

#Skapar spelfönstret och ger det ett namn
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Prebens Äventyr')

#Veriabler som bestämmer storleken på en tile, om man lever eller inte, och om man är i main menu eller inte
tile_size = 30
game_over = 0
main_menu = True

#Laddar in bilder
Bakgrund_Himmel = pygame.image.load('bilder/Bakgrund_Himmel.png')
restart_img = pygame.image.load('bilder/Börja_Om.png')
start_img = pygame.image.load('bilder/Start.png')
quit_img = pygame.image.load('bilder/Quit.png')

#Laddar in musik och ljudeffekter samt bestämmer volym
pygame.mixer.music.load('Prebens_Äventyr_Theme_Song.mp3')
pygame.mixer.music.set_volume(0.3)
jump_sound = pygame.mixer.Sound('Hopp.mp3')
jump_sound.set_volume(0.5)
death_sound = pygame.mixer.Sound('Död.mp3')
death_sound.set_volume(0.5)
goal_sound = pygame.mixer.Sound('Goal.mp3')
goal_sound.set_volume(0.3)

#Gör en knapp klass
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #Ritar ut bilden på knappen
        screen.blit(self.image, self.rect)

        #Gör så vi får muspekarens position
        pos = pygame.mouse.get_pos()

        #Gör så man kan trycka på knappen 1 gång
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        #Gör så man kan trycka på knappen igen
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
    
        return action

#Gör en spelare klass
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        #Gör ints till gubbens rörelse
        dx = 0
        dy = 0
        walk_cooldown = 3

        #kollar om man lever eller inte
        if game_over == 0:

            key = pygame.key.get_pressed()
            #Gör så att gubben vänder sig åt vänster och rör sig åt vänster när man håller inne vänster pilen
            if key[pygame.K_LEFT]:
                dx -= 4
                self.counter += 1
                self.direction = -1

            #Gör så att gubben vänder sig åt höger och rör sig åt höger när man håller inne höger pilen 
            if key[pygame.K_RIGHT]:
                dx += 4
                self.counter += 1
                self.direction = 1

            #Gör så att gubben hoppar och spelar ett ljud när man trycker space
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_sound.play()
                self.vel_y = -13
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False

            #Gör så att gubben står still och är vänd åt rätt håll när man inte trycker höger eller vänster pil
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right [self.index]
                if self.direction == -1:
                    self.image = self.images_left [self.index]

            #Gör så att gubben står still och är vänd åt höger om man håller inne både höger och vänster pil
            if key[pygame.K_LEFT] == True and key[pygame.K_RIGHT] == True:
                self.counter = 0
                self.index = 0
                self.image = self.images_right[self.index]

            #Gör så att gubben har en animation när han rör sig
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right [self.index]
                if self.direction == -1:
                    self.image = self.images_left [self.index]

            #Gör så att spelet har gravitation
            self.vel_y += 1
            if self.vel_y > 7:
                self.vel_y = 7
            dy += self.vel_y

            #Kollar efter kollision
            self.in_air = True
            for tile in world.tile_list:
                #Kollar efter kollision i x-led
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height): 
                    dx = 0
                #Kollar efter kollision i y-led           
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #Gör så att man dör och spelar ett ljud om man kolliderar med "DevilShit" fienden
            if pygame.sprite.spritecollide(self, DevilShit_group, False):
                game_over = -1
                death_sound.play()
            
            #Gör så att man dör och spelar ett ljud om man kolliderar med "Spikar" fienden
            if pygame.sprite.spritecollide(self, Spikar_group, False):
                game_over = -1
                death_sound.play()

            #Gör så att man vinner och spelar ett ljud när man kolliderar med målflaggan
            if pygame.sprite.spritecollide(self, Goal_group, False):
                game_over = 1
                pygame.mixer.music.stop()
                goal_sound.play()

            #Uppdaterar gubbens kordinater
            self.rect.x += dx
            self.rect.y += dy

        #Gör så att gubben blir en ängel som flyger till toppen av skärmen när man dör
        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 30:
                self.rect.y -= 3

        #Sätter gubben på skärmen
        screen.blit(self.image, self.rect)

        return game_over

    #En reset metod
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

#Gör en värld klass
class World():
    def __init__(self, data):
        self.tile_list = []

        #Laddar in bilder
        Gräs_Block = pygame.image.load('bilder/Gräs_Block.png')
        Jord_Block = pygame.image.load('bilder/Jord_Block.png')

        #Gör så vi kan lägga in ett visst nummer i world_data som representerar ett visst block/fiende
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:

                #1=Gräs block
                if tile == 1:
                    img = pygame.transform.scale(Gräs_Block, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                #2=Jord block
                if tile == 2:
                    img = pygame.transform.scale(Jord_Block, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                
                #3=DevilShit fienden
                if tile == 3:
                    DevilShit = Enemy(col_count * tile_size, row_count * tile_size + 11)
                    DevilShit_group.add(DevilShit)

                #4=Spikar fienden
                if tile == 4:
                    Spikar = Spikes(col_count * tile_size, row_count * tile_size)
                    Spikar_group.add(Spikar)

                #5=Mål
                if tile == 5:
                    goal = Goal(col_count * tile_size, row_count * tile_size)
                    Goal_group.add(goal)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            #Ritar tilesen ovan på skärmen
            screen.blit(tile[0], tile[1])

#Fiende klass till "DevilShit" som bl.a laddar in bilden och gör en rektangel av den
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
        #Gör så att "DevilShit" rör sig höger och vänster
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 29:
            self.move_direction *= -1
            self.move_counter *= -1

#Spikar klass som bl.a laddar in bilden och gör en rektangel av den
class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bilder/Spikar.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Mål klass som bl.a laddar in bilden och gör en rektangel av den
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bilder/Mål.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Här bestämmer vi var på skärmen vi ska rita in någon av siffrorna 1-5 som representerar olika block/fienden
world_data = [
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
[2, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 0, 0, 0,],
[2, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1,],
[2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 2,],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2,],
[2, 0, 0, 0, 1, 0, 3, 0, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2,],
[2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,], 
]

#Klasserna vi har gjort som vi kan använda i while run loopen sedan
player = Player(60, screen_height - 78)
DevilShit_group = pygame.sprite.Group()
Spikar_group = pygame.sprite.Group()
Goal_group = pygame.sprite.Group()
world = World(world_data)

#Gör olika knappar med hjälp av knapp klassen och bestämmer var på skärmen vi vill ha dem
restart_buttom = Button(screen_width // 2 - 85, screen_height // 2, restart_img)
start_button = Button(screen_width // 2 - 110, screen_height // 2 - 130, start_img)
quit_button = Button(screen_width // 2 - 95, screen_height // 2, quit_img)

#En while loop som går medan run = True och om run = False så slutar loopen(Spelet stängs av)
run = True
while run:

    #Gör så att spelet är i FPSen vi skrev in tidigare
    clock.tick(FPS)

    #Ritar in bakgrundsbilden
    screen.blit(Bakgrund_Himmel, (0, 0))

    #Kollar om man är i main menu eller inte och om man inte är det så laddas världen in
    if main_menu == True:

        #Knapp som stänger av spelet
        if quit_button.draw():
            run = False
        
        #Knapp som startar spelet
        if start_button.draw():
            main_menu = False
            pygame.mixer.music.play(-1, 0.0, 2000)
    else:

        #Laddar in världen
        world.draw()

        #Om man lever så rör sig DevilShit
        if game_over == 0:
            DevilShit_group.update()

        #Ritar ut allt på skärmen
        DevilShit_group.draw(screen)
        Spikar_group.draw(screen)
        Goal_group.draw(screen)

        game_over = player.update(game_over)

        #Om spelaren har dött så stoppar musiken och man kan sedan trycka på en knapp för att börja om
        if game_over == -1:
            pygame.mixer.music.stop()
            if restart_buttom.draw():
                player.reset(60, screen_height - 78)
                game_over = 0
                death_sound.stop()
                pygame.mixer.music.play(-1, 0.0, 2000)

        #Om spelaren når mål så stoppar musiken och kan man sedan trycka på en knapp för att börja om
        if game_over == 1:
            if restart_buttom.draw():
                player.reset(60, screen_height - 78)
                game_over = 0
                goal_sound.stop()
                pygame.mixer.music.play(-1, 0.0, 2000)

    #Om man trycker på krysset i rutan eller om man trycker ESC så stängs spelet av
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                run = False


    pygame.display.update()

pygame.quit()