import random
import math
from pygame import Rect  # permitido
import pgzrun

WIDTH = 565
HEIGHT = 425

# Estados do jogo
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_EXIT = 'exit'

game_state = STATE_MENU
sound_on = True

# Música
music.set_volume(0.5)
music.play('sound_game')

# --- BOTÕES (recorte da imagem spritesheet) ---
button_start_rect = Rect(25, 22, 138, 55)        # PLAY
button_sound_rect = Rect(214, 183, 190, 60)       # SOUND
button_exit_rect = Rect(25, 187, 138, 60)        # EXIT

# Posições na tela
button_start_pos = (WIDTH // 2 - 85, 100)
button_sound_pos = (WIDTH // 2 - 65, 180)
button_exit_pos = (WIDTH // 2 - 85, 260)

# Hitboxes para clique
button_start_hitbox = Rect(button_start_pos, (138, 45))
button_sound_hitbox = Rect(button_sound_pos, (60, 60))
button_exit_hitbox = Rect(button_exit_pos, (138, 45))


# --- FUNÇÕES DE MENU ---
def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        music.play('sound_game')
    else:
        music.stop()


def on_mouse_down(pos):
    global game_state
    if game_state == STATE_MENU:
        if button_start_hitbox.collidepoint(pos):
            game_state = STATE_PLAYING
        elif button_sound_hitbox.collidepoint(pos):
            toggle_sound()
        elif button_exit_hitbox.collidepoint(pos):
            exit()


# --- DRAW ---
def draw():
    screen.clear()

    if game_state == STATE_MENU:
        screen.blit('fundo', (0, 0))

        screen.surface.blit(images.menu_sprites, button_start_pos, button_start_rect)
        screen.surface.blit(images.menu_sprites, button_sound_pos, button_sound_rect)
        screen.surface.blit(images.menu_sprites, button_exit_pos, button_exit_rect)

    elif game_state == STATE_PLAYING:
        draw_game()


# --- UPDATE GERAL ---
def update(dt):
    if game_state == STATE_PLAYING:
        update_game(dt)


# --- HERÓI ---
class Hero:
    def __init__(self):
        self.actor = Actor('hero_idle1', (100, 100))
        self.speed = 3
        self.walk_images = ['hero_walk1', 'hero_walk2']
        self.idle_images = ['hero_idle1', 'hero_idle2']
        self.current_image = 0
        self.is_walking = False

    def update(self):
        self.is_walking = False
        if keyboard.left:
            self.actor.x -= self.speed
            self.is_walking = True
        if keyboard.right:
            self.actor.x += self.speed
            self.is_walking = True
        if keyboard.up:
            self.actor.y -= self.speed
            self.is_walking = True
        if keyboard.down:
            self.actor.y += self.speed
            self.is_walking = True

    def animate(self):
        self.current_image = (self.current_image + 1) % 2
        if self.is_walking:
            self.actor.image = self.walk_images[self.current_image]
        else:
            self.actor.image = self.idle_images[self.current_image]

    def draw(self):
        self.actor.draw()


# --- INIMIGOS ---
class Enemy:
    def __init__(self, x, y):
        self.actor = Actor('enemy1_walk1', (x, y))
        self.walk_images = ['enemy1_walk1', 'enemy1_walk2']
        self.current_image = 0
        self.direction = random.choice(['horizontal', 'vertical'])
        self.range = 50
        self.start_pos = (x, y)
        self.speed = 1

    def update(self):
        if self.direction == 'horizontal':
            self.actor.x += self.speed
            if abs(self.actor.x - self.start_pos[0]) > self.range:
                self.speed *= -1
        else:
            self.actor.y += self.speed
            if abs(self.actor.y - self.start_pos[1]) > self.range:
                self.speed *= -1

    def animate(self):
        self.current_image = (self.current_image + 1) % 2
        self.actor.image = self.walk_images[self.current_image]

    def draw(self):
        self.actor.draw()


# --- INSTÂNCIAS ---
hero = Hero()
enemies = [Enemy(400, 200), Enemy(600, 400)]


# --- LÓGICA DE JOGO ---
def update_game(dt):
    hero.update()
    for enemy in enemies:
        enemy.update()
    check_collision()


def draw_game():
    screen.blit('background', (0, 0))
    hero.draw()
    for enemy in enemies:
        enemy.draw()


def animate_all():
    if game_state == STATE_PLAYING:
        hero.animate()
        for enemy in enemies:
            enemy.animate()


def check_collision():
    for enemy in enemies:
        if hero.actor.colliderect(enemy.actor):
            if sound_on:
                sounds.hit.play()
            reset_game()


def reset_game():
    hero.actor.pos = (100, 100)


# Agendamento da animação dos sprites
clock.schedule_interval(animate_all, 0.3)

pgzrun.go()
