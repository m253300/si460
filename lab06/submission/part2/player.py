#!/usr/bin/python3

# Important Libraries
import pyglet

# Our Hero Class
class Player:
    def __init__(self, x=380, y=250, flip_x=False):
        self.speed = 0.05
        self.scale = 0.15
        self.loop = True

        # Example sprite building...
        # --- What a horrible way of loading in images ---
        # --- There must be a better way ---
        # --- Possibly a good Lab problem, hmmm.... ---
        a = pyglet.resource.image('mylevel/sprites/hero/Attack (1).png', flip_x)
        b = pyglet.resource.image('mylevel/sprites/hero/Attack (2).png', flip_x)
        c = pyglet.resource.image('mylevel/sprites/hero/Attack (3).png', flip_x)
        d = pyglet.resource.image('mylevel/sprites/hero/Attack (4).png', flip_x)
        e = pyglet.resource.image('mylevel/sprites/hero/Attack (5).png', flip_x)
        f = pyglet.resource.image('mylevel/sprites/hero/Attack (6).png', flip_x)
        g = pyglet.resource.image('mylevel/sprites/hero/Attack (7).png', flip_x)
        h = pyglet.resource.image('mylevel/sprites/hero/Attack (8).png', flip_x)
        i = pyglet.resource.image('mylevel/sprites/hero/Attack (9).png', flip_x)
        j = pyglet.resource.image('mylevel/sprites/hero/Attack (10).png',flip_x)

        # We can change the anchor point of an image, by setting it's x and y
        # anchor values, example:
        # a.anchor_x = a.width / 2.0

        # Retrieve the appropriate sequence of images from the sprite dictionary
        self.playerSequence = [a,b,c,d,e,f,g,h,i,j]

        # Some basic settings
        self.animationSpeed = self.speed
        self.animationScale = self.scale
        self.animationLoop = self.loop
        self.animationX = x
        self.animationY = y

        # Build the pyglet animation sequence
        self.playerAnimation = pyglet.image.Animation.from_image_sequence(self.playerSequence,
                                                                          self.animationSpeed,
                                                                          self.animationLoop)
        # Create the sprite from the animation sequence
        self.playerSprite = pyglet.sprite.Sprite(self.playerAnimation,
                                                 x=self.animationX,
                                                 y=self.animationY)
        # Set the player's scale
        self.playerSprite.scale = self.animationScale

    def draw(self, t=0, *other):
        self.playerSprite.draw()

objects = [Player(), Player(280, 250, True)]
