import pygame
from game_helper import Helper
from objects import Scene, ScoreCounter, Player, Platform, Button, EnemyTimerHelper
from BFS import BreadthFirstSearch
from level_types import Level, LevelWithButtons


class GameplayLevel(Level):
    def __init__(self, scene: Scene, player: Player, score_counter: ScoreCounter, platforms: list[Platform]):
        super().__init__(scene)
        self.player = player
        self.score_counter = score_counter
        self.platforms = platforms
        self.enemies = []
        self.fireballs = []
        self.pause = False
        self.bfs = BreadthFirstSearch(self.platforms)
        self.enemy_timer_helper = EnemyTimerHelper()

    def collide(self, key):
        collide_status = False

        current_speed = self.player.speed
        if self.player.current_animation_lst_ind in [4, 5]:
            current_speed += 4

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
                break

        return collide_status

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
                            enemy.health -= fireball.damage
                            if not enemy.health:
                                self.score_counter.update_stats(enemy.reward)
                                self.scene.remove_obj(enemy)
                                self.enemies.remove(enemy)
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
                # enemy.current_bfs_index = self.bfs_cooldown
                enemy.current_bfs_index = enemy.bfs_cooldown
            enemy.move(enemy.current_action)
            enemy.current_bfs_index -= 1

    def spawn_enemy(self):
        enemy = Helper.create_enemy(self.bfs.tiles, self.player, self.score_counter.score)
        self.enemies.append(enemy)
        self.scene.append_obj(enemy)

    def run(self):

        enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(enemy_timer, self.enemy_timer_helper.get_current_timing(self.score_counter.score))

        while True:
            self.scene.draw_obj(self.pause)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 'to_menu'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    return 'to_pause'
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.shoot()

                if event.type == enemy_timer:
                    self.spawn_enemy()
                    pygame.time.set_timer(enemy_timer, self.enemy_timer_helper.get_current_timing(self.score_counter.score))

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
            self.collide_fireballs()

            if self.collide_with_enemies():
                return 'game_over'

            self.clock.tick(15)


class Menu(LevelWithButtons):
    def __init__(self, scene: Scene, buttons: list[Button]):
        super().__init__(scene)
        self.buttons = buttons
        self.current_button_index = None
        self.buttons_callbacks = ['to_play', 'get_load_level_name', None]
        self.is_loading = False

    def run(self):
        while True:
            self.scene.draw_obj()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_s):
                    self.switch_button(event.key)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.current_button_index is not None:
                    if self.is_loading:

                        if self.current_button_index == len(self.buttons) - 1:
                            return 'to_menu'
                        else:
                            return f'load:{self.buttons[self.current_button_index].text}'

                    else:
                        return self.buttons_callbacks[self.current_button_index]

            self.clock.tick(15)


class Pause(LevelWithButtons):
    def __init__(self, scene: Scene):
        super().__init__(scene)
        self.basic_scene = self.scene
        self.to_pause_menu()
        self.buttons_callbacks = ['to_play_from_pause', 'get_saving_name', 'to_menu']
        self.is_saving = False
        self.saving_name_tracker = None

    def get_saving_name(self):
        self.scene = Helper.turn_scene_to_get_saving_name(self.basic_scene)
        self.is_saving = True
        self.saving_name_tracker = Helper.create_text_tracker_for_saving_name()
        self.scene.append_obj(self.saving_name_tracker)

    def to_pause_menu(self):
        self.scene = self.basic_scene
        self.buttons.clear()
        Helper.turn_scene_to_pause(self)
        self.is_saving = False

    def run(self):
        while True:
            self.scene.draw_obj(pause=True)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:
                    if self.is_saving:

                        if event.key == pygame.K_ESCAPE:
                            self.to_pause_menu()

                        elif event.key == pygame.K_BACKSPACE:
                            self.saving_name_tracker.update()

                        elif event.unicode.isalpha():
                            self.saving_name_tracker.update(event.unicode)

                        elif event.key == pygame.K_RETURN and len(self.saving_name_tracker.text):
                            self.to_pause_menu()
                            return 'save_level'
                    else:
                        if event.key == pygame.K_p:
                            return 'to_play_from_pause'

                        elif event.key == pygame.K_RETURN and self.current_button_index is not None:
                            return self.buttons_callbacks[self.current_button_index]

                        elif event.key == pygame.K_w or event.key == pygame.K_s:
                            self.switch_button(event.key)

            self.clock.tick(15)


class GameOver(LevelWithButtons):
    def __init__(self, scene: Scene, buttons: list[Button]):
        super().__init__(scene)
        self.buttons = buttons
        self.current_button_index = None
        self.buttons_callbacks = ['to_play', 'to_menu']

    def run(self):
        while True:
            self.scene.draw_obj()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    return 'to_play'

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.current_button_index is not None:
                    return self.buttons_callbacks[self.current_button_index]

                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_s):
                    self.switch_button(event.key)

            self.clock.tick(15)
