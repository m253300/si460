#!/usr/bin/python3

# Important Libraries
import pyglet, config

# Our Hero Class
class Player:
    def __init__(self, sprites={},
                       buildSprite=None,
                       playerClass="hero",
                       mode="Run",
                       facing="Right",
                       speed=0.05,
                       scale=0.15,
                       loop=True,
                       x=380,
                       y=250):

        # Store the sprites, and the sprite building function
        self.sprites      = sprites
        self.buildSprite  = buildSprite
        self.playerSprite = None

        # Some basic settings
        self.animationSpeed = speed
        self.animationScale = scale
        self.animationLoop  = loop
        self.animationX     = x
        self.animationY     = y
        self.playerClass    = playerClass
        self.mode           = mode
        self.facing         = facing

        # Build the starting character sprite
        self.changeSprite()

    # Build the initial character
    def changeSprite(self, mode=None, facing=None):
        if mode is not None:
            self.mode = mode
        if facing is not None:
            self.facing = facing
        if self.playerSprite is not None:
            self.animationX = self.playerSprite.x
            self.animationY = self.playerSprite.y
        self.playerSprite = self.buildSprite(self.sprites,
                                             self.playerClass,
                                             self.mode,
                                             self.facing,
                                             self.animationSpeed,
                                             self.animationScale,
                                             self.animationLoop,
                                             self.animationX,
                                             self.animationY)

    # Move the character
    #left arrow   65361  
    #right arrow  65363  
    #left shift   65505  
    #right shift  65506 
    def movement(self, t=0, keyTracking={}):
        keys = keyTracking.keys()
        velocity = 0

        if len(keyTracking) != 0:
            if 65505 in keys or 65506 in keys:
                velocity = 9
            else:
                velocity = 3

            if 65361 in keys:
                if self.mode != "Run" or self.facing != "Left":
                    self.changeSprite("Run", "Left")
                else:
                    self.playerSprite.x = self.playerSprite.x - velocity
            elif 65363 in keys:
                if self.mode != "Run" or self.facing != "Right":
                    self.changeSprite("Run", "Right")
                else:
                    self.playerSprite.x = self.playerSprite.x + velocity
        elif self.mode != "Idle":
            self.changeSprite("Idle")
        
    # Draw our character
    def draw(self, t=0, keyTracking={}, *other):
        self.movement(t, keyTracking)
        self.playerSprite.draw()
