import pyglet
import json
import os

def load_sprites_from_sheet(sprites_path):
    """
    Loads a sprite sheet and extracts individual sprites based on coordinates
    from a JSON file, creating both Right and Left facing versions.

    Args:
        sprites_path (str): Path to the sprite sheet png and json.

    Returns:
        dict: A dictionary where keys are sprite names and values are
              pyglet.image.TextureRegion objects.  The dictionary is
              nested like this:
              {'character_name': {'animation_name': {'Right': [list of TextureRegions], 'Left': [list of TextureRegions]}}}
    """

    sheet_image_path = f"{sprites_path}/spritesheet.png"
    sheet_json_path = f"{sprites_path}/spritesheet.json"

    sprite_sheet = pyglet.image.load(sheet_image_path)

    with open(sheet_json_path, 'r') as f:
        sprite_data = json.load(f)

    sprites = {}
    for sprite_name, data in sprite_data['frames'].items():
        # Extract character and animation name
        parts = sprite_name.split("-")
        if len(parts) > 1:
            character_name = parts[0]
            animation_name = parts[1].split(" ")[0]  # animation name
        else:
            character_name = "other"  # Or some default
            animation_name = parts[0].split(" ")[0]  # animation name

        # Extract frame data
        x = data['frame']['x']
        y = data['frame']['y']
        width = data['frame']['w']
        height = data['frame']['h']

        # Create TextureRegion for Right facing
        right_region = sprite_sheet.get_region(x, sprite_sheet.height - y - height, width, height)

        # Create a flipped TextureRegion for Left facing
        left_region = right_region.get_texture().get_transform(flip_x = True)

        # Store the TextureRegions
        if character_name not in sprites:
            sprites[character_name] = {}
        if animation_name not in sprites[character_name]:
            sprites[character_name][animation_name] = {"Right": [], "Left": []}  # Initialize both directions

        sprites[character_name][animation_name]["Right"].append(right_region)
        sprites[character_name][animation_name]["Left"].append(left_region)  # Store the flipped version

    return sprites


def buildSprite(sprites={}, character="Hero", mode="Run", facing="Right",
                animationSpeed=0.05, animationScale=0.15, animationLoop=True,
                animationX=400, animationY=300):
    """
    Build and return a configured sprite.  This version now takes a dictionary
    of TextureRegions with 'Right' and 'Left' facing.
    """

    # Grab the correct sequence of images
    if character in sprites and mode in sprites[character] and facing in sprites[character][mode]:
        playerSequence = sprites[character][mode][facing]
    else:
        print(f"Error: Could not find animation sequence for character='{character}', mode='{mode}', facing='{facing}'")
        return None  # Or raise an exception

    # Build the pyglet animation sequence
    playerAnimation = pyglet.image.Animation.from_image_sequence(playerSequence,
                                                                 animationSpeed,
                                                                 animationLoop)
    # Create the sprite from the animation sequence
    playerSprite = pyglet.sprite.Sprite(playerAnimation,
                                        x=animationX,
                                        y=animationY)
    # Set the player's scale
    playerSprite.scale = animationScale

    return playerSprite


if __name__ == '__main__':
    # Example Usage
    sheet_path = 'mylevel/sprites'  # Path to your spritesheet.png
    my_sprites = load_sprites_from_sheet(sheet_path)

    # Example: Create a sprite using the loaded data
    player = buildSprite(my_sprites, character="enemy1", mode="Dead", facing="Left", animationSpeed=0.1, animationX=100, animationY=100)

    if player:
        window = pyglet.window.Window(800, 600)

        @window.event
        def on_draw():
            window.clear()
            player.draw()

        pyglet.app.run()