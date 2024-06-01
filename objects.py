import pygame
from mathematical_funcs import trajectory_calculate


class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinates(self) -> tuple[int, ...]:
        result = tuple([self.x, self.y])
        return result


class VisibleObject(Object):
    def __init__(self, x, y, max_animation_cnt, lst_of_animation_lst):
        super().__init__(x, y)
        self.max_animation_cnt = max_animation_cnt
        self.lst_of_animation_lst = lst_of_animation_lst
        self.current_animation_lst_ind = 0
        self.current_animation_ind = 0

    def get_current_animation(self):
        return self.lst_of_animation_lst[self.current_animation_lst_ind][self.current_animation_ind]

    def change_animation_ind(self):
        if self.current_animation_ind == self.max_animation_cnt - 1:
            self.current_animation_ind = 0
        else:
            self.current_animation_ind += 1

    def change_animation_lst_ind(self):
        if self.current_animation_lst_ind == len(self.lst_of_animation_lst):
            self.current_animation_lst_ind = 0
        else:
            self.current_animation_ind += 1


class Player(VisibleObject):
    def __init__(self, x: int, y: int, max_animation_cnt: int, lst_of_animation_lst, jump_size: int = 9, speed: int = 8, cnt_steps_to_run: int = 20):
        super().__init__(x, y, max_animation_cnt, lst_of_animation_lst)
        self.animation_cnt = 0
        self.max_animation_cnt = max_animation_cnt
        self.turn = False
        self.jump = False
        self.fall = False
        self.gravity = 10
        self.jump_size = jump_size
        self.jump_count = jump_size
        self.speed = speed
        self.cnt_steps_to_run = cnt_steps_to_run
        self.current_cnt_steps = cnt_steps_to_run

    def move_right(self, collide_status):
        last_turn = self.turn
        self.turn = True
        if last_turn != self.turn:
            self.current_cnt_steps = self.cnt_steps_to_run
            self.current_animation_ind = 0

        if not self.current_cnt_steps:
            self.current_animation_lst_ind = 5
        else:
            self.current_animation_lst_ind = 3

        if self.x < 1024 - 9 - 32 - self.speed and not collide_status:

            if self.current_animation_lst_ind == 3:
                self.x += self.speed
                self.current_cnt_steps -= 1
            else:
                self.x += self.speed + 4
        else:

            self.current_cnt_steps = self.cnt_steps_to_run

    def move_left(self, collide_status):
        last_turn = self.turn
        self.turn = False
        if last_turn != self.turn:
            self.current_cnt_steps = self.cnt_steps_to_run
            self.current_animation_ind = 0

        if not self.current_cnt_steps:
            self.current_animation_lst_ind = 4
        else:
            self.current_animation_lst_ind = 2

        if self.x > self.speed - 9 and not collide_status:

            if self.current_animation_lst_ind == 2:
                self.x -= self.speed
                self.current_cnt_steps -= 1
            else:
                self.x -= self.speed + 4
        else:

            self.current_cnt_steps = self.cnt_steps_to_run

    # def move_right(self, collide_status):
    #     last_turn = self.turn
    #     self.turn = True
    #     # self.current_animation_lst_ind = 3
    #     if last_turn != self.turn:
    #         self.current_animation_ind = 0
    #     if self.x < 1024 - 9 - 32 - self.speed and not collide_status:
    #         self.x += self.speed

    # def move_left(self, collide_status):
    #     last_turn = self.turn
    #     self.turn = False
    #     self.current_animation_lst_ind = 4
    #     # self.current_animation_lst_ind = 2
    #     if last_turn != self.turn:
    #         self.current_animation_ind = 0
    #     if self.x > self.speed - 9 and not collide_status:
    #         self.x -= self.speed

    def make_jump(self, collide_up):
        if not collide_up and self.jump_count > 0:
            self.jump = True
            self.y -= (self.jump_count ** 2) // 2
            self.jump_count -= 1
        else:
            self.jump = False
            self.fall = True
            self.jump_count = self.jump_size

    def make_fall(self, collide_down):
        if not collide_down:
            self.fall = True
            self.y += self.gravity
        else:
            self.fall = False

    def become_idle(self):
        last_current_animation_lst_ind = self.current_animation_lst_ind
        self.current_cnt_steps = self.cnt_steps_to_run
        if self.turn:
            self.current_animation_lst_ind = 1
        else:
            self.current_animation_lst_ind = 0
        if last_current_animation_lst_ind != self.current_animation_lst_ind:
            self.current_animation_ind = 0

    def get_rect(self):
        player_coordinates = self.get_coordinates()
        rect_coordinates = (player_coordinates[0] + 9, player_coordinates[1] - 2)
        return pygame.Rect(rect_coordinates, (32, 72))

    def get_current_tile(self) -> tuple[int, int]:
        player_coordinates = self.get_coordinates()
        rect_coordinates = (player_coordinates[0] + 9, player_coordinates[1] - 2)

        player_tile_row_index = rect_coordinates[1] // 24 + 1
        player_tile_column_index = rect_coordinates[0] // 32

        player_tile = (player_tile_row_index, player_tile_column_index)
        return player_tile


class Enemy(VisibleObject):
    def __init__(self, x, y, max_animation_cnt: int, lst_of_animation_lst: list[...], x_speed: int = 4, y_speed: int = 3):
        super().__init__(x, y, max_animation_cnt, lst_of_animation_lst)
        self.animation_cnt = 0
        self.max_animation_cnt = max_animation_cnt
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.current_bfs_index = 0
        self.current_action = None

    def get_rect(self):
        enemy_coordinates = self.get_coordinates()
        rect_coordinates = (enemy_coordinates[0] + 19, enemy_coordinates[1] + 24)
        return pygame.Rect(rect_coordinates, (32, 24))

    def get_current_tile(self) -> tuple[int, int]:
        enemy_coordinates = self.get_coordinates()
        rect_coordinates = (enemy_coordinates[0] + 19, enemy_coordinates[1] + 24)

        enemy_tile_row_index = rect_coordinates[1] // 24
        enemy_tile_column_index = rect_coordinates[0] // 32

        enemy_tile = (enemy_tile_row_index, enemy_tile_column_index)
        return enemy_tile

    def move(self, way):

        if way is not None:
            split_way = way.split()
            for way in split_way:
                if way == 'left':
                    self.current_animation_lst_ind = 0
                    self.x -= self.x_speed
                elif way == 'right':
                    self.current_animation_lst_ind = 1
                    self.x += self.x_speed
                elif way == 'up':
                    self.y -= self.y_speed
                elif way == 'down':
                    self.y += self.y_speed


class Button(VisibleObject):
    def __init__(self, x, y, font_name, text, text_size, base_color, current_color):
        base_btn_img = TextBoxCreator.create_text_img(font_name, text, text_size, base_color)
        current_btn_img = TextBoxCreator.create_text_img(font_name, text, text_size, current_color)
        super().__init__(x, y, 1, [[base_btn_img], [current_btn_img]])
        self.current = False

    def select(self):
        self.current = True
        self.current_animation_lst_ind = 1

    def to_base_condition(self):
        self.current = False
        self.current_animation_lst_ind = 0


class Platform(VisibleObject):
    def __init__(self, x, y, max_animation_cnt, lst_of_animation_lst):
        super().__init__(x, y, max_animation_cnt, lst_of_animation_lst)
        self.rect = self.get_current_animation().get_rect(topleft=self.get_coordinates())

    def get_rect(self):
        return self.rect


class FireBall(VisibleObject):
    def __init__(self, x, y, max_animation_cnt, lst_of_animation_lst, mouse_position, speed: int = 10):
        super().__init__(x, y, max_animation_cnt, lst_of_animation_lst)
        self.speed = speed
        self.trajectory = trajectory_calculate(self.get_coordinates(), mouse_position, self.speed)

    def move(self):
        self.x += self.trajectory[0]
        self.y += self.trajectory[1]

    def check_position(self):
        position_status = True
        if self.x < 0 or self.x > 1024 or self.y < 0 or self.y > 768:
            position_status = False
        return position_status


class TextBoxCreator:
    @staticmethod
    def create_text_img(font_name, text, text_size, color):
        font = pygame.font.SysFont(font_name, text_size)
        text_img = font.render(text, True, color)
        return text_img
