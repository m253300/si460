#!/usr/bin/python3

# Get the name of this .py file, since we should be able to assume
# that the files are in the same directory!
levelName = __file__.split('/')[-1].split('.py')[0]
background = levelName + "/backgrounds/level1.png"
spritesLocation = levelName + "/sprites"

# Important Libraries
import pyglet

# Game Libraries
import sprites

# SI460 Level Definition
class Level:
    def __init__(self, background, sprites, hero, enemies=[]):

        # Create the Background, this is one method of creating images,
        # we will work with multiple methods.
        # Take a look at how this is drawn in the on_draw function
        # and the self.background.blit method.
        self.background = pyglet.resource.image(background)
        self.background_x = 0
        self.background_y = 0

        # Store the loaded sprites and hero
        self.sprites = sprites
        self.hero = hero
        self.enemies = enemies

    def draw(self, t=0, width=800, height=600, *other):

        # Draw the game background
        if self.background.width < width:
            self.background.blit(self.background_x,self.background_y,height=height,width=width)
        else:
            self.background.blit(self.background_x,self.background_y,height=height)

        # Draw the hero.
        self.hero.draw(t)

        # Draw the enemies
        for enemy in self.enemies:
            enemy.draw(t)

# Load all game sprites
print('Loading Sprites...')
gameSprites = sprites.loadAllImages(spritesLocation)

# Load in the hero
print('Loading the Hero...')
from player import Player
#playerClass="hero", mode="Run", facing="Right", speed=0.05, scale=0.15
hero = Player(gameSprites, sprites.buildSprite, "hero", "Attack")

# Load in the Enemies
print('Loading the Enemies...')
enemy1 = Player(gameSprites, sprites.buildSprite, "enemy-1", "Attack", "Right", 0.05, 0.15, True, 300)
enemy2 = Player(gameSprites, sprites.buildSprite, "enemy-2", "Attack", "Left", 0.05, 0.15, True, 540)
enemies = [enemy1, enemy2]

# provide the level to the game engine
print('Starting level:', levelName)
level = Level(background, gameSprites, hero, enemies)
