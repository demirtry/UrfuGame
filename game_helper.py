import pygame
from objects import Scene, Player, VisibleObject, Button, TextBoxCreator, Enemy, FireBall, Platform, ScoreCounter, TextTracker
from mathematical_funcs import img_multiplication, degree_calculation, img_rotation, generate_enemy_position
from working_with_files import clear_directory, check_directory


class Helper:

    screen = pygame.display.set_mode((1024, 768))

    @staticmethod
    def create_level1_bg():
        start_background_x = -188
        start_background_y = -165
        background_picture = pygame.image.load('images/backgrounds/background_gameplay.png')
        bg = VisibleObject(start_background_x, start_background_y, [[background_picture]])

        return bg

    @staticmethod
    def create_player():

        # base_player_x = 503
        # base_player_y = 674

        # player between platforms
        base_player_x = 320 + 32 - 9
        base_player_y = 720 + 24 - 70

        player_idle_left = [
            pygame.image.load('images/player_images/idle/left/player_idle1_left.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/left/player_idle2_left.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/left/player_idle3_left.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/left/player_idle4_left.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/left/player_idle5_left.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/left/player_idle6_left.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/left/player_idle7_left.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/left/player_idle8_left.png').convert_alpha()
        ]

        player_idle_right = [
            pygame.image.load('images/player_images/idle/right/player_idle1_right.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/right/player_idle2_right.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/right/player_idle3_right.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/right/player_idle4_right.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/right/player_idle5_right.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/right/player_idle6_right.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/right/player_idle7_right.png').convert_alpha(),
            pygame.image.load('images/player_images/idle/right/player_idle8_right.png').convert_alpha()
        ]

        player_walk_left = [
            pygame.image.load('images/player_images/walk/left/player_walk1_left.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/left/player_walk2_left.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/left/player_walk3_left.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/left/player_walk4_left.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/left/player_walk5_left.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/left/player_walk6_left.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/left/player_walk7_left.png').convert_alpha(),
        ]

        player_walk_right = [
            pygame.image.load('images/player_images/walk/right/player_walk1_right.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/right/player_walk2_right.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/right/player_walk3_right.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/right/player_walk4_right.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/right/player_walk5_right.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/right/player_walk6_right.png').convert_alpha(),
            pygame.image.load('images/player_images/walk/right/player_walk7_right.png').convert_alpha(),
        ]

        player_run_left = [
            pygame.image.load('images/player_images/run/left/player_run1_left.png').convert_alpha(),
            pygame.image.load('images/player_images/run/left/player_run2_left.png').convert_alpha(),
            pygame.image.load('images/player_images/run/left/player_run3_left.png').convert_alpha(),
            pygame.image.load('images/player_images/run/left/player_run4_left.png').convert_alpha(),
            pygame.image.load('images/player_images/run/left/player_run5_left.png').convert_alpha(),
            pygame.image.load('images/player_images/run/left/player_run6_left.png').convert_alpha(),
            pygame.image.load('images/player_images/run/left/player_run7_left.png').convert_alpha(),
            pygame.image.load('images/player_images/run/left/player_run8_left.png').convert_alpha()
        ]

        player_run_right = [
            pygame.image.load('images/player_images/run/right/player_run1_right.png').convert_alpha(),
            pygame.image.load('images/player_images/run/right/player_run2_right.png').convert_alpha(),
            pygame.image.load('images/player_images/run/right/player_run3_right.png').convert_alpha(),
            pygame.image.load('images/player_images/run/right/player_run4_right.png').convert_alpha(),
            pygame.image.load('images/player_images/run/right/player_run5_right.png').convert_alpha(),
            pygame.image.load('images/player_images/run/right/player_run6_right.png').convert_alpha(),
            pygame.image.load('images/player_images/run/right/player_run7_right.png').convert_alpha(),
            pygame.image.load('images/player_images/run/right/player_run8_right.png').convert_alpha(),
        ]

        player_lst_of_anim_lst = [player_idle_left, player_idle_right, player_walk_left,
                                  player_walk_right, player_run_left, player_run_right]

        start_player = Player(base_player_x, base_player_y, player_lst_of_anim_lst)

        return start_player

    @staticmethod
    def create_score_counter_objects():

        score_bg_img = pygame.image.load('images/jungle_counter_bg.png')
        score_bg_obj = VisibleObject(830, 0, [[score_bg_img]])

        score_counter = ScoreCounter(870, 25)

        return score_bg_obj, score_counter

    @staticmethod
    def create_level1_objects(player: Player = None):
        if player is None:
            player = Helper.create_player()

        # platforms = [
        #     Helper.create_platform(96, 648, 5),
        #     Helper.create_platform(256, 552, 5),
        #     Helper.create_platform(384, 432, 3),
        #     Helper.create_ground_platform(),
        #     Helper.create_platform(96, 720, 1),
        #     Helper.create_platform(96, 696, 1),
        #     Helper.create_platform(96, 672, 1),
        #     Helper.create_platform(320, 720, 1),
        #     Helper.create_platform(384, 720, 1),
        # ]

        # platforms = [
        #     Helper.create_ground_platform(),
        #     Helper.create_platform(96, 648, 5),
        #     Helper.create_platform(256, 552, 5),
        #     Helper.create_platform(384, 432, 3),
        #     Helper.create_platform(448, 312, 3),
        #     Helper.create_platform(512, 216, 2),
        #     Helper.create_platform(384, 168, 2),
        # ]

        platforms = [
            Helper.create_ground_platform(),
            Helper.create_platform(96, 648, 5),
            Helper.create_platform(0, 648 - 24*4, 2),
            Helper.create_platform(32*3, 648 - 24*8, 3),
            # Helper.create_platform(32*6, 648 - 24*12, 1),
            Helper.create_platform(256, 552, 5),
            # Helper.create_platform(384, 432, 3),
            Helper.create_platform(448 - 32 * 6, 312 - 24, 3),
            Helper.create_platform(512 - 32*4, 216, 2),
            Helper.create_platform(384, 168, 2),
            Helper.create_platform(1024-32*8, 648 - 24, 3),
            Helper.create_platform(1024-32*12, 648 - 24 * 5, 2),
            Helper.create_platform(32, 648 - 24 * 12, 2)

        ]

        score_bg_obj, score_counter = Helper.create_score_counter_objects()

        scene = Scene(Helper.screen, Helper.create_level1_bg(), player, score_bg_obj, score_counter)

        scene.append_obj(*platforms)

        return scene, player, score_counter, platforms

    @staticmethod
    def create_menu_scene():
        menu_x = -80
        menu_y = 0

        menu_btn1 = Button(512 - 65, 150, 'arial', 'Играть', 50, (152, 13, 243), (206, 31, 107))
        menu_btn2 = Button(512 - 282 // 2, 250, 'arial', 'Загрузить игру', 50, (152, 13, 243), (206, 31, 107))
        menu_btn3 = Button(512 - 61, 350, 'arial', 'Выйти', 50, (152, 13, 243), (206, 31, 107))

        menu_picture = pygame.image.load('images/backgrounds/menu_background2.png').convert()
        menu_obj = VisibleObject(menu_x, menu_y, [[menu_picture]])

        menu_scene = Scene(Helper.screen, menu_obj, menu_btn1, menu_btn2, menu_btn3)
        buttons = [menu_btn1, menu_btn2, menu_btn3]

        return menu_scene, buttons

    @staticmethod
    def create_menu_level_loader_scene(saved_levels: dict):

        saved_names = list(saved_levels.keys())

        buttons = []
        for i in range(len(saved_names)):
            button_x = 512 - TextBoxCreator.create_text_img('arial', saved_names[i], 50, (152, 13, 243)).get_rect().size[0] // 2
            buttons.append(Button(button_x, 190 + 75 * i, 'arial', saved_names[i], 50, (152, 13, 243), (206, 31, 107)))

        menu_loader_picture = pygame.image.load('images/backgrounds/menu_background2.png').convert()
        menu_loader_obj = VisibleObject(-80, 0, [[menu_loader_picture]])

        if len(saved_names):
            loader_head_img = TextBoxCreator.create_text_img('arial', 'Выберите сохранение', 50, (12, 127, 145))

        else:
            loader_head_img = TextBoxCreator.create_text_img('arial', 'Сохранения не найдены', 50, (12, 127, 145))

        loader_head_x = 512 - loader_head_img.get_rect().size[0] // 2
        loader_head_obj = VisibleObject(loader_head_x, 110, [[loader_head_img]])

        back_button_y = 190 + 75 * len(saved_names)
        back_button = Button(512 - 119 // 2, back_button_y, 'arial', 'Назад', 50, (152, 13, 243),
                             (206, 31, 107))

        buttons.append(back_button)

        level_loader_scene = Scene(Helper.screen, menu_loader_obj, loader_head_obj)
        level_loader_scene.append_obj(*buttons)

        return level_loader_scene, buttons

    @staticmethod
    def turn_scene_to_pause(pause):
        new_scene = Scene(Helper.screen)
        for obj in pause.scene.obj_lst:
            new_scene.append_obj(obj)
        pause.update_scene(new_scene)

        pause_scene_img = pygame.image.load('images/backgrounds/pause.jpg').convert()
        pause_scene_obj = VisibleObject(128, 96, [[pause_scene_img]])

        pause_head_img = TextBoxCreator.create_text_img('arial', 'Игра на паузе', 50, (12, 127, 145))
        pause_head_obj = VisibleObject(512 - 266 // 2, 210, [[pause_head_img]])
        pause_btn1 = Button(512 - 237 // 2, 320, 'arial', 'Продолжить', 50, (152, 13, 243), (206, 31, 107))
        pause_btn2 = Button(512 - 299 // 2, 415, 'arial', 'Сохранить игру', 50, (152, 13, 243), (206, 31, 107))
        pause_btn3 = Button(512 - 272 // 2, 510, 'arial', 'Выйти в меню', 50, (152, 13, 243), (206, 31, 107))
        pause.scene.append_obj(pause_scene_obj, pause_head_obj, pause_btn1, pause_btn2, pause_btn3)

        pause.buttons.append(pause_btn1)
        pause.buttons.append(pause_btn2)
        pause.buttons.append(pause_btn3)

    @staticmethod
    def turn_scene_to_get_saving_name(scene: Scene):

        new_scene = Scene(Helper.screen)
        for obj in scene.obj_lst:
            new_scene.append_obj(obj)

        saving_bg_img = pygame.image.load('images/backgrounds/pause.jpg').convert()
        saving_bg_obj = VisibleObject(128, 96, [[saving_bg_img]])

        saving_name_head_img = TextBoxCreator.create_text_img('arial', 'Введите имя', 50, (12, 127, 145))
        saving_name_head_obj = VisibleObject(512 - 245 // 2, 210, [[saving_name_head_img]])

        saving_name_getter_img = pygame.image.load('images/backgrounds/saving_name_getter_bg.png').convert_alpha()
        saving_name_getter_obj = VisibleObject(512 - 325 // 2, 295, [[saving_name_getter_img]])

        new_scene.append_obj(saving_bg_obj, saving_name_head_obj, saving_name_getter_obj)

        return new_scene

    @staticmethod
    def create_text_tracker_for_saving_name():
        return TextTracker(400, 393, 45)

    @staticmethod
    def create_level_copy(level):
        copied_scene = Scene(Helper.screen)
        copied_player = Helper.create_player()
        copied_player.current_animation_ind = level.player.current_animation_ind
        copied_player.current_animation_lst_ind = level.player.current_animation_lst_ind
        copied_player.x = level.player.x
        copied_player.y = level.player.y
        copied_player.turn = level.player.turn
        copied_player.jump = level.player.jump
        copied_player.fall = level.player.fall
        copied_player.current_cnt_steps = level.player.current_cnt_steps
        copied_player.jump_count = level.player.jump_count
        copied_platforms = level.platforms.copy()
        score_counter_bg, copied_score_counter = Helper.create_score_counter_objects()
        copied_score_counter.update_score(level.score_counter.score)
        copied_score_counter.update_image()

        copied_scene.append_obj(Helper.create_level1_bg(), copied_player, score_counter_bg, copied_score_counter)
        copied_scene.append_obj(*copied_platforms)

        return copied_scene, copied_player, copied_score_counter, copied_platforms

    @staticmethod
    def copy_enemy(enemy):
        new_enemy = Enemy(enemy.x, enemy.y, enemy.lst_of_animation_lst.copy())
        new_enemy.animation_cnt = enemy.animation_cnt
        new_enemy.current_animation_lst_ind = enemy.current_animation_lst_ind
        new_enemy.current_bfs_index = enemy.current_bfs_index
        new_enemy.current_action = enemy.current_action

        return new_enemy

    @staticmethod
    def copy_fireball(fireball):
        new_fireball = FireBall(fireball.x, fireball.y, fireball.lst_of_animation_lst.copy())
        new_fireball.trajectory = fireball.trajectory
        new_fireball.current_animation_ind = fireball.current_animation_ind

        return new_fireball

    @staticmethod
    def copy_enemies_and_fireballs(new_level, old_level):

        new_level.enemy_timer_count = old_level.enemy_timer_count
        copied_enemies = []
        copied_fireballs = []

        for enemy in old_level.enemies:
            copied_enemy = Helper.copy_enemy(enemy)
            copied_enemies.append(copied_enemy)

        for fireball in old_level.fireballs:
            copied_fireball = Helper.copy_fireball(fireball)
            copied_fireballs.append(copied_fireball)

        new_level.enemies = copied_enemies
        new_level.fireballs = copied_fireballs

        new_level.scene.append_obj(*copied_enemies)
        new_level.scene.append_obj(*copied_fireballs)

    @staticmethod
    def create_platform(platform_x, platform_y, size):
        check_directory()
        base_platform_path = 'images/jungle_platform.png'
        final_platform_path = f'images/dynamic/jungle_platform_{size}.png'
        img_multiplication(base_platform_path, final_platform_path, size)
        ground_platform_img = pygame.image.load(final_platform_path).convert_alpha()
        platform_obj = Platform(platform_x, platform_y, [[ground_platform_img]])
        clear_directory()
        return platform_obj

    @staticmethod
    def create_ground_platform():
        return Helper.create_platform(0, 744, 32)

    @staticmethod
    def create_enemy(tiles, player):

        enemy_walk_left = [
            pygame.image.load('images/enemy_images/walk/walk_left/enemy_walk_left_3.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_left/enemy_walk_left_2.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_left/enemy_walk_left_-1.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_left/enemy_walk_left_1.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_left/enemy_walk_left_0.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_left/enemy_walk_left_1.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_left/enemy_walk_left_-1.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_left/enemy_walk_left_2.png').convert_alpha()
        ]

        enemy_walk_right = [
            pygame.image.load('images/enemy_images/walk/walk_right/enemy_walk_right_3.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_right/enemy_walk_right_2.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_right/enemy_walk_right_-1.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_right/enemy_walk_right_1.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_right/enemy_walk_right_0.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_right/enemy_walk_right_1.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_right/enemy_walk_right_-1.png').convert_alpha(),
            pygame.image.load('images/enemy_images/walk/walk_right/enemy_walk_right_2.png').convert_alpha()
        ]

        enemy_x, enemy_y, enemy_turn = generate_enemy_position(tiles, player)
        enemy = Enemy(enemy_x, enemy_y, [enemy_walk_left, enemy_walk_right], enemy_turn)

        return enemy

    @staticmethod
    def create_fireball(player: Player):

        start_coordinates = player.get_coordinates()
        fireball_coordinates = (start_coordinates[0]+9, start_coordinates[1] + 24)
        degree_coordinates = (start_coordinates[0] + 25 + 9, start_coordinates[1] + 35)

        mouse_position = pygame.mouse.get_pos()
        degree = degree_calculation(degree_coordinates, mouse_position)

        fireball_img_up = img_rotation('images/fireball_images/base_fireball_up.png', degree)
        fireball_img_down = img_rotation('images/fireball_images/base_fireball_down.png', degree)

        fireball_movement = [fireball_img_up, fireball_img_down, fireball_img_up, fireball_img_up]

        fireball_explosion = [
            pygame.image.load('images/fireball_images/fireball_boom1.png'),
            pygame.image.load('images/fireball_images/fireball_boom2.png'),
            pygame.image.load('images/fireball_images/fireball_boom3.png'),
            pygame.image.load('images/fireball_images/fireball_boom4.png')
        ]

        fireball = FireBall(fireball_coordinates[0], fireball_coordinates[1], [fireball_movement, fireball_explosion], mouse_position)
        return fireball

    @staticmethod
    def create_game_over_objects(score_counter: ScoreCounter, record_status):

        game_over_picture = pygame.image.load('images/backgrounds/game_over_bg.jpg').convert()
        game_over_bg_obj = VisibleObject(0, 0, [[game_over_picture]])

        game_over_center_img = pygame.image.load('images/backgrounds/game_over_bg_2.jpg').convert()
        game_over_center_obj = VisibleObject(312, 110, [[game_over_center_img]])

        game_over_head_img = TextBoxCreator.create_text_img('arial', 'Game over!', 60, (115, 209, 209))
        game_over_head_obj = VisibleObject(512 - 256 // 2, 150, [[game_over_head_img]])

        score_img = TextBoxCreator.create_text_img('arial', score_counter.update_text(), 35, (255, 255, 255))
        score_obj_x = 512 - score_img.get_rect().size[0] // 2
        score_obj = VisibleObject(score_obj_x, 240, [[score_img]])

        game_over_btn1 = Button(512 - 252//2, 400, 'arial', 'Играть снова', 50, (255, 255, 255), (58, 85, 201))
        game_over_btn2 = Button(512 - 272//2, 500, 'arial', 'Выйти в меню', 50, (255, 255, 255), (58, 85, 201))

        game_over_scene = Scene(Helper.screen, game_over_bg_obj, game_over_center_obj, game_over_head_obj, score_obj, game_over_btn1, game_over_btn2)

        if record_status:
            score_record_head = TextBoxCreator.create_text_img('arial', 'New record!', 35, (115, 209, 209))
            score_record_head_obj = VisibleObject(512 - 156 // 2, 315, [[score_record_head]])
            game_over_scene.append_obj(score_record_head_obj)

        buttons = [game_over_btn1, game_over_btn2]

        return game_over_scene, buttons
