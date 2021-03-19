from ursina import *

from opensimplex import OpenSimplex
from ursina.mesh_importer import compress_models

from player import Player
from voxel import *

# Default settings / variables for the application (Initialization)
gravity = 9.8

simplexNoise = OpenSimplex()

# Create application class
app = Ursina()

<<<<<<< HEAD
application.asset_folder = application.asset_folder / 'assets'

# Import textures
grass_tex = load_texture('assets/textures/grass_block.png')

=======
>>>>>>> parent of 8155f5f (Added voxel model and texture)
# Set settings for the window
window.title = "Minecraft: Python Edition"
# window.show_ursina_splash = True
window.borderless = False
window.exit_button.enabled = False
window.fps_counter.enabled = True
window.center_on_screen()

# Create the player
player = Player(gravity = gravity)

# Create the terrain using simplex noise
for i in range(-12, 12):
    for j in range(-12, 12):
        flatNoise = simplexNoise.noise2d(j, i) / 10
        hillyNoise = simplexNoise.noise2d(j, i) * 5

        worldNoise = flatNoise * hillyNoise

        voxels.append(Voxel(position = Vec3(j, 0, i)))
    
def update():
    # Close game window
    if (held_keys['escape']):
        application.quit()

# Run app
app.run()