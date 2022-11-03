import random
from game import Game
from game_print import GamePrint
from game_play import GamePlay

# init game
game = Game()
game_print = GamePrint(game)
game_print.print_your_info()

# first turn
turn = 0
game_print.print_current_cycle(turn)

# init game play
game_play = GamePlay(game, game_print)

while game_play.make_turn():
    turn += 1

print()

input("Press Enter to print players")

game_print.print_mafia_players()
game_print.print_civilians(show_sherif=True)