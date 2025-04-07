import pygame
from PPlay.window import *
from PPlay.animation import *
from PPlay.sprite import *
from PPlay.keyboard import *

janela = Window(800, 600)
teclado = Keyboard()

class Character:
    def __init__(self, tipo, jump, sprite):
        self.tipo = tipo
        self.jump = jump
        self.sprite = Sprite(sprite, 6)

    def exibir_info(self):
        print(f"\nType: {self.tipo} \njump: {self.jump}")

    def position(self, x ,y):
        self.sprite.set_position(x, y)

class Player (Character):
    def __init__(self, tipo, jump, speed, sprite):
        super().__init__(tipo, jump, sprite)
        self.speed = speed
        self.vy = 0  # Velocidade vertical
        self.is_jumping = False
        self.gravity = 1800
        self.jump_force = -800
        self.ground_y = 300  # altura inicial do chão
        
    def mover(self):
        """Move o personagem baseado na entrada do teclado"""
        
        if teclado.key_pressed("DOWN"):
            self.sprite.y += self.speed * janela.delta_time()

        if teclado.key_pressed("LEFT"):
            self.sprite.x -= self.speed * janela.delta_time()

        if teclado.key_pressed("RIGHT"):
            self.sprite.x += self.speed * janela.delta_time()
            
    def pular(self):

        if teclado.key_pressed("UP") and not self.is_jumping:
            self.vy = self.jump_force
            self.is_jumping = True

        self.vy += self.gravity * janela.delta_time()
        self.sprite.y += self.vy * janela.delta_time()

        if self.sprite.y >= self.ground_y:
            self.sprite.y = self.ground_y
            self.vy = 0
            self.is_jumping = False


    def desenhar(self):
        """Desenha o sprite na tela"""
        self.sprite.draw()

player = Player("Humano", False, 200, "Warrior_Purple_stay.png")  # Certifique-se de ter um arquivo "player.png"
player.position(300,300)

while True:
    janela.set_background_color((0, 0, 0))  # Define fundo preto\
    player.mover()  # Atualiza a posição do jogador
    player.desenhar()  # Desenha o jogador na tela
    player.pular()
    janela.update()
