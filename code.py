import time
import board

import digitalio
import busio
import adafruit_lis3dh

import adafruit_imageload

from random import randint

import displayio
from adafruit_st7789 import ST7789

import math
#import gc

from adafruit_seesaw.seesaw import Seesaw

import terminalio
from adafruit_display_text import label

font = terminalio.FONT

# setup for accelerometer

i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x18, int1=int1)

# backlight left display pin initialisation
ss = Seesaw(i2c)
ss.pin_mode(5, ss.OUTPUT)
ss.pin_mode(9, ss.INPUT_PULLUP)
ss.pin_mode(10, ss.INPUT_PULLUP)
ss.pin_mode(11, ss.INPUT_PULLUP)


# display setup for m4sk

displayio.release_displays()

spi1 = busio.SPI(board.RIGHT_TFT_SCK, MOSI=board.RIGHT_TFT_MOSI)
display1_bus = displayio.FourWire(spi1, command=board.RIGHT_TFT_DC, chip_select=board.RIGHT_TFT_CS, reset=board.RIGHT_TFT_RST)
display1 = ST7789(display1_bus, width=240, height=240, rowstart=80,
                 backlight_pin=board.RIGHT_TFT_LITE)


spi2 = busio.SPI(board.LEFT_TFT_SCK, MOSI=board.LEFT_TFT_MOSI)
display2_bus = displayio.FourWire(spi2, command=board.LEFT_TFT_DC, chip_select=board.LEFT_TFT_CS)
display2 = ST7789(display2_bus, width=240, height=240, rowstart=80)

# backlight left display on
ss.analog_write(5, 255)

# Functions

# return angle in degrees from atan2(y, x) from accelerometer, ajusted to the display orientation, plus absolute inclinaison of screen ( > 9.7ish is flat, 0 is up)
def get_angle():
    x, y, z = lis3dh.acceleration
    angle = math.degrees(math.atan2(y,x)) + 90.0
    if angle < 0:
        angle = 360 + angle
    #print(angle, abs(z))
    return (angle, abs(z))

#test collision for 16p sprites .
def collision(a, b):
    if abs(a.x-b.x)**2 + abs(a.y-b.y)**2 < 16 ** 2:
        # collision
        # print("COLLISION !!!")
        return True
    else:
        return False

# reset heart position
def reset_heart():
    global active_heart
    for i in range(1,5):
        heart_group.hidden = True
        time.sleep(0.15)
        heart_group.hidden = False
        time.sleep(0.15)
    heart_group.hidden = True
    cur_heart = active_heart
    active_heart = randint(0,1)
    if cur_heart == active_heart:
        if active_heart == 0:
            heart.x = randint(48, 207)
            heart.y = randint(48, 176)
            heart_group.hidden = False
        else:
            heart.x = randint(17, 176)
            heart.y = randint(48, 176)
            heart_group.hidden = False
    else:
        if active_heart == 1:
            group.remove(heart_group)
            group2.insert(1,heart_group)
            heart.x = randint(17, 176)
            heart.y = randint(48, 176)
            heart_group.hidden = False
        else:
            group2.remove(heart_group)
            group.insert(1,heart_group)
            heart.x = randint(48, 207)
            heart.y = randint(48, 176)
            heart_group.hidden = False


def show_game_over():
    # print("Game is over",gameover_text_group.x, gameover_text_group.y)
    gameover_text_group.y += 2
    if gameover_text_group.y > 240:
        gameover_text_group.y = -50
        gameover_text_group.x = randint(0,90)

def reinitialize_game():
    print("Reinitialise game !")
    global score_player, score_opponent, level, active_heart, active_oppo, active_sprite, act_op, act_sp, gameover, oppo_group, sprite_group
    gameover_group.hidden = True
    group.remove(gameover_group)
    score_player = 0
    score_opponent = 0
    level = 1
    text_area1.text = "0"
    text_area2.text = "0"
    text_area4.text = "1"
    sprite.x = 112
    sprite.y = 48
    opponent.x = 112
    opponent.y = 176
    heart.x = randint(48, 224)
    heart.y = 112
    if active_heart == 1:
        group2.remove(heart_group)
        group.insert(1, heart_group)
    active_heart = 0
    active_oppo = 0
    active_sprite = 0
    act_op = opponent
    act_sp = sprite
    sprite2_group.hidden = True
    oppo2_group.hidden = True
    sprite_group.hidden = False
    oppo_group.hidden = False
    gameover = False
    oppo_group.hidden = False

print("Going to the castle !")

sprite_sheet, palette = adafruit_imageload.load("/castle_sprite_sheet.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)


sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16,
                            default_tile = 1)

sprite2 = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16,
                            default_tile = 1)

sprite3 = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16,
                            default_tile = 1)


heart = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16,
                            default_tile = 2)

opponent = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16,
                            default_tile = 0)

opponent2 = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16,
                            default_tile = 0)

opponent3 = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16,
                            default_tile = 0)

# debug to find wich color is white
#for color in palette:
#    print(hex(color))
palette.make_transparent(16)

# Create the castle TileGrid
castle = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 5,
                            height = 5,
                            tile_width = 16,
                            tile_height = 16)

# Create a Group to hold the sprite and add it
sprite_group = displayio.Group()
sprite_group.append(sprite)

sprite2_group = displayio.Group()
sprite2_group.append(sprite2)

# Create a Group to hold the heart and add it

heart_group = displayio.Group(scale=1)
heart_group.append(heart)

oppo_group = displayio.Group(scale=1)
oppo_group.append(opponent)

oppo2_group = displayio.Group(scale=1)
oppo2_group.append(opponent2)

# Create a Group to hold the castle and add it
castle_group = displayio.Group(scale=3)
castle_group.append(castle)

# Create a Group to hold the sprite and castle
group = displayio.Group(max_size=6)

# game over screen
gameover_bitmap = displayio.Bitmap(240, 240, 2)
gameover_palette = displayio.Palette(2)
gameover_palette[0] = 0x000000
gameover_palette[1] = 0xffffff

gameover_screen = displayio.TileGrid(gameover_bitmap, pixel_shader=gameover_palette)

gameover_group = displayio.Group()
gameover_group.append(gameover_screen)
gameover_text_group = displayio.Group(scale=3)

for i in range(0,240):
    for j in range(0,240):
        gameover_bitmap[j, i] = 0

text_area_game = label.Label(font, text="GAME  ", color=0xffffff)
text_area_over = label.Label(font, text="   OVER", color=0xffffff)
gameover_text_group.append(text_area_game)
gameover_text_group.append(text_area_over)
gameover_group.append(gameover_text_group)

text_area_game.x = 5
text_area_game.y = 12
text_area_over.x = 5
text_area_over.y = 24
gameover_group.hidden = True

# everything for the score display

score_bitmap = displayio.Bitmap(224, 32, 4)

score_palette = displayio.Palette(4)
score_palette[0] = 0x111111
score_palette[1] = 0x000000
score_palette[2] = 0xffffff
score_palette[3] = 0xff0000
score_palette.make_transparent(0)

scores = displayio.TileGrid(score_bitmap, pixel_shader=score_palette)

text_area1 = label.Label(font, text="0", color=0xffffff, max_glyphs=2)
text_area2 = label.Label(font, text="0", color=0xffffff, max_glyphs=2)
text_area3 = label.Label(font, text="lvl.", color=0xdddddd)
text_area4 = label.Label(font, text="1", color=0xffffff, max_glyphs=2)
text_group = displayio.Group()
text1_group = displayio.Group(scale=2)
text1_group.append(text_area1)
text2_group = displayio.Group(scale=2)
text2_group.append(text_area2)
text3_group = displayio.Group()
text3_group.append(text_area3)
text4_group = displayio.Group(scale=2)
text4_group.append(text_area4)
text_group.append(text1_group)
text_group.append(text2_group)
text_group.append(text3_group)
text_group.append(text4_group)

score_group = displayio.Group(max_size=5)
score_group.append(scores)
score_group.append(sprite3)
score_group.append(opponent3)
score_group.append(text_group)


for i in range(0,32):
    for j in range(0,224):
        if i < 3 or i > 29:
            score_bitmap[j, i] = 2
        elif j < 3 or j > 221:
            score_bitmap[j, i] = 2
        else:
            score_bitmap[j, i] = 0


# Add the sprite and castle to the group
group.append(castle_group)
group.append(score_group)
group.append(heart_group)
group.append(oppo_group)
group.append(sprite_group)
#group.append(gameover_group)

# Same for second display

castle2 = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 5,
                            height = 5,
                            tile_width = 16,
                            tile_height = 16)
castle2_group = displayio.Group(scale=3)
castle2_group.append(castle2)

group2 = displayio.Group()
group2.append(castle2_group)
group2.append(oppo2_group)
oppo2_group.hidden = True
group2.append(sprite2_group)
sprite2_group.hidden = True

# Castle tile assignments
# corners
castle[0, 0] = 3  # upper left
castle2[4, 0] = 5  # upper right
castle[0, 4] = 9  # lower left
castle2[4, 4] = 11 # lower right
# top / bottom walls
for x in range(1, 5):
    castle[x, 0] = 4  # top
    castle[x, 4] = 10 # bottom
    castle2[x-1, 0] = 4  # top
    castle2[x-1, 4] = 10  # bottom
# left/ right walls
for y in range(1, 4):
    castle[0, y] = 6 # left
    castle2[4, y] = 8 # right
# floor
for x in range(1, 5):
    for y in range(1, 4):
        castle[x, y] = 7 # floor
        castle2[x-1,y] = 7 # floor

# put the sprite somewhere in the castle
sprite.x = 112
sprite.y = 48

sprite2.x = 112
sprite2.y = 48

opponent.x = 112
opponent.y = 176

opponent2.x = 112
opponent2.y = 176

# put randomly the heart (on the line between player and opponent).

heart.x = randint(48, 224)
heart.y = 112

# Place score panel

scores.x = 8
scores.y = 8
#icons for player and opponent.
sprite3.x = 16
sprite3.y = 16
opponent3.x = 80
opponent3.y = 16
#text areas
#scores
text_area1.x = 22
text_area1.y = 12
text_area2.x = 52
text_area2.y = 12
# lvl
text_area3.x = 180
text_area3.y = 26
text_area4.x = 105
text_area4.y = 12

# Add the Groups to the Displays
display1.show(group)
display2.show(group2)

# some variable holding states

active_sprite = 0
act_sp = sprite
active_heart = 0
active_oppo = 0
act_op = opponent

# score, level etc.

score_player = 0
score_opponent = 0
level = 1

# Reaction time

reaction = False
reaction_max = 1.8

# Game over
gameover = False

# start time
start_time = time.monotonic()
# Loop forever

while True:
    loop_start_time = time.monotonic()
    coll_wall_y_t = False
    coll_wall_y_b = False
    coll_wall_x_l = False
    coll_wall_x_r = False

    # angle et valeur absolue de z ( 10 = écran a plat, 0 = écran debout)
    angle, z = get_angle()
    movement = False
    speed = 0
    if z > 9.67:
        # print ("do nothing, z =", z)
        delta_x = 0
        delta_y = 0
        movement = False
    else:
        if z > 9:
            speed = 1
        elif z > 6:
            speed = 4
        elif z > 4:
            speed = 7
        else:
            speed = 10
        delta_x = (4 + speed) * math.sin(math.radians(angle))
        delta_y = (-4 - speed) * math.cos(math.radians(angle))

        if act_sp.y + math.ceil(delta_y) < 48:
            coll_wall_y_t = True
        elif act_sp.y + math.ceil(delta_y) > 176:
            coll_wall_y_b = True
        if active_sprite == 0:
            if sprite.x + math.ceil(delta_x) < 48:
                coll_wall_x_l = True
        else:
            if sprite2.x + math.ceil(delta_x) > 176:
                coll_wall_x_r = True
        movement = True
    # opponent movement.

    if active_heart == active_oppo:
        x_heart = act_op.x - heart.x
        y_heart = act_op.y - heart.y
    elif active_oppo == 0:
        x_heart = act_op.x - heart.x - 240
        y_heart = act_op.y - heart.y
    else:
        x_heart = act_op.x - heart.x + 240
        y_heart = act_op.y - heart.y

    op_angle = math.degrees(math.atan2(y_heart,x_heart)) + 90.0

    if op_angle < 0:
        op_angle = op_angle + 360.0

    delta_op_x = (-1 - level) * math.sin(math.radians(op_angle))
    delta_op_y = (1 + level) * math.cos(math.radians(op_angle))

    # apply deltas if required to generate movement.
    if coll_wall_x_l:
        sprite.x = 48
        if coll_wall_y_b or coll_wall_y_t:
            movement = False
    elif coll_wall_x_r:
        sprite2.x = 176
    else:
        act_sp.x += math.ceil(delta_x)
    if coll_wall_y_t:
        act_sp.y = 48
    elif coll_wall_y_b:
        act_sp.y = 176
    else:
        act_sp.y += math.ceil(delta_y)
    #movement of opponent
    if reaction == False:
        act_op.x += math.ceil(delta_op_x)
        act_op.y += math.ceil(delta_op_y)
    else:
        now = time.monotonic()
        if now - start_reaction > max(reaction_max - (level*0.1), 0.5):
            reaction = False
    # display change
    if active_sprite == 0:
        if sprite.x > 224:
            if sprite.x > 240:
                # changing active sprite
                active_sprite = 1
                act_sp = sprite2
                sprite2_group.hidden = False
                sprite2.y = sprite.y
                sprite2.x = 0
                sprite_group.hidden = True
            else:
                # make sprite2 visible tied to sprite.y
                sprite2_group.hidden = False
                sprite2.y = sprite.y
                sprite2.x = sprite.x - 240
    elif active_sprite == 1:
        if sprite2.x < 0:
            if sprite2.x < -16:
                #changing active sprite
                active_sprite = 0
                act_sp = sprite
                sprite_group.hidden = False
                sprite.y = sprite2.y
                sprite.x = 224
                sprite2_group.hidden = True
            else:
                # make sprite visible tied to sprite2.y
                sprite_group.hidden = False
                sprite.y = sprite2.y
                sprite.x = 240 + sprite2.x
    else:
        print ("Error !!! active_sprite =", active_sprite)
    # Same for opponent
    if active_oppo == 0:
        if opponent.x > 224:
            if opponent.x > 240:
                # changing active sprite
                active_oppo = 1
                act_op = opponent2

                oppo2_group.hidden = False
                opponent2.y = opponent.y
                opponent2.x = 0
                oppo_group.hidden = True
            else:
                # make sprite2 visible tied to sprite.y
                oppo2_group.hidden = False
                opponent2.y = opponent.y
                opponent2.x = opponent.x - 240
    elif active_oppo == 1:
        if opponent2.x < 0:
            if opponent2.x < -16:
                #changing active sprite
                active_oppo = 0
                act_op = opponent
                oppo_group.hidden = False
                opponent.y = opponent2.y
                opponent.x = 224
                oppo2_group.hidden = True
            else:
                # make sprite visible tied to sprite2.y
                oppo_group.hidden = False
                opponent.y = opponent2.y
                opponent.x = 240 + opponent2.x
    else:
        print ("Error !!! active_oppo =", active_oppo)
    # collision detection
    # player vs opponent
    if active_sprite == active_oppo:
        if collision(act_op, act_sp):
            act_op.x = act_op.x - math.ceil(delta_op_x) + math.ceil(delta_x)
            act_op.y = act_op.y - math.ceil(delta_op_y) + math.ceil(delta_y)
            act_sp.x = act_sp.x - math.ceil(delta_x) + math.ceil(delta_op_x)
            act_sp.y = act_sp.y - math.ceil(delta_y) + math.ceil(delta_op_y)
    # player vs heart
    if movement and active_sprite == active_heart:
        if collision(act_sp, heart):
            reset_heart()
            score_player += 1
            text_area1.text = str(score_player)
            start_reaction = time.monotonic()
            reaction = True
            #print("Collision with heart !")
    # opponent vs heart
    if active_oppo == active_heart:
        if collision(act_op, heart):
            reset_heart()
            score_opponent += 1
            text_area2.text = str(score_opponent)
            start_reaction = time.monotonic()
            reaction = True
    if score_player > 9:
        # level up
        score_player = 0
        score_opponent = 0
        text_area1.text = "0"
        text_area2.text = "0"
        level += 1
        print("level up :", level)
        text_area4.text = str(level)
    if score_opponent > 9:
        gameover = True
        print("Game Over")
        print("Level", level)
        print("Score :", score_player, "-", score_opponent)
        group.append(gameover_group)
        gameover_group.hidden = False
        while True:
            if ss.digital_read(9) == False or ss.digital_read(10) == False or ss.digital_read(11) == False:
                reinitialize_game()
                break
            else:
                show_game_over()
                time.sleep(.01)
                pass
    time.sleep(0.07)
