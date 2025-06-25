import random
from pygame import Rect
import pgzrun

WIDTH = 565
HEIGHT = 425

# Estados do jogo
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_EXIT = 'exit'

game_state = STATE_MENU
sound_on = True
game_over_played = False  # flag para som game_over

# Música
music.set_volume(0.5)
music.play('sound_game')

# --- BOTÕES (recorte da imagem spritesheet) ---
button_start_rect = Rect(25, 22, 138, 55)        # PLAY
button_sound_rect = Rect(214, 183, 190, 60)      # SOUND
button_exit_rect = Rect(25, 187, 138, 60)        # EXIT

# Posições na tela
button_start_pos = (WIDTH // 2 - 85, 100)
button_sound_pos = (WIDTH // 2 - 65, 180)
button_exit_pos = (WIDTH // 2 - 85, 260)

# Hitboxes para clique
button_start_hitbox = Rect(button_start_pos, (138, 55))
button_sound_hitbox = Rect(button_sound_pos, (60, 60))
button_exit_hitbox = Rect(button_exit_pos, (138, 60))


# --- FUNÇÕES DE MENU ---
def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        music.play('sound_game')
    else:
        music.stop()


def on_mouse_down(pos):
    global game_state, game_over_played
    if game_state == STATE_MENU:
        if button_start_hitbox.collidepoint(pos):
            hero.pos = [75, 9]            # reseta posição
            game_over_played = False      # libera game_over para próxima vez
            music.stop()
            music.play('sound_game')      # retoma música de fundo
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


# --- HERÓI COM SPRITESHEET ---
class Hero:
    def __init__(self):
        self.image = images.hero_sheet
        self.pos = [75, 9]
        self.speed = 10
        self.frame_width = 55
        self.frame_height = 78
        self.frames = [0, 1, 2, 3]
        self.current_frame = 0
        self.is_walking = False

    def update(self):
        self.is_walking = False
        if keyboard.left:
            self.pos[0] -= self.speed
            self.is_walking = True
        if keyboard.right:
            self.pos[0] += self.speed
            self.is_walking = True
        if keyboard.up:
            self.pos[1] -= self.speed
            self.is_walking = True
        if keyboard.down:
            self.pos[1] += self.speed
            self.is_walking = True

        # Limitar herói dentro da tela
        self.pos[0] = max(0, min(self.pos[0], WIDTH - self.frame_width))
        self.pos[1] = max(0, min(self.pos[1], HEIGHT - self.frame_height))

    def animate(self):
        if self.is_walking:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        else:
            self.current_frame = 0

    def draw(self):
        src_x = self.current_frame * self.frame_width
        src_y = 0
        source_rect = Rect(src_x, src_y, self.frame_width, self.frame_height)
        dest_rect = Rect(self.pos[0], self.pos[1], self.frame_width, self.frame_height)
        screen.surface.blit(self.image, dest_rect, source_rect)

    def get_rect(self):
        padding_x = 10
        padding_y = 10
        return Rect(
            self.pos[0] + padding_x,
            self.pos[1] + padding_y,
            self.frame_width - 2 * padding_x,
            self.frame_height - 2 * padding_y,
        )


# --- INIMIGO COM SPRITESHEET ---
class Enemy:
    def __init__(self, x, y):
        self.image = images.enemy_sheet
        self.pos = [x, y]
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.speed_y = random.choice([-1, 1]) * random.uniform(0.5, 1.5)

        self.frame_width = 80
        self.frame_height = 80

        self.frames = [0, 1, 2, 3, 2, 1]
        self.current_frame = 0

    def update(self):
        # Movimento contínuo
        self.pos[0] += self.speed_x
        self.pos[1] += self.speed_y

        # Rebater nas bordas da tela
        if self.pos[0] < 0 or self.pos[0] + self.frame_width > WIDTH:
            self.speed_x *= -1
        if self.pos[1] < 0 or self.pos[1] + self.frame_height > HEIGHT:
            self.speed_y *= -1

    def animate(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self):
        src_x = self.frames[self.current_frame] * self.frame_width
        src_y = 0  # Primeira linha da spritesheet
        source_rect = Rect(src_x, src_y, self.frame_width, self.frame_height)
        screen.surface.blit(self.image, self.pos, source_rect)

    def get_rect(self):
        padding_x = 15
        padding_y = 15
        return Rect(
            self.pos[0] + padding_x,
            self.pos[1] + padding_y,
            self.frame_width - 2 * padding_x,
            self.frame_height - 2 * padding_y,
        )


# --- INSTÂNCIAS ---
hero = Hero()
enemies = [Enemy(400, 200), Enemy(200, 300), Enemy(200, 300), Enemy(200, 300)]


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
    global game_over_played, game_state
    for enemy in enemies:
        if hero.get_rect().colliderect(enemy.get_rect()):
            if sound_on and not game_over_played:
                music.stop()
                music.play('game_over')      # toca game_over.ogg uma vez
                game_over_played = True
            reset_game()
            game_state = STATE_MENU
            break  # importa sair do loop para não repetir


# Posições iniciais dos inimigos
ENEMY_START_POSITIONS = [
    (400, 200),
    (200, 300),
    (200, 300),
    (200, 300)
]

# --- INSTÂNCIAS ---
hero = Hero()
enemies = [Enemy(x, y) for x, y in ENEMY_START_POSITIONS]

# RESET GAME
def reset_game():
    hero.pos = [75, 9]
    for enemy, (x0, y0) in zip(enemies, ENEMY_START_POSITIONS):
        enemy.pos = [x0, y0]

# Agendamento da animação dos sprites
clock.schedule_interval(animate_all, 0.3)

pgzrun.go()
