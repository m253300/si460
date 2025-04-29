#!/usr/bin/python3

# Important Libraries
import pyglet

# Our own Game Libraries
import sprites, config
from enemy1 import Enemy1
from enemy2 import Enemy2

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
        # self.sound = pyglet.media.Player()
        # self.sound.queue(pyglet.media.load(config.background_music, streaming=True))
        # self.sound.eos_action = 'loop'
        # self.sound.loop = True
        # self.sound.play()
        # self.soundPlaying = True

    # Here is a complete drawBoard function which will draw the terrain.
    # Lab Part 1 - Draw the board here
    def drawBoard(self, level, delta_x=0, delta_y=0, height=50, width=50):
        for row in level.keys():
            for col in level[row].keys():
                level[row][col].anchor_x = 0
                level[row][col].anchor_y = 0
                level[row][col].blit(col*width+delta_x,row*height+delta_y, height=height, width=width)

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

        for x in config.kunai:
            if x.playerSprite.x > width:
                config.kunai.remove(x)
            else:
                x.draw(t)

        if self.hero.flags['dead']:
            label = pyglet.text.Label('You Died',
                    font_name='Times New Roman',
                    font_size=60,
                    x=width/2, y=height/2,
                    color = (255, 0, 0, 255),
                    anchor_x='center', anchor_y='center')
            label.draw()

# Load all game sprites
print('Loading Sprites...')
gameSprites = sprites.loadAllImages(config.spritespath)

# Load in the hero
print('Loading the Hero...')
from player import Player
hero = Player(gameSprites,
              sprites.buildSprite,
              "hero", "Attack", "Right",
              config.playerSpriteSpeed,
              config.playerSpriteScale,
              True,
              config.playerStartCol * config.width - 0.5 * config.width,
              config.playerStartRow * config.height * 1.02)

# Load in the Enemies
print('Loading the Enemies...')
# must go through config.enemies in a for loop and put the correct enemy in the correct location
enemies = []
for e in config.enemies:
    if e[2] == 'e1':
        enemies.append(Enemy1(gameSprites,
                          sprites.buildSprite,
                          'enemy-1', 'Idle', 'Left',
                          config.playerSpriteSpeed,
                          config.playerSpriteScale,
                          True,
                          e[0] * config.width - 0.5 * config.width,
                          e[1] * config.height))
    elif e[2] == 'e2':
        enemies.append(Enemy2(gameSprites,
                          sprites.buildSprite,
                          'enemy-2', 'Idle', 'Left',
                          config.playerSpriteSpeed,
                          config.playerSpriteScale,
                          True,
                          e[0] * config.width - 0.5 * config.width,
                          e[1] * config.height))

# provide the level to the game engine
print('Starting level:', config.levelName)
level = Level(gameSprites, hero, enemies)
