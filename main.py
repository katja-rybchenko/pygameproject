import pygame
import random
import sys
# version 1.1
PINK = (221, 160, 221)
WHITE = (255, 255, 255)
BLUE = (29, 32, 76)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
FPS = 30
animCount = 0
# список анимации
petAnim = [pygame.image.load('арт материал/животное анимация 1.png'),
           pygame.image.load('арт материал/животное анимация 2.png'),
           pygame.image.load('арт материал/животное анимация 1.png'),
           pygame.image.load('арт материал/животное анимация 3.png'),
           pygame.image.load('арт материал/животное анимация 1.png')]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img='арт материал/игрок2.png'):  # класс игрока
        super().__init__()

        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Кординаты
        self.pos_x = 0
        self.pos_y = 0
        self.wall = None
        self.pet = False

        self.coins = None
        self.hun = None
        self.car = None
        self.pet_pet = None
        self.coll_coins = 0
        self.shield = 0
        self.wallet = 100

        self.enemi = pygame.sprite.Group()
        # состояние до встречи с противником
        self.alive = 11
        self.hunger = 100

    def update(self):
        # движение вправо влево
        self.rect.x += self.pos_x
        block_hit_l = pygame.sprite.spritecollide(self, self.wall, False)
        for block in block_hit_l:
            # возвращения игрока
            if self.pos_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        # движение вниз вверх
        self.rect.y += self.pos_y
        block_hit_l = pygame.sprite.spritecollide(self, self.wall, False)
        for block in block_hit_l:
            # возвращения игрока
            if self.pos_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        # проверка на монеты
        coins_hit_l = pygame.sprite.spritecollide(self, self.coins, False)
        for coin in coins_hit_l:
            self.coll_coins += 1
            self.wallet += 100
            coin.kill()

        # взаимодействие с огородом
        garden_hit_l = pygame.sprite.spritecollide(self, self.hun, False)
        for gar in garden_hit_l:
            if self.hunger <= 50:
                self.hunger = 100

        # взаимодействие с табличкой для питомца
        pet_hit_l = pygame.sprite.spritecollide(self, self.pet_pet, False)
        for pet in pet_hit_l:
            if self.wallet >= 500:
                self.wallet += 500
                self.pet = True
                pet.kill()

        # взаимодействие с ковром
        car_hit_l = pygame.sprite.spritecollide(self, self.car, False)
        for carr in car_hit_l:
            if self.alive <= 5:
                self.alive += 5

        # проверка на врага
        if pygame.sprite.spritecollide(self, self.enemi, False) and self.shield == 0:
            if self.hunger <= 2:
                self.alive -= 1
                self.hunger = 100
            self.alive -= 1
            self.shield = 15
            self.hunger -= 1

        if pygame.sprite.spritecollide(self, self.enemi, False) and self.shield > 0:
            if self.hunger <= 2:
                self.alive -= 1
                self.hunger = 100
            self.shield -= 1
            self.hunger -= 1


class Home(pygame.sprite.Sprite):  # класс дом
    def __init__(self, x, y, img='арт материал/домик.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Konyra(pygame.sprite.Sprite):  # дом для любимца
    def __init__(self, x, y, img='арт материал/конура.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall(pygame.sprite.Sprite):  # стены
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("арт материал/стена.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Coins(pygame.sprite.Sprite):  # сундуки
    def __init__(self, x, y, img='арт материал/сундук.png'):
        super().__init__()
        # загрузка изображения
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ссarpet(pygame.sprite.Sprite):  # ковёр
    def __init__(self, x, y, img='арт материал/коврик.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pygame.sprite.Sprite):  # враг
    def __init__(self, x, y, img='арт материал/враг.png', img2='враг2.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # направление врага от начальной точки до конечной точки
        self.start = x
        self.stop = x + random.randint(180, 240)
        self.direct = 2

    def update(self):
        # дошел до конечной точки и обратно k точке старта
        if self.rect.x >= self.stop:
            self.direct = -1
        # обратное направление, 2 конечная точка
        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direct = 1
        # смещение спрайта
        self.rect.x += self.direct * 2


class Checkk(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Garden(pygame.sprite.Sprite):  # класс огород
    def __init__(self, x, y, img='арт материал/огород.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Pet_Table(pygame.sprite.Sprite):  # класс огород
    def __init__(self, x, y, img='арт материал/табличка питомца.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


pygame.init()

font = pygame.font.SysFont('Arial', 24, True)
text2 = font.render('0', True, WHITE)
pet = pygame.image.load('арт материал/животное анимация 1.png')
clock = pygame.time.Clock()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Странствующий по лабиринту')
h_img = pygame.image.load('арт материал/жизни.png')
h_img_hun = pygame.image.load('арт материал/уровеньголода.png')
aplle = pygame.image.load('арт материал/картинка уровня голода.png')
money = pygame.image.load('арт материал/монеточкаиконка.png')
run = False

all_sprite_list = pygame.sprite.Group() # группа слоёв основная
wall_list = pygame.sprite.Group()# группа стен

wall_cord = [
    [0, 0, 10, 1000], [0, 0, 1000, 60], [990, 0, 10, 1000],
    [10, 0, 1000, 10], [10, 200, 100, 10], [390, 550, 220, 10],
    [390, 350, 10, 200], [600, 350, 10, 600], [390, 350, 10, 200],
    [365, 350, 10, 700], [0, 990, 1000, 10], [390, 340, 90, 10],
    [520, 340, 90, 10], [365, 315, 200, 10], [390, 600, 210, 10],
    [440, 550, 10, 30], [490, 580, 10, 30], [390, 630, 190, 10],
    [390, 630, 10, 200], [390, 830, 190, 10], [510, 660, 90, 10],
    [510, 660, 10, 90], [415, 750, 105, 10], [545, 690, 10, 110],
    [415, 790, 140, 10], [570, 670, 10, 170], [365, 940, 190, 10],
    [545, 860, 10, 80], [390, 860, 165, 10], [390, 860, 10, 65],
    [390, 965, 10, 25], [400, 915, 110, 10], [430, 950, 10, 25],
    [470, 965, 10, 25], [510, 950, 10, 25], [545, 965, 10, 25],
    [365, 315, 200, 10], [10, 530, 340, 10],
    [40, 490, 300, 10], [10, 570, 150, 10], [40, 610, 200, 10],
    [10, 650, 300, 10], [40, 690, 300, 10], [10, 730, 340, 10],
    [40, 770, 150, 10], [10, 810, 150, 10], [40, 850, 200, 10],
    [240, 730, 10, 130], [10, 890, 300, 10], [310, 890, 10, 80],
    [270, 760, 10, 130], [340, 530, 10, 170], [310, 760, 10, 130],
    [230, 530, 10, 80], [310, 580, 10, 80], [270, 530, 10, 80],
    [40, 270, 10, 230], [40, 270, 500, 10], [365, 270, 10, 50],
    [100, 300, 10, 200], [140, 270, 10, 200], [180, 300, 10, 200],
    [220, 270, 10, 200], [260, 300, 10, 200], [300, 270, 10, 200],
    [340, 300, 10, 200], [800, 100, 190, 10], [770, 140, 190, 10],
    [800, 180, 190, 10], [770, 220, 190, 10], [800, 260, 190, 10],
    [770, 300, 190, 10], [760, 60, 10, 600], [610, 460, 200, 10],
    [810, 460, 10, 300], [610, 750, 180, 10], [610, 790, 300, 10],
    [910, 790, 10, 160], [870, 830, 10, 160], [770, 350, 190, 10],
    [950, 350, 10, 190], [850, 540, 110, 10], [850, 400, 10, 140],
    [790, 400, 60, 10], [600, 140, 10, 800], [830, 790, 10, 160],
    [790, 830, 10, 160], [750, 790, 10, 160], [710, 830, 10, 160],
    [670, 790, 10, 160], [630, 830, 10, 160], [610, 510, 100, 10],
    [660, 550, 100, 10], [610, 590, 100, 10], [660, 630, 100, 10],
    [610, 700, 160, 10], [555, 140, 10, 175], [295, 140, 260, 10],
    [295, 140, 10, 110], [295, 140, 10, 110], [295, 240, 100, 10],
    [100, 240, 300, 10], [435, 170, 10, 70], [435, 170, 80, 10],
    [435, 240, 120, 10], [390, 170, 10, 70], [330, 170, 60, 10],
    [40, 960, 270, 10], [40, 920, 10, 40], [40, 920, 240, 10],
    [910, 600, 10, 230], [850, 600, 60, 10], [850, 600, 10, 160],
    [850, 460, 80, 10], [610, 300, 100, 10], [660, 340, 100, 10],
    [610, 380, 100, 10], [660, 420, 100, 10], [610, 460, 100, 10],
    [660, 260, 100, 10], [610, 220, 100, 10], [660, 180, 100, 10],
    [610, 140, 100, 10], [40, 100, 700, 10], [40, 100, 10, 80],
    [40, 170, 190, 10], [230, 125, 10, 100],
]
for cord in wall_cord:
    home = Home(400, 390)
    check = Checkk(0, 0, 1000, 50)
    wall = Wall(cord[0], cord[1], cord[2], cord[3])
    kon = Konyra(405, 499)
    wall_list.add(kon)
    all_sprite_list.add(kon)
    wall_list.add(wall)
    all_sprite_list.add(wall)
    wall_list.add(home)
    all_sprite_list.add(home)
    wall_list.add(check)
    all_sprite_list.add(check)

# создание монет
coin_list = pygame.sprite.Group()
coin_cord = [[100, 125], [236, 70], [403, 234],
             [580, 960], [442, 688], [720, 210],
             [940, 590], [940, 690], [940, 790],
             [940, 890], [680, 660], [890, 500],
             [190, 790], [185, 560], [60, 450]]
for cord in coin_cord:
    coin = Coins(cord[0], cord[1])
    coin_list.add(coin)
    all_sprite_list.add(coin)

# создание огорода
garden_list = pygame.sprite.Group()
garden_cord = [[500, 500]]
for cord in garden_cord:
    garden = Garden(cord[0], cord[1])
    garden_list.add(garden)
    all_sprite_list.add(garden)

# добавление и создание таблички
pet_list = pygame.sprite.Group()
pet_cord = [[430, 490]]
for cord in pet_cord:
    pet = Pet_Table(cord[0], cord[1])
    pet_list.add(pet)
    all_sprite_list.add(pet)

# добавление и создание ковра
car_list = pygame.sprite.Group()
car_cord = [[407, 435]]
for cord in car_cord:
    car = Ссarpet(cord[0], cord[1])
    car_list.add(car)
    all_sprite_list.add(car)

# # добавление и создание врага
enemi_list = pygame.sprite.Group()
enemi_cord = [[30, 500], [400, 110], [30, 700], [30, 860], [620, 760]]
for cord in enemi_cord:
    enemy = Enemy(cord[0], cord[1])
    enemi_list.add(enemy)
    all_sprite_list.add(enemy)

player = Player(400, 360)
player.wall = wall_list
all_sprite_list.add(player)

# Добавление списка монет к игроку
player.coins = coin_list

# добавление в создание спрайта игрока
player.enemi = enemi_list

# Добавление списка счёта голода к игроку
player.hun = garden_list

# Добавление списка ковра к игроку
player.car = car_list

# Добавление списка таблички для питомца к игроку
player.pet_pet = pet_list


font = pygame.font.SysFont('Arial', 24, True)
text2 = font.render('0', True, WHITE)
pet = pygame.image.load('арт материал/животное анимация 1.png')
clock = pygame.time.Clock()
run = False


def anim_pet(): # Анимация питомца
    global animCount
    screen.blit(petAnim[animCount // 6], (435, 510))
    animCount += 1
    if animCount >= 30:
        animCount = 0
    pygame.display.update()


def sh_wallet(): # счёт монет
    show = 0
    while show != player.wallet:
        text2 = font.render(f'{player.wallet}', True, WHITE)
        screen.blit(text2, (930, 18))
        show += 1


def sh_hunger(): # уровень голода
    show = 0
    x = 370
    while show != player.hunger:
        screen.blit(h_img_hun, (x, 20))
        x += 2
        show += 1


def show_aplle(): # картинка яблока
    screen.blit(aplle, (340, 15))


def show_money(): # картинка монетки
    screen.blit(money, (900, 12))


def sh_h(): # счёт жизни
    show = 0
    x = 10
    while show != round(player.alive):
        screen.blit(h_img, (x, 10))
        x += 32
        show += 1


def terminate():
    pygame.quit()
    sys.exit()


while not run:
    for event in pygame.event.get():
        for sprite in all_sprite_list: # перемекщение игрока
            if event.type == pygame.QUIT:
                run = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.pos_x = -3
                elif event.key == pygame.K_RIGHT:
                    player.pos_x = 3
                elif event.key == pygame.K_UP:
                    player.pos_y = -3
                elif event.key == pygame.K_DOWN:
                    player.pos_y = 3

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.pos_x = 0
                elif event.key == pygame.K_RIGHT:
                    player.pos_x = 0
                elif event.key == pygame.K_UP:
                    player.pos_y = 0
                elif event.key == pygame.K_DOWN:
                    player.pos_y = 0
            sh_h()
    bg = pygame.image.load("арт материал/фон игры.png")
    screen.blit(bg, (0, 0))

    if player.alive == 0: # экран итогов
        bg2 = pygame.image.load("арт материал/фон заставки.png")
        screen.blit(bg2, (0, 0))
        font = pygame.font.SysFont('Arial', 50, True)
        text3 = font.render(f"Cчёт : {player.wallet}", True, WHITE)
        screen.blit(text3, (420, 450))

    elif player.alive == 11: # экран заставки
        intro_text = ["Начать игру"]
        bg2 = pygame.image.load("арт материал/фон заставки.png")
        screen.blit(bg2, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                player.alive -= 1
    else: # экран игры
        all_sprite_list.update()
        all_sprite_list.draw(screen)
        sh_h()
        sh_wallet()
        sh_hunger()
        show_aplle()
        show_money()
        if player.pet == True:
            anim_pet()
    pygame.display.flip()
    clock.tick(40)

pygame.quit()
