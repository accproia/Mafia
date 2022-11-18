from game import Game
from game_config import GameConfig

class Smiles:
    white_check_mark = "\u2705" 

class GamePrint:

    def __init__(self, game:Game) -> None:
        self.game = game

    def print_mafia_players(self) -> str:
        return ", ".join(str(maf) for maf in self.game.mafia)

    def print_civilians(self, show_sherif:bool) -> str:
        str_civilians_with_sherrif = [(str(i)+"*" if i == self.game.sheriff and show_sherif else str(i)) for i in self.game.civilians]
        return ", ".join(str_civilians_with_sherrif)

    def print_player_turn(self, player:int, play_with:list, speech_quality:int) -> str:
        play_with = sorted(play_with)
        return "player {} with speech {}% plays with {}".format(
            player, 
            speech_quality, 
            ", ".join(str(i) for i in play_with))

    def print_your_info(self) -> str:
        return "You are player #{}".format(str(self.game.you) + ("*" if self.game.you == self.game.sheriff else ""))

    def print_current_cicle(self, turn:int) -> str:
        return "Current turn: {}".format(turn)

    