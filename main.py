import random
import pygame
from pygame import Rect
import pgzrun

# Initialize mixer for sound effects
pygame.mixer.init()

WIDTH = 565
HEIGHT = 425

# Game states
game_state = 'menu'
sound_on = True
game_over_played = False

# Music keys (files in music/ folder)
BG_MUSIC = 'sound_game'

# Load game over sound manually from music folder
game_over_sound = pygame.mixer.Sound('music/game_over.ogg')

# Volume setup
music.set_volume(0.5)
# Start background music
music.play(BG_MUSIC)  # loop by default

# Menu button definitions
button_start_rect = Rect(25, 22, 138, 55)
button_music_rect = Rect(214, 183, 190, 60)
button_exit_rect  = Rect(25, 187, 138, 60)

button_start_pos = (WIDTH//2 - 85, 100)
button_music_pos = (WIDTH//2 - 65, 180)
button_exit_pos  = (WIDTH//2 - 85, 260)

button_start_hit = Rect(button_start_pos, (138,55))
button_music_hit = Rect(button_music_pos, (190,60))
button_exit_hit  = Rect(button_exit_pos,  (138,60))

# Level settings
GRAVITY = 0.5
JUMP_VELOCITY = -10
HERO_START = (75, HEIGHT - 78)
ENEMY_START_POSITIONS = [(300, HEIGHT - 80), (450, HEIGHT - 80)]

# Toggle background music
def toggle_music():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        music.play(BG_MUSIC)
    else:
        music.stop()

# Mouse click handler
def on_mouse_down(pos):
    global game_state, game_over_played
    if game_state == 'menu':
        if button_start_hit.collidepoint(pos):
            game_state = 'playing'
            game_over_played = False
            hero.reset()
            for e in enemies:
                e.reset()
            music.stop()
            if sound_on:
                music.play(BG_MUSIC)
        elif button_music_hit.collidepoint(pos):
            toggle_music()
        elif button_exit_hit.collidepoint(pos):
            exit()

# Hero class
class Hero:
    def __init__(self):
        self.sheet = images.hero_sheet
        self.width = 60
        self.height = 78
        self.walk_frames = [0,1,2,3]
        self.idle_frames = [0,1]
        self.frame_index = 0
        self.is_walking = False
        self.on_ground = False
        self.vel_y = 0.0
        self.pos = list(HERO_START)
        self.anim_timer = 0

    def reset(self):
        self.pos = list(HERO_START)
        self.vel_y = 0
        self.frame_index = 0
        self.is_walking = False
        self.on_ground = False

    def update(self):
        self.is_walking = False
        if keyboard.left:
            self.pos[0] = max(0, self.pos[0] - 5)
            self.is_walking = True
        if keyboard.right:
            self.pos[0] = min(WIDTH - self.width, self.pos[0] + 5)
            self.is_walking = True
        if keyboard.up and self.on_ground:
            self.vel_y = JUMP_VELOCITY
            self.on_ground = False
        # apply gravity
        self.vel_y += GRAVITY
        self.pos[1] += self.vel_y
        # ground collision
        ground_y = HEIGHT - self.height
        if self.pos[1] >= ground_y:
            self.pos[1] = ground_y
            self.vel_y = 0
            self.on_ground = True

    def animate(self):
        self.anim_timer += 1
        if self.is_walking and self.anim_timer % 5 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
        elif not self.is_walking and self.anim_timer % 20 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
        frames = self.walk_frames if self.is_walking else self.idle_frames
        idx = frames[self.frame_index % len(frames)]
        return Rect(idx*self.width, 0, self.width, self.height)

    def draw(self):
        src = self.animate()
        dest = Rect(self.pos[0], self.pos[1], self.width, self.height)
        screen.surface.blit(self.sheet, dest, src)

    def get_rect(self):
        pad_x, pad_y = 10, 10
        return Rect(self.pos[0]+pad_x, self.pos[1]+pad_y,
                    self.width-2*pad_x, self.height-2*pad_y)

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.sheet = images.enemy_sheet
        self.width = 80
        self.height = 80
        self.frames = [0,1,2,3,2,1]
        self.frame_index = 0
        self.start_pos = (x, y)
        self.pos = [x, y]
        self.speed = random.choice([-2, 2])
        self.anim_timer = 0

    def reset(self):
        self.pos = list(self.start_pos)
        self.speed = random.choice([-2, 2])
        self.frame_index = 0

    def update(self):
        self.pos[0] += self.speed
        if self.pos[0] <= 0 or self.pos[0] + self.width >= WIDTH:
            self.speed *= -1

    def animate(self):
        self.anim_timer += 1
        if self.anim_timer % 10 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        return Rect(self.frames[self.frame_index]*self.width, 0, self.width, self.height)

    def draw(self):
        src = self.animate()
        dest = Rect(self.pos[0], self.pos[1], self.width, self.height)
        screen.surface.blit(self.sheet, dest, src)

    def get_rect(self):
        pad_x, pad_y = 15, 15
        return Rect(self.pos[0]+pad_x, self.pos[1]+pad_y,
                    self.width-2*pad_x, self.height-2*pad_y)

# Create instances
hero = Hero()
enemies = [Enemy(x, y) for x, y in ENEMY_START_POSITIONS]

# Main loop functions
def update(dt):
    if game_state != 'playing':
        return
    hero.update()
    for e in enemies:
        e.update()
    check_collision()


def draw():
    screen.clear()
    if game_state == 'menu':
        screen.blit('background', (0, 0))
        screen.surface.blit(images.menu_sprites, button_start_pos, button_start_rect)
        screen.surface.blit(images.menu_sprites, button_music_pos, button_music_rect)
        screen.surface.blit(images.menu_sprites, button_exit_pos, button_exit_rect)
    else:
        screen.blit('background', (0, 0))
        hero.draw()
        for e in enemies:
            e.draw()


def check_collision():
    global game_state, game_over_played
    if game_state != 'playing':
        return
    for e in enemies:
        if hero.get_rect().colliderect(e.get_rect()):
            if sound_on and not game_over_played:
                game_over_sound.play()
                game_over_played = True
            game_state = 'menu'
            reset_game()
            break


def reset_game():
    hero.reset()
    for e in enemies:
        e.reset()

pgzrun.go()
