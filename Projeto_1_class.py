import pygame
import json
from PPlay.animation import *
from PPlay.collision import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.point import *
from PPlay.sound import *
from PPlay.sprite import *
from PPlay.window import *


janela = Window(800, 400)
teclado = Keyboard()

# Carrega colisores do JSON exportado do Tiled
with open("tiles_64x64/Primeiro_andar_Raízes.json") as f:
    mapa = json.load(f)

colisores = []
for layer in mapa["layers"]:
    if layer["type"] == "objectgroup" and layer["name"] == "objetos":
        for obj in layer["objects"]:
            bloco = GameImage("bloco_transparente.png")
            bloco.set_position(obj["x"], obj["y"])
            bloco.width = obj["width"]
            bloco.height = obj["height"]
            colisores.append(bloco)

class Camera:
    def __init__(self, window_width, window_height):
        self.x = 0
        self.y = 0
        self.window_width = window_width
        self.window_height = window_height

    def update(self, target):
        self.x = target.x - self.window_width // 2 + target.width // 2
        self.y = target.y - self.window_height // 2 + target.height // 2

    def apply(self, obj):
        """Aplica o offset da câmera a um objeto PPlay (Sprite/GameImage)."""
        obj.set_position(obj.x - self.x, obj.y - self.y)

    def undo(self, obj):
        """Restaura a posição original após desenhar."""
        obj.set_position(obj.x + self.x, obj.y + self.y)


class Character:
    def __init__(self, tipo, jump, hp):
        self.tipo = tipo
        self.jump = jump
        self.hp = hp

class Player(Character):
    def __init__(self, tipo, jump, speed, hp,
                 sprite_stay, sprite_left, sprite_right, sprite_attack_l, sprite_attack_r):
        
        super().__init__(tipo, jump, hp)
        self.speed = speed
        self.vy = 0
        self.is_jumping = False
        self.gravity = 1800
        self.jump_force = -500

        self.sprite_stay = Sprite(sprite_stay, 4)
        self.sprite_right = Sprite(sprite_right, 5)
        self.sprite_left = Sprite(sprite_left, 5)
        self.sprite_attack_l = Sprite(sprite_attack_l, 5)
        self.sprite_attack_r = Sprite(sprite_attack_r, 5)

        self.sprite_stay.set_sequence_time(0, 3, 220, True)
        self.sprite_left.set_sequence_time(0, 4, 220, True)
        self.sprite_right.set_sequence_time(0, 4, 220, True)
        self.sprite_attack_l.set_sequence_time(0, 5, 120)
        self.sprite_attack_r.set_sequence_time(0, 5, 120)

        self.sprite = self.sprite_stay

    def position(self, x, y):
        self.sprite.set_position(x, y)

    def atualizar_pos_sprites(self):
        self.sprite_left.x = self.sprite.x
        self.sprite_left.y = self.sprite.y

        self.sprite_right.x = self.sprite.x
        self.sprite_right.y = self.sprite.y

        self.sprite_stay.x = self.sprite.x
        self.sprite_stay.y = self.sprite.y

        self.sprite_attack_r.x = self.sprite.x
        self.sprite_attack_r.y = self.sprite.y

        self.sprite_attack_l.x = self.sprite.x
        self.sprite_attack_l.y = self.sprite.y

    def mover(self):
        if teclado.key_pressed("LEFT"):
            self.sprite = self.sprite_left
            self.sprite.x -= self.speed * janela.delta_time()
            for bloco in colisores:
                if Collision.collided(self.sprite, bloco):
                    self.sprite.x = bloco.x + bloco.width + 1

        elif teclado.key_pressed("RIGHT"):
            self.sprite = self.sprite_right
            self.sprite.x += self.speed * janela.delta_time()

            for bloco in colisores:
                if Collision.collided(self.sprite, bloco):
                    self.sprite.x = bloco.x - self.sprite.width - 1

        else:
            self.sprite = self.sprite_stay

    def pular(self):
        if not self.is_jumping and teclado.key_pressed("UP"):
            self.vy = self.jump_force
            self.is_jumping = True

        self.vy += self.gravity * janela.delta_time()
        self.sprite.y += self.vy * janela.delta_time()

        for bloco in colisores:
            if Collision.collided(self.sprite, bloco) and self.vy > 0:
                self.sprite.y = bloco.y - self.sprite.height
                self.vy = 0
                self.is_jumping = False
                break

    def atacar(self):
        if teclado.key_pressed("space"):
            self.sprite = self.sprite_attack_r

        if teclado.key_pressed("space") and teclado.key_pressed("LEFT"):
            self.sprite = self.sprite_attack_l

    def desenhar(self):
        self.sprite.update()
        self.sprite.draw()

player = Player(
    tipo="Guerreiro",
    jump=False,
    speed=100,
    sprite_stay="knight-character-sprites-pixel-art\Spritesheet 128\Knight_1\Idle2.png",
    sprite_left="knight-character-sprites-pixel-art\Spritesheet 128\Knight_1\Walk_left2.png",
    sprite_right="knight-character-sprites-pixel-art\Spritesheet 128\Knight_1\walk_right2.png",
    sprite_attack_r="knight-character-sprites-pixel-art\Spritesheet 128\Knight_1\Attack_right.png",
    sprite_attack_l="knight-character-sprites-pixel-art\Spritesheet 128\Knight_1\Attack_left.png",
    hp=100
    )

player.position(50, 850)

camera = Camera(janela.width, janela.height)

tile1 = GameImage("tiles_64x64\Primeiro_andar_Raízes.png")

while True:
    janela.set_background_color((0, 0, 0))

    camera.update(player.sprite)

    player.atualizar_pos_sprites()
    player.pular()
    player.mover()
    player.atacar()

    # Blocos com offset de câmera
    for bloco in colisores:
        camera.apply(bloco)
        bloco.draw()
        camera.undo(bloco)

    camera.apply(tile1)
    tile1.draw()
    camera.undo(tile1)

    # Player com offset de câmera
    camera.apply(player.sprite)
    player.desenhar()
    camera.undo(player.sprite)

    janela.update()