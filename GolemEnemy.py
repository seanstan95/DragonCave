import math
import pathlib
from typing import List

import arcade
from arcade.draw_commands import Texture

from Enemy import Enemy


class GolemEnemy(Enemy):
    """Boss enemy that appears in cave 2. Has 3 health and can only be damaged if the player has magic fire arrows."""
    def __init__(self, scale: float, center_x: float, center_y: float, health: int, init_range: int):
        super().__init__(scale, center_x, center_y, health, init_range)

        self.character_x_loc = 0
        self.character_y_loc = 0
        self.attacking_textures = []
        self.cur_texture_index = 0

    def update_animation(self, delta_time=1/30):
        """
        Logic for selecting the proper texture to use.
        """
        texture_list: List[Texture] = []

        x1 = self.center_x
        x2 = self.last_texture_change_center_x
        y1 = self.center_y
        y2 = self.last_texture_change_center_y
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        change_direction = True
        if self.change_x < 0 < len(self.walk_left_textures) and self.state != self.FACE_LEFT:
            self.state = self.FACE_LEFT
        elif self.change_x > 0 < len(self.walk_right_textures) and self.state != self.FACE_RIGHT:
            self.state = self.FACE_RIGHT
        elif self.change_y < 0 < len(self.walk_down_textures) and self.state != self.FACE_DOWN:
            self.state = self.FACE_DOWN
        elif self.change_y > 0 < len(self.walk_up_textures) and self.state != self.FACE_UP:
            self.state = self.FACE_UP
        else:
            change_direction = False

        # if not moving, load first texture from walk textures (in place of standing textures)
        if self.change_x == 0 and self.change_y == 0:
            if self.state == self.FACE_LEFT:
                self.texture = self.walk_left_textures[0]
            elif self.state == self.FACE_RIGHT:
                self.texture = self.walk_right_textures[0]
            elif self.state == self.FACE_UP:
                self.texture = self.walk_up_textures[0]
            elif self.state == self.FACE_DOWN:
                self.texture = self.walk_down_textures[0]

        elif change_direction or distance >= self.texture_change_distance:
            self.last_texture_change_center_x = self.center_x
            self.last_texture_change_center_y = self.center_y

            if self.state == self.FACE_LEFT:
                texture_list = self.walk_left_textures
            elif self.state == self.FACE_RIGHT:
                texture_list = self.walk_right_textures
            elif self.state == self.FACE_UP:
                texture_list = self.walk_up_textures
            elif self.state == self.FACE_DOWN:
                texture_list = self.walk_down_textures

            if len(texture_list) == 0:
                raise RuntimeError("error loading walk animations in goblin update_animation")

            # check if done playing the texture
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0

            self.texture = texture_list[self.cur_texture_index]
            
            
def setup_golem(scl, change_x, change_y, cent_x, cent_y, health, init_range):
    golem = GolemEnemy(scale=scl, center_x=cent_x, center_y=cent_y, health=health, init_range=init_range)

    # get sprite sheet path
    walking_sprite_sheet = pathlib.Path.cwd() / 'Assets' / 'Enemies' / 'Golem' / 'golem-walk.png'

    golem_frame_width = 64
    golem_frame_height = 64

    for image_num in range(1, 7, 1):
        frame = arcade.load_texture(str(walking_sprite_sheet), image_num * golem_frame_width,
                                    golem_frame_height * 0, height=golem_frame_height,
                                    width=golem_frame_width)
        frame.width = frame.width * scl
        frame.height = frame.height * scl
        golem.walk_up_textures.append(frame)

        frame = arcade.load_texture(str(walking_sprite_sheet), image_num * golem_frame_width,
                                    golem_frame_height * 1, height=golem_frame_height,
                                    width=golem_frame_width)
        frame.width = frame.width * scl
        frame.height = frame.height * scl
        golem.walk_left_textures.append(frame)

        frame = arcade.load_texture(str(walking_sprite_sheet), image_num * golem_frame_width,
                                    golem_frame_height * 2, height=golem_frame_height,
                                    width=golem_frame_width)
        frame.width = frame.width * scl
        frame.height = frame.height * scl
        golem.walk_down_textures.append(frame)

        frame = arcade.load_texture(str(walking_sprite_sheet), image_num * golem_frame_width,
                                    golem_frame_height * 3, height=golem_frame_height,
                                    width=golem_frame_width)
        frame.width = frame.width * scl
        frame.height = frame.height * scl
        golem.walk_right_textures.append(frame)

    golem.change_x = change_x
    golem.change_y = change_y
    return golem
