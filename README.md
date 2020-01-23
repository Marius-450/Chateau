# Chateau

Little game for the Monster M4sk. Catch the heart before Blinka

### Requirements 

#### Material 
* a Monster M4sk board (from adafruit)

#### Libs

* adafruit_lis3dh
* adafruit_imageload
* adafruit_st7789
* adafruit_seesaw
* adafruit_display_text

### Controls / Gameplay

* You are the robot(Adabot), your goal is to catch the heart before the snake (Blinka).
* Tilt the board to make the robot move. Tilt more equals more speed.
* Collisions "bump" the opponents : they exchange velocity and heading angle. (so from behind, you just push it and it slow you down)
* Each time you reach 10 points, you level-up : scores are back to 0-0, Blinka speed-up a little and wait less when the heart move.
* When Blinka reach 10 pts, it's **game over**. Click any of the 3 top-right buttons to reset the game.


### TODO 

* A Boss level. *Currently working on it*
* Power-ups
* A welcome screen 
* Extending game over screen to the 2nd display
* Sounds *(Got a bug with that)*

### Known Issues

* When steping between the 2 displays, if the sprite go back to the display it come from, the sprite ont the other display may not be hidden correctly
* Sounds not working

### Misc

I got a lot of fun with this project learning about moving things, tilegrids, collision detection, and games mechanics. 

