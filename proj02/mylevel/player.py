#!/usr/bin/python3

# Important Libraries
import config, numpy, math, pyglet

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
        self.timeFalling = 0
        # this will keep track of the current action and will be needed for jumping and possibly other animations unless I am just stupid and need better conditionals because the self.mode already exists
        self.flags = {'jumping'   : False,
                      'falling'   : False,
                      'dead'      : False,
                      'attacking' : False,
                      'throwing'  : False}
        self.health = 3
        self.timeDamageWasTaken = 0
        self.timeAttackStarted = 0

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

        if self.health <= 0 and not self.flags['dead']:
            self.flags['dead'] = True
            self.animationLoop = False
            self.changeSprite('Dead', self.facing)

        elif self.health > 0:
            if t - self.timeAttackStarted > 0.65:
                self.flags['attacking'] = False
                self.flags['throwing'] = False

            modes = []
            if keyTracking != {}:
                for key in keyTracking:
                    if key in config.keyMappings:
                        modes.append(config.keyMappings[key])

            if not self.flags['jumping'] and not self.flags['attacking'] and not self.flags['throwing']:
                if 'right' in modes:
                    if 'run' in modes and self.velocity[0] != 9:
                        self.time = t
                        self.position[0] = self.playerSprite.x
                        self.velocity[0] = 9
                    if 'run' not in modes and self.velocity[0] == 9:
                        self.velocity[0] = 3
                        self.time = t
                        self.position[0] = self.playerSprite.x
                    if self.mode != 'Run' or self.facing != 'Right':
                        self.velocity[0] = 3
                        self.time = t
                        self.position[0] = self.playerSprite.x
                        self.changeSprite('Run', 'Right')

                elif 'left' in modes:
                    if 'run' in modes and self.velocity[0] != -9:
                        self.velocity[0] = -9
                        self.time = t
                        self.position[0] = self.playerSprite.x
                    if 'run' not in modes and self.velocity[0] == -9:
                        self.velocity[0] = -3
                        self.time = t
                        self.position[0] = self.playerSprite.x
                    if self.mode != 'Run' or self.facing != 'Left':
                        self.velocity[0] = -3
                        self.time = t
                        self.position[0] = self.playerSprite.x
                        self.changeSprite('Run', 'Left')

                elif self.mode != 'Idle' and modes == []:
                    # Set velocity to 0 since idle
                    self.time = t
                    self.velocity[0] = 0
                    self.position[0] = self.playerSprite.x
                    self.changeSprite('Idle', self.facing)

            if 'jump' in modes and not self.flags['jumping'] and self.onSolidGround(self.playerSprite.y-1):
                self.flags['jumping'] = True
                self.animationLoop = False
                self.changeSprite('Jump', self.facing)
                self.velocity[1] = 9

            if 'attack' in modes and not self.flags['attacking'] and not self.flags['jumping']:
                self.flags['attacking'] = True
                self.animationLoop = False
                self.velocity[0] = 0
                self.position[0] = self.playerSprite.x
                self.changeSprite('Attack', self.facing)
                self.timeAttackStarted = t

            if 'shoot' in modes and not self.flags['attacking'] and not self.flags['jumping'] and not self.flags['throwing']:
                self.flags['throwing'] = True
                self.animationLoop = False
                self.velocity[0] = 0
                self.position[0] = self.playerSprite.x
                self.changeSprite('Throw', self.facing)
                self.timeAttackStarted = t

            self.updateLocation(t)

        hp = ''
        for x in range(self.health):
            hp += "♥"
        label = pyglet.text.Label(hp,
                font_name='Times New Roman',
                font_size=20,
                x=self.playerSprite.x, y=self.playerSprite.y + self.playerSprite.height,
                color = (255, 0, 0, 255),
                anchor_x='center', anchor_y='bottom')
        label.draw()

    def ableToBeAttacked(self, t):
        if t - self.timeDamageWasTaken > 1:
            return True
        else:
            return False

    def updateLocation(self, t):
        # LATERAL MOVEMENT
        if self.canMoveLaterally():
            time = t - self.time
            position = self.position + self.pixels * ( self.velocity * time ) + self.pixels * ( 0.5 * self.acceleration * time * time )

            # prevents player from going off leftmost edge of screen
            if position[0] - self.playerSprite.width * 0.5 < 0:
                position[0] = 0
            else:
                self.playerSprite.x = position[0]
        else:
            if not self.isObstructedAbove():
                self.velocity[0] = 0
            self.position[0] = self.playerSprite.x

        # GRAVITY/DOWNWARD MOVEMENT
        time = t - self.timeFalling
        position = self.position + self.pixels * ( self.velocity * time ) + self.pixels * ( 0.5 * self.acceleration * time * time )
        if not self.onSolidGround(position[1]) and not self.flags['falling']:
            self.timeFalling = t
            self.position[1] = self.playerSprite.y
            self.flags['falling'] = True
        elif not self.onSolidGround(position[1]) and self.flags['falling']:
            if self.isObstructedAbove() and self.flags['jumping']:
                self.velocity[1] = 0
            else:
                self.playerSprite.y = position[1]
        else:
            self.timeFalling = 0
            self.flags['falling'] = False
            self.playerSprite.y = math.floor((self.playerSprite.y+self.playerSprite.height*0.25)/config.height)*config.height
            self.velocity[1] = 0
            self.flags['jumping'] = False
            self.animationLoop = True

        if self.playerSprite.y + self.playerSprite.height < 0:
            self.health = 0

    def isObstructedAbove(self):
        py = self.playerSprite.y
        oy = math.floor((py + (self.playerSprite.height * 0.75))/config.height)
        ox = math.floor(self.playerSprite.x/config.width)

        if oy in config.level and ox in config.level[oy]:
            return True
        else:
            return False
            

    # Returns True if player can move laterally/nothing is in the player's way. Returns False if unable to move/something is in the way
    def canMoveLaterally(self):
        py = self.playerSprite.y

        # ox is adjusted to account for the sprite anchor being in the center of the player sprite
        ox = None
        if self.facing == 'Right':
            ox = math.floor((self.playerSprite.x + self.playerSprite.width * 0.5)/config.width)
        else:
            ox = math.floor((self.playerSprite.x - self.playerSprite.width * 0.5)/config.width)
        oy = math.floor(py/config.height)
        oy2 = math.floor((py + (self.playerSprite.height * 0.75))/config.height)

        #check if there is an object in the next x position
        if (oy in config.level and ox in config.level[oy]) or (oy2 in config.level and ox in config.level[oy2]):
            return False
        return True
        
    # detects if the player is on solid ground and thus cannot fall. If the player is on solid ground and cannot fall, then returns true, otherwise returns false
    def onSolidGround(self, newY):
        # ox is adjusted to account for the sprite anchor being in the center of the player sprite
        oxLeft = math.floor((self.playerSprite.x - self.playerSprite.width * 0.3)/config.width)
        oxRight = math.floor((self.playerSprite.x + self.playerSprite.width * 0.3)/config.width)
        oy = math.floor((self.playerSprite.y)/config.height)
        oyNew = math.floor((newY)/config.height)

        if not self.flags['falling'] and ((oy not in config.level) or (oy in config.level and oxLeft not in config.level[oy] and oxRight not in config.level[oy])):
            return False
        elif self.flags['falling'] and ((oyNew not in config.level) or (oyNew in config.level and oxLeft not in config.level[oyNew] and oxRight not in config.level[oyNew])):
            return False
        else:
            return True

    # Draw our character
    def draw(self, t=0, keyTracking={}, *other):
        self.movement(t, keyTracking)
        self.playerSprite.draw()