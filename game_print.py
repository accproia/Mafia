from game import Game

class GamePrint:

    def __init__(self, game:Game) -> None:
        self.game = game

    def print_mafia_players(self) -> None:
        print(", ".join(str(maf) for maf in self.game.mafia))

    def print_civilians(self, show_sherif:bool) -> None:
        str_civilians_with_sherrif = [(str(i)+"*" if i == self.game.sheriff and show_sherif else str(i)) for i in self.game.civilians]
        print(", ".join(str_civilians_with_sherrif))

    def your_input(self, speech_quality:int) -> None:
        input("player {} with speach {}%:".format( 
                self.game.you, 
                speech_quality))

    def print_player_turn(self, player:int, play_with:list, speech_quality:int) -> None:
        
        # sort 
        play_with = sorted(play_with)

        # print
        print("player {} with speech {}% plays with {}".format(
            player, 
            speech_quality, 
            ", ".join(str(i) for i in play_with)), end="")

    def print_your_info(self):
        print("You are player #{}".format(str(self.game.you) + ("*" if self.game.you == self.game.sheriff else "")))

    def print_current_cycle(self, turn:int):
        print("Current turn: {}".format(turn))

    def press_any_key_to_continue(self):
        input()
    