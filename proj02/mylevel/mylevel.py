#!/usr/bin/python3

# Important Libraries
import pyglet
from pyglet.gl import glLoadIdentity, glTranslatef

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

        # calculate hitbox for the goal to win the game
        x = config.goalCol * config.width
        y = config.goalRow * config.height
        w = config.width
        h = config.height
        self.goalhb = (x-w, y+0.25*h), (x, y+0.75*h)

        self.scrollX = 0

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

        # Draw the objects
        self.drawBoard(config.objects, 0, 0, config.height, config.width)

        # check if hero intersects with goal and then display win label and freeze game
        if intersect(hero.getHitbox(), self.goalhb):
            config.flags['endgame'] = True
            keyTracking = {}
            label = pyglet.text.Label('Victory',
                    font_name='Times New Roman',
                    font_size=60,
                    x=width/2 + self.scrollX, y=height/2,
                    color = (0, 0, 255, 255),
                    anchor_x='center', anchor_y='center')
            label.draw()

        if self.hero.flags['dead']:
            label = pyglet.text.Label('You Died',
                    font_name='Times New Roman',
                    font_size=60,
                    x=width/2 + self.scrollX, y=height/2,
                    color = (255, 0, 0, 255),
                    anchor_x='center', anchor_y='center')
            label.draw()

        # Draw the enemies
        for enemy in self.enemies:
            # remove enemies if dead
            # i will need to implement a dead timer so that they can do their dying animation before being removed
            if enemy.flags['dead'] and enemy.ableToBeAttacked(t):
                self.enemies.remove(enemy)
            else:
                enemy.draw(t)

        # Draw the hero.
        self.hero.draw(t, keyTracking)

        for x in config.kunai:
            if x.playerSprite.x < 0 or x.playerSprite.x > config.cols * config.width:
                config.kunai.remove(x)
            else:
                x.draw(t)

        # check for collision attacks:
        if len(enemies) > 0:
            for enemy in enemies:
                if not enemy.flags['dead']:
                    ehb = enemy.getHitbox()

                    # if kunai is in zombie hitbox then zombie take 1 damage and kunai is removed from array
                    if len(config.kunai) > 0:
                        for kunai in config.kunai:
                                khb = kunai.getHitbox()
                                if intersect(khb, ehb):
                                    enemy.takeDamage(1, t)
                                    config.kunai.remove(kunai)

                    # if player is attacking and zombie within front half of player, then zombie takes one damage
                    hhb = hero.getHitbox()
                    if hero.flags['attacking'] and intersect(hhb, ehb):
                        enemy.takeDamage(2, t)
                    # if zombie is touching player, then zombie triggers attack animation and player takes 1 damage
                    elif intersect(hhb, ehb):
                        enemy.attack(t)
                        hero.takeDamage(1, t)

        limitLeft = (1/4)*width
        leftQuarter = (1/4)*width + self.scrollX
        rightQuarter = (3/4)*width + self.scrollX
        playerLocation = self.hero.playerSprite.x
        if playerLocation < leftQuarter and leftQuarter > limitLeft:
            # Shift the world
            self.scrollX -= 5
            glTranslatef(5, 0, 0)
            # Shift the background image
            self.background_x = self.scrollX
        elif playerLocation > rightQuarter:
            # Shift the world
            self.scrollX += 5
            glTranslatef(-5, 0, 0)
            # Shift the background image
            self.background_x = self.scrollX

def intersect(kunaiHitbox, enemyHitbox):
    llx1 = kunaiHitbox[0][0]
    lly1 = kunaiHitbox[0][1]
    urx1 = kunaiHitbox[1][0]
    ury1 = kunaiHitbox[1][1]

    llx2 = enemyHitbox[0][0]
    lly2 = enemyHitbox[0][1]
    urx2 = enemyHitbox[1][0]
    ury2 = enemyHitbox[1][1]

    # this portion of code is from ChatGPT, I tried to figure this out on my own but after some drawings and one failed attempt I decided to get help. I was hoping for numpy to have some rectangle library though
    if urx1 < llx2 or urx2 < llx1:
        return False
    if ury1 < lly2 or ury2 < lly1:
        return False
    return True

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
