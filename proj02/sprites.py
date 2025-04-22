import pyglet
import os
import pickle
import ast  # For safer literal evaluation

# Cache file name
CACHE_FILE = "sprite_cache.pkl"


def loadAllImages(filepath="mylevel/sprites"):
    """
    Loads all images from all subdirectories in the sprite directory,
    using a cache to speed up subsequent loads. This version caches
    strings of pyglet.resource.image() calls.
    """
    if os.path.exists(CACHE_FILE):
        print(f"Loading sprite data from cache: {CACHE_FILE}")
        with open(CACHE_FILE, "rb") as f:
            cached_data = pickle.load(f)

        # Evaluate the strings to create images
        results = {}
        for character, modes in cached_data.items():
            results[character] = {}
            for mode, directions in modes.items():
                results[character][mode] = {}
                for direction, image_strings in directions.items():
                    images = []
                    for img_str in image_strings:
                        try:
                            img = eval(img_str)
                            img.anchor_x = img.width / 2.0
                            images.append(img)
                        except Exception as e:
                            print(f"Error evaluating '{img_str}': {e}")
                    results[character][mode][direction] = images
        print("Images loaded from cache.")
        return results

    print("Loading sprite data from disk and creating cache...")
    dirs = os.listdir(filepath)
    results = {}
    cache_data = {}  # Dictionary to store strings for caching
    for d in dirs:
        char_images, char_cache_data = loadImages(filepath + '/' + d)
        results[d] = char_images
        cache_data[d] = char_cache_data

    # Save the strings to the cache file
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache_data, f)
    print(f"Saved sprite data to cache: {CACHE_FILE}")
    return results


def loadImages(filepath="mylevel/sprites/hero"):
    files = os.listdir(filepath)
    files.sort()
    results = {}
    cache_data = {}  # Dictionary to store strings for caching

    # Lets fix the numbering problem (1, 10, 2, 3, etc.)
    for f in files:
        if f.find('.png') != -1 and f.find('(') != -1:
            mode = f.split('(')[0].strip()
            seqnum = f.split(')')[0].split('(')[1].strip().zfill(2)
            if not mode in results:
                results[mode] = {'Right': {}, 'Left': {}}
                cache_data[mode] = {'Right': [], 'Left': []}  # Initialize lists

            right_img_str = f"pyglet.resource.image('{filepath}/{f}', flip_x=False)"
            left_img_str = f"pyglet.resource.image('{filepath}/{f}', flip_x=True)"

            results[mode]['Right'][seqnum] = right_img_str
            results[mode]['Left'][seqnum] = left_img_str

            cache_data[mode]['Right'].append(right_img_str)
            cache_data[mode]['Left'].append(left_img_str)

        elif f.find('.png') != -1:
            mode = f.split('.png')[0].strip()
            seqnum = "00"
            if not mode in results:
                results[mode] = {'Right': {}, 'Left': {}}
                cache_data[mode] = {'Right': [], 'Left': []}  # Initialize lists

            right_img_str = f"pyglet.resource.image('{filepath}/{f}', flip_x=False)"
            left_img_str = f"pyglet.resource.image('{filepath}/{f}', flip_x=True)"

            results[mode]['Right'][seqnum] = right_img_str
            results[mode]['Left'][seqnum] = left_img_str

            cache_data[mode]['Right'].append(right_img_str)
            cache_data[mode]['Left'].append(left_img_str)

    # Now lets start the process to load the actual images, now that
    # the order will be correct.
    final_results = {}
    for mode in results:
        right = []
        left = []
        for seqnum, img_str in sorted(results[mode]['Right'].items()):
            try:
                r = eval(img_str)
                r.anchor_x = r.width / 2.0
                right.append(r)
            except Exception as e:
                print(f"Error evaluating '{img_str}': {e}")

            try:
                l = eval(results[mode]['Left'][seqnum])
                l.anchor_x = l.width / 2.0
                left.append(l)
            except Exception as e:
                print(f"Error evaluating '{results[mode]['Left'][seqnum]}': {e}")
        final_results[mode] = {'Right': right, 'Left': left}

    # return our results
    return final_results, cache_data


def buildSprite(sprites={}, character="hero", mode="Run", facing="Right",
                animationSpeed=0.05, animationScale=0.15, animationLoop=True,
                animationX=400, animationY=300):
    # ... (rest of your buildSprite function remains the same)

    # Grab the correct sequence of images
    playerSequence = sprites[character][mode][facing]

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
    loadTest = loadImages()
    imagesTest = loadAllImages()