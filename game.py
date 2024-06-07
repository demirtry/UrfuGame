import pygame
from level_types import Level
from game_logic import GameplayLevel, Menu, Pause, GameOver
from game_helper import Helper
from objects import Scene, ScoreCounter


class LevelCreator:
    @staticmethod
    def create_lvl1():
        scene, player, score_counter, platforms = Helper.create_level1_objects()
        return GameplayLevel(scene, player, score_counter, platforms)

    @staticmethod
    def create_menu_lvl():
        menu_scene, menu_buttons = Helper.create_menu_scene()
        return Menu(menu_scene, menu_buttons)

    @staticmethod
    def create_pause_lvl(scene: Scene):
        return Pause(scene)

    @staticmethod
    def create_game_over_lvl(score_counter: ScoreCounter, record_status):
        game_over_scene, game_over_buttons = Helper.create_game_over_objects(score_counter, record_status)
        return GameOver(game_over_scene, game_over_buttons)


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.current_level = LevelCreator.create_menu_lvl()
        self.screen = pygame.display.set_mode((1024, 768))
        self.paused_level = None
        self.score_record = 0
        self.saved_levels = {}
        self.commands_dict = {
            'to_play': self.to_play,
            'to_play_from_pause': self.to_play_from_pause,
            'to_menu': self.to_menu,
            'to_pause': self.to_pause,
            'get_load_level_name': self.get_load_level_name,
            'save_level': self.save_level,
            'game_over': self.game_over,
            'get_saving_name': self.get_saving_name
        }

    def draw(self, pause: bool = False):
        self.current_level.scene.draw_obj(pause)

    def switch_running(self):
        self.game_running = not self.game_running

    def get_running_current_level(self):
        self.current_level.get_level_running()

    def switch_current_level(self, level: Level | None = None):
        self.current_level = level
        if level is not None:
            if not self.current_level.get_level_running():
                self.current_level.switch_level_running()

    def run(self):
        current_command = self.current_level.run()
        if current_command is None:
            self.switch_running()
        elif not current_command.startswith('load'):
            self.commands_dict[current_command]()
        else:
            self.load_level(current_command.split(':')[1])

    def to_play(self):
        self.switch_current_level(LevelCreator.create_lvl1())

    def to_play_from_pause(self):
        self.switch_current_level(self.paused_level)
        self.paused_level = None

    def to_menu(self):
        self.switch_current_level(LevelCreator.create_menu_lvl())

    def to_pause(self):
        self.paused_level = self.current_level
        self.switch_current_level(LevelCreator.create_pause_lvl(self.current_level.scene))

    def get_load_level_name(self):
        self.current_level.scene, self.current_level.buttons = Helper.create_menu_level_loader_scene(self.saved_levels)
        self.current_level.is_loading = True

    def load_level(self, level_name: str):
        level_to_load = self.saved_levels[level_name]

        scene, player, score_counter, platforms = Helper.create_level_copy(level_to_load)
        copied_level_to_load = GameplayLevel(scene, player, score_counter, platforms)
        Helper.copy_enemies_and_fireballs(copied_level_to_load, level_to_load)

        self.switch_current_level(copied_level_to_load)

    def game_over(self):
        record_status = self.update_score_record(self.current_level.score_counter.score)
        new_level = LevelCreator.create_game_over_lvl(self.current_level.score_counter, record_status)
        self.switch_current_level(new_level)

    def save_level(self):
        scene, player, score_counter, platforms = Helper.create_level_copy(self.paused_level)
        saved_level = GameplayLevel(scene, player, score_counter, platforms)
        Helper.copy_enemies_and_fireballs(saved_level, self.paused_level)
        self.saved_levels.update({self.current_level.saving_name_tracker.text: saved_level})

    def get_saving_name(self):
        self.current_level.get_saving_name()

    def quit(self):
        self.current_level.switch_level_running()
        self.switch_current_level()

    def update_score_record(self, score):
        record_status = False
        if score > self.score_record:
            self.score_record = score
            record_status = True

        return record_status
