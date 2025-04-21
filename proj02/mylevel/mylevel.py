#!/usr/bin/python3

# Important Libraries
import pyglet

# Our own Game Libraries
import sprites, config

# SI460 Level Definition
class Level:
    def __init__(self, sprites, hero, enemies=[]):

        # Create the Background, this is one method of creating images,
        # we will work with multiple methods.
        # Take a look at how this is drawn in the on_draw function
        # and the self.background.blit method.
        self.background   = pyglet.resource.image(config.background)
        self.background_x = 0
        self.background_y = 0

        # Store the loaded sprites and hero
        self.sprites = sprites
        self.hero    = hero
        self.enemies = enemies

        # Music in the Background
        self.backgroundMusic = pyglet.media.Player()
        self.backgroundMusic.queue(pyglet.media.load(config.background_music, streaming=True))
        self.backgroundMusic.eos_action = 'loop'
        self.backgroundMusic.loop = True
        self.backgroundMusic.play()

    # Here is a complete drawBoard function which will draw the terrain.
    # Lab Part 1 - Draw the board here

    # {0: {0: <ImageData 128x128>, 1: <ImageData 128x128>, 2: <ImageData 128x128>, 3: <ImageData 128x128>, 4: <ImageData 128x128>, 5: <ImageData 128x128>, 6: <ImageData 128x128>, 7: <ImageData 128x128>, 8: <ImageData 128x128>, 9: <ImageData 128x128>, 10: <ImageData 128x128>, 11: <ImageData 128x128>}, 
    # 1: {0: <ImageData 128x128>, 1: <ImageData 128x128>, 2: <ImageData 128x128>, 3: <ImageData 128x128>, 4: <ImageData 128x128>, 5: <ImageData 128x128>, 6: <ImageData 128x128>, 7: <ImageData 128x128>, 8: <ImageData 128x128>, 9: <ImageData 128x128>, 10: <ImageData 128x128>, 11: <ImageData 128x128>}, 
    # 2: {0: <ImageData 128x128>, 1: <ImageData 128x128>}, 
    # 3: {0: <ImageData 128x128>, 1: <ImageData 128x128>}, 
    # 5: {3: <ImageData 128x93>, 4: <ImageData 128x93>}, 
    # 7: {6: <ImageData 128x93>, 7: <ImageData 128x93>, 8: <ImageData 128x93>, 9: <ImageData 128x93>, 10: <ImageData 128x93>, 11: <ImageData 128x93>, 12: <ImageData 128x93>, 13: <ImageData 128x93>, 14: <ImageData 128x93>}, 
    # 10: {12: <ImageData 128x93>, 13: <ImageData 128x93>}}

    def drawBoard(self, level, delta_x=0, delta_y=0, height=50, width=50):
        # iterate through the level dictionary and blit all the images to the screen
        for yAxis, innerLevel in level.items():
            for xAxis, image in innerLevel.items():
                sprite = pyglet.sprite.Sprite(image, xAxis*width, yAxis*height)
                sprite.scale_x = width/image.width
                sprite.scale_y = height/image.height
                sprite.draw()


    def draw(self, t=0, width=800, height=600, keyTracking={}, mouseTracking=[], *other):

        # Draw the game background
        if self.background.width < width:
            self.background.blit(self.background_x,self.background_y,height=height,width=width)
        else:
            self.background.blit(self.background_x,self.background_y,height=height)

        # Draw the gameboard
        self.drawBoard(config.level, 0, 0, config.height, config.width)

        # Draw the enemies
        for enemy in self.enemies:
            enemy.draw(t)

        # Draw the hero.
        self.hero.draw(t, keyTracking)

# Load all game sprites
print('Loading Sprites...')
gameSprites = sprites.loadAllImages(config.spritespath)

# Load in the hero
print('Loading the Hero...')
from player import Player
hero = Player(gameSprites,
              sprites.buildSprite,
              "hero", "Idle", "Right",
              config.playerSpriteSpeed,
              config.playerSpriteScale,
              True,
              config.playerStartCol * config.width,
              config.playerStartRow * config.height)

# Load in the Enemies
print('Loading the Enemies...')
enemies = []

# provide the level to the game engine
print('Starting level:', config.levelName)
level = Level(gameSprites, hero, enemies)