from ursina import application
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os

app = Ursina()

# Variables
grass_texture = load_texture("Assets/Textures/Grass_Block.png")
stone_texture = load_texture("Assets/Textures/Stone_Block.png")
brick_texture = load_texture("Assets/Textures/Brick_Block.png")
dirt_texture = load_texture("Assets/Textures/Dirt_Block.png")
wood_texture = load_texture("Assets/Textures/Wood_Block.png")
sky_texture = load_texture("Assets/Textures/Skybox.png")
arm_texture = load_texture("Assets/Textures/Arm_Texture.png")
punch_sound = Audio("Assets/SFX/Punch_Sound.wav", loop = False, autoplay = False)
window.exit_button.visible = True
block_pick = 1

textures = [None, grass_texture, stone_texture, brick_texture, dirt_texture, wood_texture]
voxel_dict = {}
voxel_tupes= {}
SAVE_FILENAME = 'map_save.json'

def pos_to_key(pos):
    return (int(pos[0]), int(pos[1]), int(pos[2]))

def create_voxel(positsion, texture_id=1):
    texture = textures[texture_id]
    v = Voxel(position=positsion, texture=texture)
    key = pos_to_key(positsion)
    voxel_dict[key] = v
    voxel_tupes[key] = texture_id
    return v

def save_map(filename = SAVE_FILENAME):
    data = []
    for pos, tex_id in voxel_tupes.items():
        x, y, z = pos
        data.append([x, y, z, tex_id])
    with open (filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_map(filename = SAVE_FILENAME):
    if not os.path.exists(filename):
        return
    for v in list(voxel_dict.values()):
        destroy(v)
    voxel_dict.clear()
    voxel_tupes.clear()
    with open(filename, "r", encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        x, y, z, tex_id = item
        create_voxel((x,y,z), texture_id=tex_id)


# Updates every frame
def update():
    global block_pick

    if held_keys["left mouse"] or held_keys["right mouse"]:
        hand.active()
    else:
        hand.passive()

    if held_keys["1"]: block_pick = 1
    if held_keys["2"]: block_pick = 2
    if held_keys["3"]: block_pick = 3
    if held_keys["4"]: block_pick = 4
    if held_keys["5"]: block_pick = 5
def input(key):
    if key == 'k':
        save_map()
    if key == 'l':
        load_map()
    if key == 'escape':
        save_map()
        application.quit()


# Voxel (block) properties
class Voxel(Button):
    def __init__(self, position = (0, 0, 0), texture = grass_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = "Assets/Models/Block",
            origin_y = 0.5,
            texture = texture,
            color = color.color(0, 0, random.uniform(0.9, 1)),
            highlight_color = color.light_gray,
            scale = 0.5
        )
    
    # What happens to blocks on inputs
    def input(self,key):
        if self.hovered:
            if key == "left mouse down":
                punch_sound.play()
                target_pos = self.position + mouse.normal
                create_voxel(target_pos, texture_id= block_pick)
                                 
            if key == "right mouse down":
                punch_sound.play()
                keypos = pos_to_key(self.position)
                if keypos in voxel_dict:
                    del voxel_dict[keypos]
                if keypos in voxel_tupes:
                    del voxel_tupes[keypos]
                destroy(self)

# Skybox
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "Sphere",
            texture = sky_texture,
            scale = 150,
            double_sided = True
        )

# Arm
class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = "Assets/Models/Arm",
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150, -10, 0),
            position = Vec2(0.4, -0.6)
        )
    
    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

# Increase the numbers for more cubes. For exapmle: for z in range(20)
if os.path.exists(SAVE_FILENAME):
    load_map()
else:
    for z in range(20):
        for x in range(20):
            create_voxel((x, 0,z), texture_id=1)


player = FirstPersonController()
sky = Sky()
hand = Hand()


app.run()