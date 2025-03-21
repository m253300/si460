#!/usr/bin/python3

# Important Libraries
import pyglet

# Our Hero Class
class Player:
    def __init__(self, sprites={}, buildSprite=None, playerClass="hero", mode="Run", facing="Right", speed=0.05, scale=0.15, loop=True, x=380, y=250):

        # Store the sprites, and the sprite building function
        self.sprites = sprites
        self.buildSprite = buildSprite

        # Some basic settings
        self.animationSpeed = speed
        self.animationScale = scale
        self.animationLoop = loop
        self.animationX = x
        self.animationY = y
        self.playerClass = playerClass
        self.mode = mode
        self.facing = facing

        # Build the initial character
        self.playerSprite = self.buildSprite(self.sprites,
                                             self.playerClass,
                                             self.mode,
                                             self.facing,
                                             self.animationSpeed,
                                             self.animationScale,
                                             self.animationLoop,
                                             self.animationX,
                                             self.animationY)

    def draw(self, t=0, *other):
        if self.playerSprite is not None:
            self.playerSprite.draw()
        else:
            print('DEBUG: You need to complete the functions in sprites.py')
