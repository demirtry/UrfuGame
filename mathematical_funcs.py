import pygame
import matplotlib.pyplot as plt
import numpy as np
import time
from math import atan, degrees
import random


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        return result

    return wrapper


def array_concatenation(img, start_img=None):
    height = 24
    new_img = []
    for i in range(height):
        if start_img is None:
            new_img_i = np.concatenate((img[i], img[i]), axis=0)
        else:
            new_img_i = np.concatenate((img[i], start_img[i]), axis=0)
        new_img.append(new_img_i)
    new_img = np.array(new_img)
    return new_img


def img_multiplication(input_path: str, output_path: str, count: int):
    start_img = plt.imread(input_path)
    img = start_img
    if count != 1:
        for i in range(int(np.sqrt(count))):
            img = array_concatenation(img)
        new_cnt = np.power(2, int(np.sqrt(count)))
        for i in range(count - new_cnt):
            img = array_concatenation(img, start_img)
        img = np.array(img)
    plt.imsave(output_path, img)


def img_rotation(input_path: str, degree: float):
    base_fireball_ing = pygame.image.load(input_path).convert_alpha()
    rotated_img = pygame.transform.rotate(base_fireball_ing, degree).convert_alpha()

    return rotated_img


def degree_calculation(start_coordinates, mouse_position):
    start_end_dx = mouse_position[0] - start_coordinates[0]
    start_end_dy = mouse_position[1] - start_coordinates[1]

    if start_end_dx:
        alpha = atan(abs(start_end_dy) / abs(start_end_dx))
    else:
        alpha = 0

    alpha = int(degrees(alpha))

    if start_end_dx >= 0 >= start_end_dy:
        pass
    elif start_end_dx <= 0 and start_end_dy <= 0:
        alpha = 180 - alpha
    elif start_end_dx <= 0 <= start_end_dy:
        alpha += 180
    else:
        alpha = 360 - alpha

    return alpha


def trajectory_calculate(start_coordinates, mouse_position, speed) -> tuple[int | float, int | float]:
    start_end_dx = mouse_position[0] - start_coordinates[0]
    start_end_dy = mouse_position[1] - start_coordinates[1]
    trajectory_length = (start_end_dx ** 2 + start_end_dy ** 2) ** (1 / 2)
    start_end_count_steps = trajectory_length / speed

    step_dx = round(start_end_dx / start_end_count_steps, 2)
    step_dy = round(start_end_dy / start_end_count_steps, 2)

    return step_dx, step_dy


def generate_enemy_position(tiles, player):

    upper_row = tiles[0, :]
    left_column = tiles[:, 0]
    right_column = tiles[:, 31]

    enemy_possible_tiles = [
        upper_row.copy(), left_column.copy(), right_column.copy()
    ]

    player_tile = player.get_current_tile()

    current_location_index = random.randint(0, 2)
    current_location = enemy_possible_tiles[current_location_index]

    if current_location_index == 1 and player_tile[1] - 5 < 0 or current_location_index == 2 and player_tile[1] + 5 > 31:
        min_banned_index = max(0, player_tile[0]-5)
        max_banned_index = min(len(current_location)-1, player_tile[0]+6)
        current_location[min_banned_index:max_banned_index] = 1

    elif current_location_index == 0 and player_tile[0] - 5 < 0:
        min_banned_index = max(0, player_tile[1]-5)
        max_banned_index = min(len(current_location)-1, player_tile[1]+6)
        current_location[min_banned_index:max_banned_index] = 1

    enemy_turn = False

    if current_location_index:
        while True:
            selected_tile_row_index = random.randint(0, len(current_location) - 1)
            if not current_location[selected_tile_row_index]:
                break

        if current_location_index == 2:
            selected_tile_column_index = 31
        else:
            enemy_turn = True
            selected_tile_column_index = 0

    else:
        while True:
            selected_tile_column_index = random.randint(0, len(current_location) - 1)
            if not current_location[selected_tile_column_index]:
                if selected_tile_column_index < 15:
                    enemy_turn = True
                break

        selected_tile_row_index = 0

    enemy_x = selected_tile_column_index * 32 - 19
    enemy_y = selected_tile_row_index * 24 - 24

    return enemy_x, enemy_y, enemy_turn
