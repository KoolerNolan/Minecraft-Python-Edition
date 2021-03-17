from opensimplex import OpenSimplex
from ursina import *
import keyboard

gravity = 9.8

voxels = []

simplexNoise = OpenSimplex()

class Player(Entity):
    def __init__(self, position = (0, 3, 0)):
        super().__init__(
            parent = scene,
            model = 'cube',
            position = position,
            rotation = (0, 0, 0),
            color = color.orange,
            visible_self = False,
            scale_y = 1,
            collider = 'box',
            collision = True,
            origin_y = 0
        )

        self.cursor = Entity(
            parent = camera.ui,
            model = 'circle',
            color = color.white,
            scale = .008
        )

        # Default variables (Initalization)
        self.player_height = 1.25

        self.move_speed = 2.75
        self.mouse_siv = 33

        self.fall_speed = 0
        self.fall_acc = .23

        self.jump_height = .21
        self.jump_speed = 0
        self.jump_acc = .865

        self.grounded = False
        self.jumping = False

        self.forward_col_ray = None
        self.sides_col_ray = None

        # Camera settings
        camera.fov = 80
        camera.orthographic = False

        # Position the camera where the players head should be
        camera.position = Vec3(self.position.x, self.position.y + self.player_height, self.position.z)
        camera.rotation = self.rotation

        mouse.locked = True
        mouse.visible = False

    def update(self):
        global gravity

        # Rotate camera to where "the player is looking"
        camera.rotation_y += mouse.velocity[0] * self.mouse_siv
        camera.rotation_x -= mouse.velocity[1] * self.mouse_siv
        camera.rotation_x = clamp(camera.rotation_x, -90, 90)
        self.rotation_y = camera.rotation_y

        # Get the direction we're trying to walk in.
        v_move = held_keys['w'] - held_keys['s']
        h_move = held_keys['d'] - held_keys['a']

        # Get direction vectors
        forward_dir = self.forward * v_move
        sides_dir = self.right * h_move

        col_ray_origin = self.world_position
        col_ray_dist = .25

        # Forward ray: check if something blocks the way when walking forward or backward
        self.forward_col_ray = boxcast(col_ray_origin, forward_dir, distance = col_ray_dist, thickness = (1, 1), ignore = (self,))
        if (self.forward_col_ray.hit):
            forward_dir = self.forward * 0

        # Sides ray: check if something blocks the way when walking sideways
        self.sides_col_ray = boxcast(col_ray_origin, sides_dir, distance = col_ray_dist, thickness = (1, 1), ignore = (self,))
        if (self.sides_col_ray.hit):
            sides_dir = self.right * 0

        direction = Vec3(forward_dir + sides_dir).normalized()

        self.position += direction * self.move_speed * time.dt

        # Position the camera where the players head should be
        camera.position = Vec3(self.position.x, self.position.y + self.player_height, self.position.z)

        # Gravity: check if any floor exists and if not, the player falls
        bottom_cast = boxcast(Vec3(self.position.x, self.position.y - (self.scale_y / 2), self.position.z), self.down, distance = .1, thickness = (1, 1), ignore = (self,))
        if not bottom_cast.hit:
            self.grounded = False
        else:
            self.fall_speed = 0
            self.jump_speed = 0
            self.reduce_jump_vel = 0
            self.grounded = True

        # Apply gravity if we're not jumping and not grounded
        if not self.grounded and not self.jumping:
            self.fall_speed += self.fall_acc * time.dt
            self.fall_speed = clamp(self.fall_speed, 0, gravity)
            self.position = Vec3(self.position.x, self.position.y - self.fall_speed, self.position.z)

        # If 'Space' is pressed, set self.jumping to true
        if (held_keys['space'] and self.grounded):
            self.jumping = True

        if (self.jumping):
            self.jump_speed += self.jump_acc * time.dt
            self.jump_speed = clamp(self.jump_speed, 0, self.jump_height)

            self.position = Vec3(self.position.x, self.position.y + self.jump_speed, self.position.z)

            if (self.jump_speed >= self.jump_height):
                self.jumping = False

    

class Voxel(Entity):
    def __init__(self, position = (0, 0, 0), durab = 2):
        super().__init__(
            parent = scene,
            model = 'cube',
            position = position,
            texture = 'white_cube',
            color = color.white,
            collider = 'box',
            collision = True,
            origin_y = 0
        )

        self.durab = durab

    def input(self, key):
        # Check if cursor is hovering over voxel and if it's in range
        if (self.hovered and distance(self.position, camera.position) <= 13):
            if (key == 'left mouse down'):
                self.remove_durab()
            elif (key == 'right mouse down'):
                voxels.append(Voxel(position = self.position + mouse.normal))

    def remove_durab(self):
        self.durab -= 1
        if (self.durab <= 0):
            destroy(self)

app = Ursina()

window.title = "Minecraft: Python Edition"
window.borderless = False
window.exit_button.enabled = False
window.fps_counter.enabled = True
window.center_on_screen()

player = Player()

for i in range(-12, 12):
    for j in range(-12, 12):
        flatNoise = simplexNoise.noise2d(j, i) / 10
        hillyNoise = simplexNoise.noise2d(j, i) * 5

        worldNoise = flatNoise * hillyNoise

        voxels.append(Voxel(position = Vec3(j, worldNoise, i)))
    
def update():
    # Close game window
    if (held_keys['escape']):
        application.quit()

app.run()