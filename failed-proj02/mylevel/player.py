#!/usr/bin/python3

# Important Libraries
import config, math, numpy

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

        # set up the foundations for the character movement
        self.position = numpy.array([self.playerSprite.x, self.playerSprite.y])
        self.pixels = numpy.array([config.pixels_per_meter, config.pixels_per_meter])
        self.acceleration = numpy.array([0, config.gravity])
        self.velocity = numpy.array([0, 0])
        # this will be set to the time in movement when a button is pressed
        # if 'left' is triggered at world time 11.6 seconds then this will be set to 11.6 and in the movement function it will calculate time as time = worldtime-self.time to determine how long the movement has been occuring
        # this will be needed for gravity and jumping most importantly
        self.time = 0 

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

    # I asked gemini to rewrite this to make use of config.keyMappings and this is the result from promp 1 and 1.5 in ai.txt with modifications
    def movement(self, t=0, keyTracking={}):
        velocity = 0
        direction = None  # Initialize direction
        actions = set()    # Use a set to store actions

        if len(keyTracking) != 0:
            for pressed_key in keyTracking:
                if pressed_key in config.keyMappings:
                    actions.add(config.keyMappings[pressed_key])

            if 'run' in actions:
                velocity = 10
            else:
                velocity = 5

            if 'left' in actions and 'right' in actions:
                self.changeSprite("Idle")
            elif 'left' in actions:
                direction = "Left"
                if self.mode != "Run" or self.facing != "Left":
                    self.changeSprite("Run", "Left")
                else: 
                    velocity *= -1
                    velocity = self.levelCollision(velocity)
                    self.playerSprite.x += velocity
            elif 'right' in actions:
                direction = "Right"
                if self.mode != "Run" or self.facing != "Right":
                    self.changeSprite("Run", "Right")
                else:
                    velocity = self.levelCollision(velocity)
                    self.playerSprite.x += velocity
            elif 'jump' in actions:
                direction = "Right"
                self.changeSprite("Attack", "Right")
        if direction is None and self.mode != "Idle":
            self.changeSprite("Idle")

        self.applyGravity()
        
    # Draw our character
    def draw(self, t=0, keyTracking={}, *other):
        self.movement(t, keyTracking)
        self.playerSprite.draw()

    # i need to turn this into a true/false return so that if level collision occurs then it returns false, otherwise true
    def levelCollision(self, velocity):
        # Player values': x & y position, sprite width
        px = self.playerSprite.x+velocity
        py = self.playerSprite.y
        pwidth = self.playerSprite.width

        leftColActual = (px-pwidth/2)/config.width
        leftColRounded = math.floor(leftColActual)
        rightColActual = (px+pwidth/2)/config.width
        rightColRounded = math.floor(rightColActual)
        
        # determine row at which the player's lower is located on the level grid
        rowLow = math.floor(py/config.height)
        if rowLow-1 < 0:
            rowLow = 1

        # DEBUG
        # print("------------------")
        # print(f"leftActual: {leftColActual}, leftRounded: {leftColRounded}")
        # print(f"rightActual: {rightColActual}, rightRounded: {rightColRounded}")

        canMoveLeft = (velocity < 0 and leftColRounded not in config.level[rowLow].keys() and leftColActual >= leftColRounded-1)
        canMoveRight = (velocity > 0 and rightColRounded not in config.level[rowLow].keys() and rightColActual <= rightColRounded+1)

        if canMoveLeft or canMoveRight:
            return velocity
        else:
            return 0

    def applyGravity(self):
        g = config.gravity
        px = self.playerSprite.x
        py = self.playerSprite.y
        row = py/config.height
        # prevents crashing when character falls too low
        rowLow = math.floor(py/config.height)
        if rowLow-1 < 0:
            rowLow = 1
        pwidth = self.playerSprite.width
        leftColActual = (px-pwidth/2)/config.width
        leftColRounded = math.floor(leftColActual)
        rightColActual = (px+pwidth/2)/config.width
        rightColRounded = math.floor(rightColActual)

        # get leftCol and rightCol
        # if either one is on solid ground, then do not fall
        # if both are not then fall until row == rowLow
        # if there is not object below character then drop them

        # true if object below left foot
        groundOnLeft = leftColRounded in config.level[rowLow-1].keys() 

        # check right food
        # true if object below right foot
        groundOnRight = rightColRounded in config.level[rowLow-1].keys() 

        if (not groundOnLeft and not groundOnRight) or row != rowLow:
            self.changeSprite("Glide")
            self.playerSprite.y -= g