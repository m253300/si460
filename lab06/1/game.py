#!/usr/bin/python3 -B

# Important Libraries
import pyglet
import time, sys

# Our world that we will draw via pyglet
class Game:

    # Update the world time based on time elapsed in the real world
    # since we started the Game Class.
    def updateClock(self, dt):
        self.worldTime = time.time() - self.startTime
        # A temporary background mover as a demo...
        self.background_x -= 0.2

    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", resizable=False):

        # Count screenshots
        self.screenshot = 0

        # Build the OpenGL / Pyglet Window
        self.window = pyglet.window.Window(width=width, height=height, resizable=resizable, caption=caption)

        # Fix transparent issue...
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        # Lets set a global clock
        self.worldTime = 0.0
        self.startTime = time.time()

        # Create the Background, this is one method of creating images,
        # we will work with multiple methods.
        # Take a look at how this is drawn in the on_draw function
        # and the self.background.blit method.
        self.background = pyglet.resource.image("background.png")
        self.background_x = 0
        self.background_y = 0

        # Schedule a Clock to update the time
        pyglet.clock.schedule_interval(self.updateClock, 1.0/30.0)

        # Handle Key Presses in our World
        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.END:
                self.screenshot = self.screenshot + 1
                pyglet.image.get_buffer_manager().get_color_buffer().save(sys.argv[-1]+'.'+str(self.screenshot)+'.png')

        # Event Handler for drawing the screen
        @self.window.event
        def on_draw():

            # Example Text, lets build a bit of text and place on the screen.
            self.label1 = pyglet.text.Label('Welcome to Gaming in SI460!',
                              font_name='Times New Roman',
                              font_size=36,
                              x=width//2, y=height//3*2,
                              anchor_x='center', anchor_y='center')

            self.label2 = pyglet.text.Label('Press ESC to exit',
                              font_name='Times New Roman',
                              font_size=24,
                              x=width//2, y=height//3,
                              anchor_x='center', anchor_y='center')

            # Clear the window (a good way to start things)
            self.window.clear()

            # Draw the game background
            self.background.blit(self.background_x,self.background_y,height=height)

            # Lets draw all of the individual objects, these objects
            # need to have a draw function that takes in worldTime as
            # a variable.
            self.label1.draw()
            self.label2.draw()

# Load in any requested objects from the command then, then start the game.
if __name__ == '__main__':
    myGame = Game(800, 600, "SI460 Game")
    pyglet.app.run()
