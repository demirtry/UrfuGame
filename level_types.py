import pygame
from objects import Scene


class Level:
    def __init__(self, scene: Scene):
        self.scene = scene
        self.clock = pygame.time.Clock()
        self.collisions = []
        self._level_running = True

    def make_collisions(self):
        self.collisions = []
        for obj in self.scene.get_obj_lst():
            self.collisions.append(obj.get_current_animation().get_rect())

    def get_level_running(self):
        return self._level_running

    def switch_level_running(self):
        self._level_running = not self._level_running

    def update_scene(self, scene: Scene):
        self.scene = scene


class LevelWithButtons(Level):
    def __init__(self, scene: Scene):
        super().__init__(scene)
        self.last_element_index_before_pause = len(self.scene.get_obj_lst()) - 1
        self.buttons = []
        self.current_button_index = None
        self.buttons_callbacks = []

    def switch_button(self, key):
        if key == pygame.K_w:
            self.button_up()
        else:
            self.button_down()

    def button_up(self):
        if self.current_button_index is None:
            self.current_button_index = 0
        else:
            self.current_button_index = max(0, self.current_button_index - 1)
        for button in self.buttons:
            button.to_base_condition()
        self.buttons[self.current_button_index].select()

    def button_down(self):
        if self.current_button_index is None:
            self.current_button_index = len(self.buttons) - 1
        else:
            self.current_button_index = min(len(self.buttons) - 1, self.current_button_index + 1)
        self.to_start()
        self.buttons[self.current_button_index].select()

    def to_start(self):
        for button in self.buttons:
            button.to_base_condition()