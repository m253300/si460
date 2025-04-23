#!/usr/bin/python3

# Important Libraries
import pyglet, config
from pyglet.window import key

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

    # I asked gemini to rewrite this to make use of config.keyMappings and this is the result from promp 1 and 1.5 in ai.txt
    def movement(self, t=0, keyTracking={}):
        velocity = 0
        direction = None  # Initialize direction
        actions = set()    # Use a set to store actions

        if len(keyTracking) != 0:
            for pressed_key in keyTracking:
                action = config.keyMappings[pressed_key]
                if action:  # Only process valid actions
                    actions.add(action)

            if 'run' in actions:
                velocity = 9
            else:
                velocity = 3

            if 'left' in actions:
                direction = "Left"
                if self.mode != "Run" or self.facing != "Left":
                    self.changeSprite("Run", "Left")
                else:
                    self.playerSprite.x -= velocity
            elif 'right' in actions:
                direction = "Right"
                if self.mode != "Run" or self.facing != "Right":
                    self.changeSprite("Run", "Right")
                else:
                    self.playerSprite.x += velocity

        if direction is None and self.mode != "Idle":
            self.changeSprite("Idle")
        
    # Draw our character
    def draw(self, t=0, keyTracking={}, *other):
        self.movement(t, keyTracking)
        self.playerSprite.draw()
