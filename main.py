import random
from game import Game
from game_print import GamePrint
from game_play import GamePlay

# init game
game = Game()
game_print = GamePrint(game)
print("You are player #{}".format(game.you))

# first turn
turn = 0
print("current turn: {}".format(turn))

# init game play
game_play = GamePlay(game, game_print)

while game_play.make_turn():
    pass

print()

input("Press Enter to print players")

game_print.print_mafia_players()
game_print.print_civilians(show_sherif=True)