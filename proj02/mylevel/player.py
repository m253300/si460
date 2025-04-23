#!/usr/bin/python3

# Important Libraries
import pyglet, config, math

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

    # I asked gemini to rewrite this to make use of config.keyMappings and this is the result from promp 1 and 1.5 in ai.txt with slight tweaks
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
                    # change to elif !levelCollision(velocity)... but then where would i check for enemy collision????
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

        if direction is None and self.mode != "Idle":
            self.changeSprite("Idle")

        self.applyGravity()
        
    # Draw our character
    def draw(self, t=0, keyTracking={}, *other):
        self.movement(t, keyTracking)
        self.playerSprite.draw()

    def levelCollision(self, velocity):
        # Player values': x & y position, sprite width
        px = self.playerSprite.x+velocity
        py = self.playerSprite.y
        pwidth = self.playerSprite.width

        roundCol = config.round(px/config.width)
        leftCol = (px-pwidth/2)/config.width
        rightCol = (px+pwidth/2)/config.width
        
        # determine row at which the player's lower is located on the level grid
        rowLow = math.floor(py/config.height)
        if rowLow-1 < 0:
            rowLow = 1

        canMoveLeft = (velocity < 0 and roundCol-1 not in config.level[rowLow].keys() and leftCol > roundCol)
        canMoveRight = (velocity > 0 and roundCol not in config.level[rowLow].keys() and rightCol < roundCol)

        if canMoveLeft or canMoveRight:
            return velocity
        else:
            return 0

    def applyGravity(self):
        g = config.gravity
        px = self.playerSprite.x
        py = self.playerSprite.y
        row = py/config.height
        rowLow = math.floor(py/config.height)
        realCol = px/config.width
        roundCol = config.round(px/config.width)
        pwidth = self.playerSprite.width
        leftCol = (px-pwidth/2)/config.width
        rightCol = (px+pwidth/2)/config.width

        # get leftCol and rightCol
        # if either one is on solid ground, then do not fall
        # if both are not then fall until row == rowLow

        # prevents crashing when character falls out too low
        if rowLow-1 < 0:
            rowLow = 1

        print(f"row: {row}, rowLow: {rowLow}")
        print(f"col: {realCol}, roundCol: {roundCol}")
        print(f"leftCol: {leftCol}, rightCol: {rightCol}")

        #if there is not object below character then drop them
        #print(config.level[rowLow-1])
        if roundCol-1 not in config.level[rowLow-1].keys() or row != rowLow:
            self.playerSprite.y -= g