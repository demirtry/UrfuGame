import pygame
from game import Game, Scene, Level, LevelWithButtons
from game_helper import Helper
from objects import Player, Platform, Button, ScoreCounter
from BFS import BreadthFirstSearch


class LevelCreator:
    @staticmethod
    def create_lvl1():
        scene, player, score_counter, platforms = Helper.create_level1_objects()
        return Level1(scene, player, score_counter, platforms)

    @staticmethod
    def create_menu_lvl():
        menu_scene, buttons = Helper.create_menu_scene()
        return Menu(menu_scene, buttons)

    @staticmethod
    def create_pause_lvl(scene: Scene):
        return Pause(scene)


class Level1(Level):
    def __init__(self, scene: Scene, player: Player, score_counter: ScoreCounter, platforms: list[Platform],
                 bfs_cooldown: int = 4):
        super().__init__(scene)
        self.player = player
        self.score_counter = score_counter
        self.platforms = platforms
        self.enemies = []
        self.fireballs = []
        self.pause = False
        self.bfs = BreadthFirstSearch(self.platforms)
        self.bfs_cooldown = bfs_cooldown
        self.enemy_timer_count = 0

    def collide(self, key):
        collide_status = False

        current_speed = self.player.speed
        if self.player.current_animation_lst_ind in [4, 5]:
            current_speed += 4

        if key == pygame.K_a or key == pygame.K_d:

            if key == pygame.K_a:
                self.player.x -= current_speed
            else:
                self.player.x += current_speed

            player_rect = self.player.get_rect()
            for platform in self.platforms:
                if pygame.Rect.colliderect(player_rect, platform.get_rect()):
                    collide_status = True
                    break

            if key == pygame.K_a:
                self.player.x += current_speed
            else:
                self.player.x -= current_speed

        return collide_status

    def collide_up(self):
        collide_status = False
        self.player.y -= (self.player.jump_count ** 2) // 2
        player_rect = self.player.get_rect()
        for platform in self.platforms:
            if pygame.Rect.colliderect(player_rect, platform.get_rect()):
                self.player.y = platform.get_coordinates()[1] + 26
                collide_status = True
                break
        if collide_status or self.player.y <= 2:
            self.player.jump = False
            self.player.jump_count = 0
        else:
            self.player.y += (self.player.jump_count ** 2) // 2
        return collide_status

    def collide_fall(self):
        collide_status = False
        self.player.y += self.player.gravity
        player_rect = self.player.get_rect()
        for platform in self.platforms:
            if pygame.Rect.colliderect(player_rect, platform.get_rect()):
                self.player.y = platform.get_coordinates()[1] - 70
                collide_status = True
                self.player.jump = False
                break
        if collide_status:
            self.player.jump_count = self.player.jump_size
            self.player.fall = False
        else:
            self.player.y -= self.player.gravity
            if not self.player.jump and self.player.y != 674:
                self.player.fall = True

        return collide_status

    def collide_with_enemies(self):
        collide_status = False
        player_rect = self.player.get_rect()
        for enemy in self.enemies:
            if pygame.Rect.colliderect(player_rect, enemy.get_rect()):
                collide_status = True
                print('You die')
                break

    def shoot(self):
        fireball = Helper.create_fireball(self.player)
        self.scene.append_obj(fireball)
        self.fireballs.append(fireball)

    def move_fireballs(self):
        updated_fireballs = []
        for fireball in self.fireballs:
            fireball.move()

            if fireball.check_position():
                updated_fireballs.append(fireball)
            else:
                self.scene.remove_obj(fireball)

        self.fireballs = updated_fireballs

    def collide_fireballs(self):
        updated_fireballs = []
        for fireball in self.fireballs:
            if not fireball.current_animation_lst_ind:
                collide_status = False
                fireball_rect = fireball.get_rect()
                for platform in self.platforms:
                    if pygame.Rect.colliderect(fireball_rect, platform.get_rect()):
                        collide_status = True
                        break

                if not collide_status:
                    for enemy in self.enemies:
                        if pygame.Rect.colliderect(fireball_rect, enemy.get_rect()):
                            collide_status = True
                            self.enemies.remove(enemy)
                            self.scene.remove_obj(enemy)
                            self.score_counter.calculate()
                            break

                updated_fireballs.append(fireball)
                if collide_status:
                    fireball.explode()
            else:
                if fireball.current_animation_ind != 3:
                    updated_fireballs.append(fireball)
                else:
                    self.scene.remove_obj(fireball)
        self.fireballs = updated_fireballs

    def move_enemies(self):
        for enemy in self.enemies:
            if not enemy.current_bfs_index:
                current_enemy_action = self.bfs.find_way(enemy.get_current_tile(), self.player.get_current_tile())
                enemy.current_action = current_enemy_action
                enemy.current_bfs_index = self.bfs_cooldown
            enemy.move(enemy.current_action)
            enemy.current_bfs_index -= 1

    def spawn_enemy(self):
        enemy = Helper.create_enemy(self.bfs.tiles, self.player)
        self.enemies.append(enemy)
        self.scene.append_obj(enemy)

    def run(self):

        enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(enemy_timer, 3000 - self.enemy_timer_count * 30)

        while self.get_level_running():
            my_game.draw(self.pause)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    my_game.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    my_game.current_level.switch_level_running()
                    my_game.switch_current_level(LevelCreator.create_menu_lvl())
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    my_game.current_level.switch_level_running()
                    my_game.paused_level = self
                    my_game.switch_current_level(LevelCreator.create_pause_lvl(self.scene))
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.shoot()

                if event.type == enemy_timer:
                    self.spawn_enemy()
                    if 3000 - self.enemy_timer_count * 30 > 1030:
                        self.enemy_timer_count += 1
                    pygame.time.set_timer(enemy_timer, 3000 - self.enemy_timer_count * 30)

            keys = pygame.key.get_pressed()
            if ((keys[pygame.K_SPACE] and not self.player.jump) or self.player.jump) and not self.player.fall:
                self.player.make_jump(self.collide_up())
            else:
                self.player.make_fall(self.collide_fall())

            if keys[pygame.K_a]:
                self.player.move_left(self.collide(pygame.K_a))
            elif keys[pygame.K_d]:
                self.player.move_right(self.collide(pygame.K_d))
            else:
                self.player.become_idle()

            self.move_fireballs()
            self.move_enemies()
            self.collide_with_enemies()
            self.collide_fireballs()

            clock.tick(15)


class Menu(LevelWithButtons):
    def __init__(self, scene: Scene, buttons: list[Button]):
        super().__init__(scene)
        self.buttons = buttons
        self.current_button_index = None
        self.buttons_callbacks = [self.to_play, self.to_play, self.quit]

    @staticmethod
    def to_play():
        my_game.current_level.switch_level_running()
        my_game.switch_current_level(LevelCreator.create_lvl1())

    @staticmethod
    def quit():
        my_game.quit()

    def run(self):
        while self.get_level_running():
            my_game.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    my_game.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.current_button_index is not None:
                    self.buttons_callbacks[self.current_button_index]()
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_s):
                    self.switch_button(event.key)

            clock.tick(15)


class Pause(LevelWithButtons):
    def __init__(self, scene: Scene):
        super().__init__(scene)
        Helper.turn_scene_to_pause(self)
        self.buttons_callbacks = [self.to_play, self.to_menu]

    @staticmethod
    def to_play():
        my_game.current_level.switch_level_running()
        my_game.switch_current_level(my_game.paused_level)
        my_game.paused_level = None

    @staticmethod
    def to_menu():
        my_game.current_level.switch_level_running()
        my_game.switch_current_level(LevelCreator.create_menu_lvl())

    def run(self):
        while self.get_level_running():
            my_game.draw(pause=True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    my_game.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.to_play()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.current_button_index is not None:
                    self.buttons_callbacks[self.current_button_index]()
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_s):
                    self.switch_button(event.key)

            clock.tick(15)


if __name__ == '__main__':

    clock = pygame.time.Clock()

    pygame.init()
    pygame.display.set_caption('my Game')

    icon = pygame.image.load('images/game_icon/GameIcon.png')
    pygame.display.set_icon(icon)

    menu = LevelCreator.create_menu_lvl()
    my_game = Game(menu, Helper.screen)

    while my_game.game_running:
        my_game.current_level.run()
        if my_game.current_level is None:
            my_game.switch_running()

    pygame.quit()
