import pygame
import random
from pygame import mixer

# Initialize
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

# Global Variables
win_width = 500
win_height = 600
game_state = False
blink_timer = 0

# Mouse
mouse_pos_x = 0
mouse_pos_y = 0

# Score
score = 0
font = pygame.font.Font('src/fonts/MinecraftRegular-Bmg3.otf', 60)
score_x = 235
score_y = 68 - 18
score_s_x = score_x
score_s_y = score_y + 3

# Game Over
game_over_state = False
game_over_state_count = 0
game_over_img = [pygame.image.load('src/images/game_over/game_over_border.png'),
                 pygame.image.load('src/images/game_over/game_over_damaged.png'),
                 pygame.image.load('src/images/game_over/game_over_darken.png'),
                 pygame.image.load('src/images/game_over/game_over_text.png'),
                 pygame.image.load('src/images/game_over/game_over_return.png')]

# SFX
game_start_sfx = mixer.Sound('src/sounds/game_start.wav')
game_over_sfx = mixer.Sound('src/sounds/game_over.wav')
game_bg_music = mixer.Sound('src/sounds/game_bg_music.wav')

# Main Screen
quote = [pygame.image.load('src/images/home/quote/0.png'),
         pygame.image.load('src/images/home/quote/1.png'),
         pygame.image.load('src/images/home/quote/2.png'),
         pygame.image.load('src/images/home/quote/3.png'),
         pygame.image.load('src/images/home/quote/4.png')]
quote_s = 1
quote_n = 0
quote_count = 0

# Title and Icon
pygame.display.set_caption('Flappy Dicky')
icon = pygame.image.load('src/images/player/player.png') 
pygame.display.set_icon(icon)

# Create screen
win = pygame.display.set_mode((win_width, win_height))
class Actor:
    def __init__(self, img, loc, vel):
        self.img = img
        if type(self.img) == list:
            self.width = self.img[0].get_width()
            self.height = self.img[0].get_height()
        else:
            self.width = self.img.get_width()
            self.height = self.img.get_height()
        self.loc = loc
        self.vel = vel

    def get_img(self):
        return self.img

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_loc(self, loc):
        return self.loc[loc]

    def set_img(self, img):
        self.img = img

    def set_loc(self, loc, n):
        self.loc[loc] = n

    def show(self):
        win.blit(self.img, (int(self.loc[0]), int(self.loc[1])))


class Button(Actor):

    sfx_state = True
    music_state = True

    def __init__(self, img, loc, vel, func):
        super().__init__(img, loc, vel)
        self.func = func
        self.clicked = False
        self.click_timer = 0
        self.n = 0

    @classmethod
    def get_music_state(cls):
        return cls.music_state

    @classmethod
    def get_sfx_state(cls):
        return cls.sfx_state

    @classmethod
    def function(cls, function):
        if function == 'music':
            if not cls.music_state:
                cls.music_state = True
                game_bg_music.play()

            else:
                cls.music_state = False
                game_bg_music.stop()

        if function == 'sfx':
            if not cls.sfx_state:
                cls.sfx_state = True
            else:
                cls.sfx_state = False

    def show(self):

        mouse = pygame.mouse.get_pressed()

        if self.loc[0] <= mouse_pos_x <= self.loc[0] + self.width and \
                self.loc[1] <= mouse_pos_y <= self.loc[1] + self.height:
            if self.click_timer == 0:
                if mouse[0]:
                    if not self.clicked:
                        self.clicked = True
                        self.n = 1
                    else:
                        self.clicked = False
                        self.n = 0
                    Button.function(self.func)
                    self.click_timer = 1

        win.blit(self.img[self.n], (self.loc[0], self.loc[1]))

        if self.click_timer >= 0:
            self.click_timer += 1
            if self.click_timer == 10:
                self.click_timer = 0


class Floor(Actor):
    total = 0
    gap = 0

    def __init__(self, img, loc, vel):
        super().__init__(img, loc, vel)
        self.loc[0] = Floor.get_gap()
        Floor.add_gap(self.width)
        Floor.add_floor()

    @classmethod
    def get_total(cls):
        return cls.total

    @classmethod
    def get_gap(cls):
        return cls.gap

    @classmethod
    def reset_gap(cls):
        cls.gap = 0

    @classmethod
    def add_floor(cls):
        cls.total += 1

    @classmethod
    def add_gap(cls, x):
        cls.gap += x

    def reset(self):
        self.loc[0] = Floor.get_gap()
        Floor.add_gap(self.get_width())

    def move_x(self):
        self.loc[0] -= self.vel
        if self.loc[0] == -self.width:
            self.loc[0] = win_width

    def show(self):
        win.blit(self.img, (self.loc[0], self.loc[1]))

    def display(self):
        self.show()
        if game_state and not game_over_state:
            self.move_x()


class Tree(Actor):
    total = 0
    gap = 0
    spawn_timer = 0

    def __init__(self, img, loc, vel):
        super().__init__(img, loc, vel)
        self.loc[0] = 125 + Tree.get_gap()
        Tree.add_gap(-125 - self.width)
        Tree.add_tree()

    @classmethod
    def get_total(cls):
        return cls.total

    @classmethod
    def get_gap(cls):
        return cls.gap

    @classmethod
    def get_spawn_timer(cls):
        return cls.spawn_timer

    @classmethod
    def set_spawn_timer(cls, x):
        cls.spawn_timer = x

    @classmethod
    def add_tree(cls):
        cls.total += 1

    @classmethod
    def add_gap(cls, x):
        cls.gap += x

    @classmethod
    def add_spawn_timer(cls):
        cls.spawn_timer += 1

    @classmethod
    def reset_gap(cls):
        cls.gap = 0

    def reset(self):
        self.loc[0] = 125 + Tree.get_gap()
        Tree.add_gap(-125 - self.width)
        Tree.set_spawn_timer(0)

    def move_x(self):
        if self.loc[0] != -self.width:
            self.loc[0] -= self.vel
        if self.loc[0] == -self.width:

            if Tree.get_spawn_timer() == 0:
                if random.randint(0, 100) == 0:
                    Tree.set_spawn_timer(1)
                    if random.randint(0, 1) == 0:
                        self.img = pygame.image.load('src/images/background/tree/oak.png')
                    else:
                        self.img = pygame.image.load('src/images/background/tree/birch.png')
                    self.loc[0] = win_width
            else:
                Tree.add_spawn_timer()
                if Tree.get_spawn_timer() == 251:
                    Tree.set_spawn_timer(0)

    def display(self):
        self.show()
        if game_state and not game_over_state:
            self.move_x()


class Obstacle(Actor):
    total = 0
    gap = 0

    def __init__(self, img, loc, vel):
        super().__init__(img, loc, vel)
        self.loc[0] = win_width + 160 + Obstacle.get_gap()
        y = random.randint((-self.height) + 96, 0)
        self.loc[1] = y
        self.loc_pair = [self.loc[0], self.loc[1] + self.height + 160]
        Obstacle.add_gap(160 + self.width)
        Obstacle.add_obs()

    @classmethod
    def get_total(cls):
        return cls.total

    @classmethod
    def get_gap(cls):
        return cls.gap

    @classmethod
    def reset_gap(cls):
        cls.gap = 0

    @classmethod
    def add_obs(cls):
        cls.total += 1

    @classmethod
    def add_gap(cls, x):
        cls.gap += x

    def get_loc_pair(self, n):
        return self.loc_pair[n]

    def reset(self):
        self.loc[0] = win_width + 160 + Obstacle.get_gap()
        y = random.randint((-self.height) + 96, 0)
        self.loc[1] = y
        self.loc_pair = [self.loc[0], self.loc[1] + self.height + 160]
        Obstacle.add_gap(160 + self.width)

    def move_x(self):
        self.loc[0] -= self.vel
        self.loc_pair[0] = self.loc[0]
        if self.loc[0] == -self.width:
            self.loc[0] = win_width + 160
            y = random.randint((-self.height) + 96, 0)
            self.loc[1] = y
            self.loc_pair[1] = self.loc[1] + self.height + 160

    def show(self):
        win.blit(self.img, (self.loc[0], self.loc[1]))
        win.blit(self.img, (self.loc_pair[0], self.loc_pair[1]))

    def collision(self):
        pass

    def display(self):
        self.show()
        if game_state and not game_over_state:
            self.move_x()
        self.collision()


class Herobrine(Actor):
    def move_x(self, tree):
        if self.loc[0] != -self.width:
            self.loc[0] -= self.vel
        if self.loc[0] == -self.width:
            if random.randint(0, 100) == 0:
                for n in range(Tree.get_total()):
                    if tree[n].get_loc(0) >= win_width - 75:
                        if random.randint(0, 1) == 0:
                            self.loc[0] = (tree[n].get_loc(0) + (tree[n].get_width()) / 2) - self.width
                        else:
                            self.loc[0] = (tree[n].get_loc(0) + (tree[n].get_width()) / 2)

    def display(self, tree):
        self.show()
        if game_state and not game_over_state:
            self.move_x(tree)


class Player(Actor):

    def __init__(self, img, loc, vel, jump_sfx):
        super().__init__(img, loc, vel)

        # Jump

        self.jump_sfx = jump_sfx
        self.jump_distance = 10
        self.jump_distance_max = -self.jump_distance
        self.jump_state = False
        self.fall = 0

    def set_jump_state(self, state):
        self.jump_state = state

    def get_jump_state(self):
        return self.jump_state

    def action(self):

        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        if game_state:
            if mouse[0] or mouse[2] or keys[pygame.K_SPACE]:
                self.jump_state = True

        if not self.jump_state:
            self.loc[1] += self.fall

        self.fall += 0.5

        self.jump()

    def jump(self):

        if self.jump_state:
            if self.jump_distance >= self.jump_distance_max:
                if self.jump_distance == 10:
                    if game_state:
                        if Button.get_sfx_state():
                            self.jump_sfx.play()
                self.loc[1] += -self.jump_distance
                self.jump_distance -= 1
                if self.jump_distance == 0:
                    self.fall = 0
                    self.jump_state = False
                    self.jump_distance = 10

    def collision(self, player, obstacle):
        global game_over_state
        if self.loc[1] >= win_height - self.height - 17:
            self.loc[1] = win_height - self.height - 17
            if not game_over_state:
                game_start_sfx.stop()
            game_over_state = True
        for n in range(Obstacle.get_total()):
            if collision(player.get_loc(0), player.get_loc(1), player.get_width(), player.get_height(),
                         obstacle[n].get_loc(0), obstacle[n].get_loc(1), obstacle[n].get_width(),
                         obstacle[n].get_height(),
                         17, 17, 34, 10) or \
                    collision(player.get_loc(0), player.get_loc(1), player.get_width(), player.get_height(),
                              obstacle[n].get_loc(0), obstacle[n].get_loc(1), obstacle[n].get_width(),
                              obstacle[n].get_height(),
                              6, 6, 4, 30) or \
                    collision(player.get_loc(0), player.get_loc(1), player.get_width(), player.get_height(),
                              obstacle[n].get_loc_pair(0), obstacle[n].get_loc_pair(1), obstacle[n].get_width(),
                              obstacle[n].get_height(),
                              17, 17, 34, 10) or \
                    collision(player.get_loc(0), player.get_loc(1), player.get_width(), player.get_height(),
                              obstacle[n].get_loc_pair(0), obstacle [n].get_loc_pair(1), obstacle[n].get_width(),
                              obstacle[n].get_height(),
                              6, 6, 4, 30):
                game_over_state = True
                pass

    def score(self, obstacle):
        global score
        for n in range(Obstacle.get_total()):
            if self.loc[0] == obstacle[n].get_loc(0) + obstacle[n].get_width():
                if Button.get_sfx_state():
                    mixer.Sound('src/sounds/score_increment.wav').play()
                score += 1

    def display(self, player, obstacle):
        self.show()
        if not game_over_state:
            self.action()
        self.collision(player, obstacle)
        self.score(obstacle)


def collision(object_1_x, object_1_y, object_1_width, object_1_height,
              object_2_x, object_2_y, object_2_width, object_2_height,
              right, left, bottom, top):
    # Left, Right, Top, Bottom
    if (((object_2_x - object_1_width + right)
         <= object_1_x <=
         (object_2_x + object_2_width + -left))
            and ((object_2_y - object_1_height) + bottom)
            <= object_1_y <=
            (object_2_y + object_2_height + -top)):
        return True
    else:
        return False


def menu(player):
    global game_state, quote_n, quote_count, quote_s, blink_timer

    if not game_state:
        win.blit(pygame.image.load('src/images/home/title.png'), (93, 25))

        win.blit(quote[quote_n], (228, 145))

        if quote_count % 5 == 0:
            quote_count = 0
            if quote_n == 4:
                quote_s = -1
            elif quote_n == 0:
                quote_s = 1
            quote_n += 1 * quote_s
        quote_count += 1

        if blink_timer < 50:
            win.blit(pygame.image.load('src/images/home/start.png'), (128, 290))
        if blink_timer == 60:
            blink_timer = 0
        blink_timer += 1

        if player.get_loc(1) >= 400:
            player.set_jump_state(True)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                game_start_sfx.play()
                game_state = True
                blink_timer = 0
                quote_count = 0
                quote_n = 0
                quote_s = 1


def score_display():
    global score_x, score_s_x
    if game_state:
        if 10 <= score <= 99:
            score_x = 235 - 18
            score_s_x = score_x
        if 100 <= score <= 999:
            score_x = 235 - 36
            score_s_x = score_x
        win.blit(font.render(str(score), False, (0, 0, 0)), (score_s_x, score_s_y))
        win.blit(font.render(str(score), False, (255, 255, 255)), (score_x, score_y))


def game_over(floor, tree, obstacle, player):
    global game_state, game_over_state, game_over_state_count, score, score_x, blink_timer

    if game_over_state:

        if game_over_state_count == 0:
            game_bg_music.stop()
            game_over_sfx.play()

        win.blit(game_over_img[0], (0, 0))

        if 1 <= game_over_state_count <= 6 or \
                74 <= game_over_state_count <= 79:
            win.blit(game_over_img[1], (0, 0))

        if game_over_state_count >= 80:
            win.blit(game_over_img[2], (0, 0))
            win.blit(game_over_img[3], (97, 239))

        if game_over_state_count >= 120:
            if blink_timer < 50:
                win.blit(game_over_img[4], (25, win_height - game_over_img[4].get_height() - 25))
            if blink_timer == 60:
                blink_timer = 0
            blink_timer += 1

        game_over_state_count += 1

        if game_over_state_count >= 120:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Score
                    score = 0
                    score_x = 235
                    # Player
                    player.set_loc(0, 64)
                    player.set_loc(1, 400)
                    # Floor
                    Floor.reset_gap()
                    for n in range(Floor.get_total()):
                        floor[n].reset()
                    # Trees
                    Tree.reset_gap()
                    for n in range(Floor.get_total()):
                        tree[n].reset()
                    # Obstacles
                    Obstacle.reset_gap()
                    for n in range(Obstacle.get_total()):
                        obstacle[n].reset()
                    game_over_sfx.stop()
                    # Game
                    game_over_state = False
                    game_state = False
                    game_over_state_count = 0
                    blink_timer = 0
                    game_bg_music.stop()
                    if Button.get_music_state():
                        game_bg_music.play(-1)


def redraw_win(background, button_sfx, button_music, floor, tree, obstacle, herobrine, player):
    background.show()
    win.blit(pygame.image.load('src/images/background/sun.png'),
             (win_width - pygame.image.load('src/images/background/sun.png').get_width() - 25,
              25))
    herobrine.display(tree)
    for n in range(Tree.get_total()):
        tree[n].display()
    for n in range(Obstacle.get_total()):
        obstacle[n].display()
    player.display(player, obstacle)
    for n in range(Floor.get_total()):
        floor[n].display()
    menu(player)
    game_over(floor, tree, obstacle, player)
    score_display()
    button_sfx.show()
    button_music.show()
    pygame.display.update()


def main():
    global mouse_pos_x, mouse_pos_y

    running = True
    clock = pygame.time.Clock()

    background = Actor(pygame.image.load('src/images/background/background.png'), [0, 0], 1)

    # Button
    button_sfx = Button([pygame.image.load('src/images/button/sfx/display.png'),
                         pygame.image.load('src/images/button/sfx/clicked.png')],
                        [win_width - (pygame.image.load('src/images/button/sfx/display.png').get_width()*2) - 25 - 10,
                         win_height - pygame.image.load('src/images/button/sfx/display.png').get_height() - 25], None,
                        'sfx')

    button_music = Button([pygame.image.load('src/images/button/music/display.png'),
                           pygame.image.load('src/images/button/music/clicked.png')],
                          [win_width - pygame.image.load('src/images/button/music/display.png').get_width() - 25,
                           win_height - pygame.image.load('src/images/button/music/display.png').get_height() - 25], None,
                          'music')

    floor = []
    for n in range(2):
        floor.append(Floor(pygame.image.load('src/images/background/floor.png'),
                           [0, win_height - pygame.image.load('src/images/background/floor.png').get_height()], 1))

    tree = []
    for n in range(2):
        tree.append(Tree(pygame.image.load('src/images/background/tree/oak.png'),
                         [0, win_height - pygame.image.load('src/images/background/tree/oak.png').get_height() - 17], 1))

    obstacle = []
    for n in range(3):
        obstacle.append(Obstacle(pygame.image.load('src/images/background/obstacle.png'), [0, 0], 1))

    herobrine = Herobrine(pygame.image.load('src/images/herobrine.png'),
                          [-pygame.image.load('src/images/herobrine.png').get_width(),
                           win_height - pygame.image.load('src/images/herobrine.png').get_height() - 17], 1)

    player = Player(pygame.image.load('src/images/player/player.png'), [64, 400], 8, mixer.Sound('src/images/player/player_jump.wav'))

    game_bg_music.play(-1)


    while running:

        clock.tick(60)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos_x = mouse_pos[0]
        mouse_pos_y = mouse_pos[1]
        redraw_win(background, button_sfx, button_music, floor, tree, obstacle, herobrine, player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()


main()
