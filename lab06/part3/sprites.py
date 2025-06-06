# SI460 pyglet sprite loading library

# pyglet and system libraries
import pyglet, os, re

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def atoi(text):
    return int(text) if text.isdigit() else text.lower()

# Function to load all images from all subdirs in sprite directory
# Returns a dictionary of the form:
#    {'hero': {'Run':{'Left':  [...array of images facing left...],
#                     'Right': [...array of images facing right...]}}}
def loadAllImages(filepath="mylevel/sprites"):
    pass

# Function to load images and categorize them into types (e.g. Run, Jump, Attack)
# I USED CHATGPT IN THIS TO COMPLETE THIS PART, MY INPUT AND THE OUTPUT ARE INCLUDED IN ANOTHER FILE
def loadImages(filepath="mylevel/sprites/hero"):
    files = os.listdir(filepath)
    files.sort()  # First sort alphabetically
    files.sort(key=natural_keys)  # Then sort using natural keys (numeric sorting)

    # Dictionary to store the organized sprite images
    sprite_dict = {}

    # Iterate through the files
    for file in files:
        # Extract the action type (e.g., 'Attack', 'Run', etc.) from the filename
        action = file.split(' ')[0]  # Everything before the space (e.g., 'Attack', 'Run')

        # Check if the action is already in the dictionary
        if action not in sprite_dict:
            sprite_dict[action] = {'Left': [], 'Right': []}

        # Create the full file path
        file_path = os.path.join(filepath, file)

        # Load image and flip for 'Left' and 'Right'
        image_left = pyglet.resource.image(file_path, flip_x=False)  # Right-facing image
        image_right = pyglet.resource.image(file_path, flip_x=True)  # Left-facing image

        # Add both images to the dictionary under the corresponding action type
        sprite_dict[action]['Right'].append(image_left)
        sprite_dict[action]['Left'].append(image_right)

    return sprite_dict

# Build and return a configured sprite
def buildSprite(sprites={}, character="hero", mode="Run", facing="Right",
                animationSpeed=0.05, animationScale=0.15, animationLoop=True,
                animationX=400, animationY=300):
    pass

# Run the following code if this script was run directly from the command line
if __name__ == '__main__':
    loadTest = loadImages()
    imagesTest = loadAllImages()
