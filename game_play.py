from game import Game
from game_print import GamePrint
import random

class GamePlay:

    # constants
    probability_coef_civilians = [1.0, 1.0, 1.0, 0.95, 0.9, 0.85, 0.8]
    probability_coef_mafia = [1.0, 0.9, 0.9, 0.85, 0.8, 0.75, 0.7]
    probability_maf_play_with_mate = 0.6

    def __init__(self, game:Game, game_print:GamePrint) -> None:
        self.game = game
        self.game_print = game_print
        self.speech_qualities = {}
        self.turn = 0

    def calc_speech_quality(self, player:int) -> None:
        self.speech_qualities[player] = random.randint(1, 100) if player in self.game.civilians else max(1, min(random.randint(1, 100) - 10, 100))
        self.update_speech_qualities()

    def update_speech_qualities(self) -> None:
        self.sorted_players = list(self.speech_qualities.items())
        self.sorted_players.sort(key = lambda x: x[1], reverse=True)

    def make_turn(self) -> bool:
        for player in range(1,11):
            self.make_player_turn(player)

        self.turn += 1

        return False

    def your_turn(self) -> None:
        you = self.game.you
        self.game_print.your_input(self.speech_qualities[you])

    def common_play_with_yourself(self, player:int, play_with:set) -> None:
        play_with.add(player)
        return None, play_with

    def maf_play_with_mates(self, play_with:set) -> None:
        play_with.update({i for i in self.game.mafia if random.randint(0, 100) < self.probability_maf_play_with_mate * 100})
        return None, play_with

    def common_play_with_other(self, player:int, play_with:set) -> None:
        candidates = [i for i in self.sorted_players if i[0] not in play_with]
        
        for idx, probability in candidates:

            if len(play_with) >= 7:
                break

            isMafia = player in self.game.mafia
            probability_coef = self.probability_coef_mafia if isMafia else self.probability_coef_civilians  
            probability = probability * probability_coef[len(play_with)]

            if random.randint(0, 100) < probability:
                play_with.add(idx)
            
        return None, play_with

    def exclude_unknow_play_with(self, player:int, play_with:set) -> None:
        
        if self.turn == 0:
            play_with.difference_update(set(range(player+1, 11)))

        return None, play_with


    def make_player_turn(self, player:int) -> None:

        self.calc_speech_quality(player)
        
        if player == self.game.you:
            self.your_turn()
            return

        play_with = set()
        self.common_play_with_yourself(player, play_with)

        if player in self.game.mafia:
            self.maf_play_with_mates(play_with)

        self.common_play_with_other(player, play_with)
        
        self.exclude_unknow_play_with(player, play_with)

        self.game_print.print_player_turn(player, play_with, self.speech_qualities[player])

        self.game_print.press_any_key_to_continue()
