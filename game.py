import random

class Game:

    mafia = set()
    civilians = set()
    sheriff = 0
    you = 0

    def get_random_civilian(self):
        return [i for i in range(1,11) if i not in self.mafia][random.randint(0, 6)]

    def __init__(self) -> None:
        self.mafia = sorted(set(random.sample(range(1,11), 3)))
        self.civilians = set(range(1,11)).symmetric_difference(self.mafia)
        self.sheriff = self.get_random_civilian()
        self.you = self.get_random_civilian()
        