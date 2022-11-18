from game import Game
from game_print import GamePrint, Smiles
import random

# constants
new_line_str = "\r\n"


class Action:
    pass

class ButtonPressed(Action):
    def __init__(self, button_name:str):
        self.button_name = button_name


class State:
    def __init__(self, game_play, game_print:GamePrint):
        self.game_play = game_play
        self.game_print = game_print

    def is_end(self) -> bool:
        return False

    def erasable(self) -> bool:
        return False

    def do(self):
        pass

    def print(self) -> tuple[str, any]:
        return ("", None)
    
    def get_next(self, action:Action):
        return End(self.game_play, self.game_print)


class InlineButton:
    def __init__(self, text:str, name:str):
        self.text = text
        self.name = name





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

    def get_first_state(self) -> State:
        return Beginning(self, self.game_print)

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

    def your_number(self) -> int:
        return self.game.you

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


    def make_others_player_turn(self, player:int) -> set:

        self.calc_speech_quality(player)
        
        play_with = set()
        self.common_play_with_yourself(player, play_with)

        if player in self.game.mafia:
            self.maf_play_with_mates(play_with)

        self.common_play_with_other(player, play_with)
        
        self.exclude_unknow_play_with(player, play_with)
        return play_with




# the first state
# shows information about you (role, sherrif or not)
class Beginning(State):

    def do(self):
        pass

    def print(self) -> tuple[str, any]:

        text = self.game_print.print_your_info() + new_line_str
        text += self.game_print.print_current_cicle(self.game_play.turn)

        return (text, None)

    def _get_next_turn(self, player:int) -> State:
        if self.game_play.your_number() == player:
            return YourTurn(player, self.game_play, self.game_print)
        else:
            return OthersTurn(player, self.game_play, self.game_print)
    
    def get_next(self, action:Action) -> State:
        # start with first player
        return self._get_next_turn(1)
        
# player turn
class PlayerTurn(State):
    play_with = set()
    
    def __init__(self, player:int, game_play:GamePlay, game_print:GamePrint):
        super().__init__(game_play, game_print)
        self.player = player
    
    def _get_next_turn(self, player:int) -> State:
        if self.game_play.your_number() == player:
            return YourTurn(player, self.game_play, self.game_print)
        else:
            return OthersTurn(player, self.game_play, self.game_print)
    
    def erasable(self) -> bool:
        return True
    
    def get_next(self, action:Action) -> State:

        if self.player == 10:
            return End(self.game_play, self.game_print)

        self.player = self.player % 10 + 1
        return self._get_next_turn(self.player)

# other's turn
class OthersTurn(PlayerTurn):
    
    def do(self):
        self.play_with = self.game_play.make_others_player_turn(self.player)

    def print(self) -> tuple[str, any]:
        text = self.game_print.print_player_turn(self.player, self.play_with, self.game_play.speech_qualities[self.player])
        return (text, None)
    

# your turn
class YourTurn(PlayerTurn):
    
    def do(self):
        self.game_play.calc_speech_quality(self.player)
        
    def _get_button(self, idx:int) -> InlineButton:
        white_check_mark = Smiles.white_check_mark
        return InlineButton( str(idx) + white_check_mark if idx in self.play_with else str(idx), str(idx) )

    def print(self) -> tuple[str, any]:

        text = self.game_print.print_player_turn(self.player, self.play_with, self.game_play.speech_qualities[self.player])
        buttons = [[self._get_button(i) for i in range(1, 6) if i != self.player],
                   [self._get_button(i) for i in range(6, 11) if i != self.player]
        ]

        return (text, buttons)

    def get_next(self, action: Action) -> State:

        if type(action) == ButtonPressed:
            player_to_play_with = None
            try:
                player_to_play_with = int(action.button_name)
            except:
                pass
            if type(player_to_play_with) == int:
                self.play_with ^= set([player_to_play_with])
                your_turn = YourTurn(self.player, self.game_play, self.game_print)
                your_turn.play_with = self.play_with
                return your_turn

        return super().get_next(action)
    
# the end state
# return this to end the game
class End(State):

    def print(self) -> tuple[str, any]:
        
        text = self.game_print.print_mafia_players() + new_line_str
        text += self.game_print.print_civilians(show_sherif=True)

        return (text, None)

    def is_end(self) -> bool:
        return True
    