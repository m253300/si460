#!/usr/bin/python3

# Important Libraries
import config, numpy, math, pyglet

# Our Hero Class
class Kunai:
    def __init__(self, sprites={},
                       buildSprite=None,
                       playerClass="weapon",
                       mode="Kunai",
                       facing="Right",
                       speed=0.05,
                       scale=0.15,
                       loop=False,
                       x=380,
                       y=250,
                       time=0):
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
        self.changeSprite(self.mode, self.facing)

        # set up the foundations for the character movement
        self.position = numpy.array([self.playerSprite.x, self.playerSprite.y])
        self.pixels = numpy.array([config.pixels_per_meter, config.pixels_per_meter])
        self.acceleration = numpy.array([0, config.gravity])
        self.velocity = numpy.array([0, 0])
        # this will be set to the time in movement when a button is pressed
        # if 'left' is triggered at world time 11.6 seconds then this will be set to 11.6 and in the movement function it will calculate time as time = worldtime-self.time to determine how long the movement has been occuring
        # this will be needed for gravity and jumping most importantly
        self.time = time

        self.acceleration = numpy.array([0, 0])
        xVel = 3
        if self.facing == 'Left':
            xVel = -3
        self.velocity = numpy.array([xVel, 0])

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
    def movement(self, t=0, keyTracking={}):
        self.updateLocation(t)

    def updateLocation(self, t):
        time = t - self.time
        position = self.position + self.pixels * ( self.velocity * time ) + self.pixels * ( 0.5 * self.acceleration * time * time )
        self.playerSprite.x = position[0]

    # Draw our character
    def draw(self, t=0, keyTracking={}, *other):
        self.movement(t, keyTracking)
        self.playerSprite.draw()