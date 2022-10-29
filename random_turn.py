import random

# constants
probability_coef = [1.0, 1.0, 1.0, 0.95, 0.9, 0.85, 0.8]

# init players
mafia = sorted(set(random.sample(range(1,11), 3)))
civilians = set(range(1,11)).symmetric_difference(mafia)
get_random_civilian = lambda: [i for i in range(1,11) if i not in mafia][random.randint(0, 6)]
sheriff = get_random_civilian()
you = get_random_civilian()
print("You are player #{}".format(you))

# print players info lambdas
print_mafia_players = lambda: print(", ".join(str(maf) for maf in mafia))
print_civilians = lambda show_sherif: print(", ".join([(str(i)+"*" if i == sheriff and show_sherif else str(i)) for i in civilians]))

# first turn
turn = 0
print("current turn: {}".format(turn))

# randomize quality of speeches of players
calc_speech_quality = lambda i: random.randint(1, 100) if i in civilians else max(1, min(random.randint(1, 100) - 10, 100))
speech_qualities = [calc_speech_quality(i) for i in range(1,11)]
#print(", ".join("{}: {}%".format(i,j) for i, j in zip(range(1,11),speech_qualities)))

# sort players by quality of speach
sorted_players = list(zip(range(1,11), speech_qualities))
sorted_players.sort(key = lambda x: x[1], reverse=True)
#print(", ".join("{}: {}%".format(i, j) for i, j in sorted_players))

#    calculating and printing turn information by next rules:
# 1) every player plays with himself
# 2) if player is mafia he has a big change to play with his teammate
# 3) for the first turn every player plays only with players before him
# 4) every player plays with at most 7 players
# 5) probability to play with each other player, when there are more then 3 of them, decreases

for player in range(1,11):

    # play with yourself
    play_with = {player}

    # play with mafia mates
    if player in mafia:
        play_with.update({i for i in mafia if random.randint(0, 99) > 30})
    
    # add players to play with, considering probability 
    candidates = [i for i in sorted_players if i[0] not in play_with]
    
    for idx, probability in candidates:

        if len(play_with) >= 7:
            break

        probability = probability * probability_coef[len(play_with)]

        if random.randint(0, 100) < probability:
            play_with.add(idx)

    # exclude unknown players for first cyrcle
    if turn == 0:
        play_with.difference_update(set(range(player+1, 11)))

    # sort 
    play_with = sorted(play_with)

    # print
    print("player {} plays with {}".format(player, ", ".join(str(i) for i in play_with)), end="")

    input()

print()

input("Press Enter to print players")

print_mafia_players()
print_civilians(show_sherif=True)