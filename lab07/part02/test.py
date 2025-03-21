import pyglet

backgroundMusic = pyglet.media.Player()
backgroundMusic.queue(pyglet.media.load('/home/m253300/si460/lab07/part02/mylevel/music/1.wav', streaming=True))
backgroundMusic.eos_action = 'loop'
backgroundMusic.loop = True
backgroundMusic.play()

# Keep the application running for the duration of the sound (or longer)
# You can calculate the duration using sound.duration
pyglet.app.run()