import pygame
from game import Game


if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption('my Game')

    icon = pygame.image.load('images/game_icon/GameIcon.png')
    pygame.display.set_icon(icon)

    my_game = Game()

    while my_game.game_running:
        my_game.run()

    pygame.quit()
