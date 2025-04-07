import pygame
from PPlay.window import *
from PPlay.animation import *
from PPlay.sprite import *
from PPlay.keyboard import *

janela = Window(800, 600)

walk_left = Sprite("Warrior_Purple_walk_left.png", 6)
walk_left.set_sequence_time(0, 6, 120, True)

walk_right = Sprite("Warrior_Purple_walk_right.png", 6)
walk_right.set_sequence_time(0, 6, 120, True)

walk_up = Sprite("Warrior_Purple_walk_up.png", 3)
walk_up.set_sequence_time(0, 3, 120, True)

walk_down = Sprite("Warrior_Purple_walk_down.png", 3)
walk_down.set_sequence_time(0, 3, 120, True)

walk_stay = Sprite("Warrior_Purple_stay.png", 6)
walk_stay.set_sequence_time(0, 6, 120, True)

walk_attack_r = Sprite("Warrior_Purple_attack_right.png", 4)
walk_attack_r.set_sequence_time(0, 4, 120, True)

# enemy_1 = Sprite()

walking = walk_stay
walking.set_position(300,200)

speed = 0.1
speed_jump = speed
attack = 0
walk = 0
jump = 0
air = 0
t = 0
falling = 0

while True:

    janela.set_background_color((0,0,150))
    janela.set_title("teste 1")

    if Keyboard().key_pressed("left"):
        walk_left.x = walking.x 
        walk_left.y = walking.y
        walking = walk_left
        walk = 1

    
    if Keyboard().key_pressed("right"):
        walk_right.x = walking.x 
        walk_right.y = walking.y        
        walking = walk_right
        walk = 1


    if Keyboard().key_pressed("up"):
        walk_up.x = walking.x 
        walk_up.y = walking.y
        walking = walk_up
        walk = 1
        jump = 1
    
    if falling == 1:
        print(speed_jump)
        speed_jump = speed_jump - speed
        walking.y= walking.y - speed_jump*t

    if jump == 1:

        t = 0.1
        # walking.y = walking.y + 0.1*(1.41/2)*t - 0.001*9*(t*t)
    
        if speed_jump < 0.8 and falling == 0:
            print("pulando")
            speed_jump = speed_jump + speed
            walking.y= walking.y + speed_jump*t
            falling = 0
        
        if speed_jump >= 0.8:
            falling = 1

        if speed_jump < -20 and falling == 1:
            falling = 0
            jump = 0

    if Keyboard().key_pressed("down"):
        walk_down.x = walking.x 
        walk_down.y = walking.y
        walking = walk_down
        walk = 1


    if Keyboard().key_pressed("s"):
        speed = 0
        walk_stay.x = walking.x
        walk_stay.y = walking.y
        walking = walk_stay

    if walk == 1 and not (Keyboard().key_pressed("right") or Keyboard().key_pressed("down") or Keyboard().key_pressed("up") or Keyboard().key_pressed("left")):
        walk_stay.x = walking.x
        walk_stay.y = walking.y
        walking = walk_stay

    if not Keyboard().key_pressed("s"):
        speed = 0.1

    if Keyboard().key_pressed("space"):
        walk_attack_r.x = walking.x 
        walk_attack_r.y = walking.y
        walking = walk_attack_r
        attack = 1

    if attack == 1 and walking.get_curr_frame() == 3 :
        walk_stay.x = walking.x
        walk_stay.y = walking.y        
        walking = walk_stay
        walk_attack_r.set_curr_frame(0)
        attack = 0
        

    walking.move_key_x(speed)
    walking.move_key_y(speed)

    walking.draw()
    walking.update()
    janela.update()
