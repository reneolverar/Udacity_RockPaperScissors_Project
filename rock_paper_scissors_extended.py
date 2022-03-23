#!/usr/bin/env python3

"""This program plays a game of:
   1.- Rock, Paper, Scissors between two Players or in a Tournament
   2.- Rock, Paper, Scissors, Lizard, Spock between two Players
   and reports the scores of each round and the final score."""

import string, random, os, contextlib, math, time

"""The Player class is the parent class for all of the Players
in this game"""


class Player:

    # Each player can learn the competitor´s move to use in their next strategy
    def learn(self, my_move, their_move):
        self.my_move = my_move
        self.their_move = their_move

    # Create player ID to identify him in tournaments
    def create_id(self, ID):
        self.ID = ID


class RockPlayer(Player):  # Always choose rock

    def __init__(self):
        self.name = "RockPlayer"

    def move(self):
        return 'rock'


class RandomPlayer(Player):  # Choose random move

    def __init__(self):
        self.name = "RandomPlayer"

    def move(self):
        return random.choice(self.moves)


class ReflectPlayer(Player):  # Choose competitor´s last move

    def __init__(self):
        self.name = "ReflectPlayer"

    def move(self):
        if round == 1:  # Random for 1st move as there is no previous move
            return random.choice(self.moves)
        else:
            return self.their_move


class CyclePlayer(Player):  # Cycles through all the moves

    def __init__(self):
        self.name = "CyclePlayer"

    # Goes through all moves in random order,
    # repeats again in random order if more rounds than moves
    def move(self):
        mod = round % len(self.moves)
        if round == 1:
            random.shuffle(self.moves)
            return self.moves[mod]
        else:
            return self.moves[mod]


class HumanPlayer(Player):

    def __init__(self):
        self.name = "HumanPlayer"

    def move(self):  # Promts user to select move
        while True:
            if len(self.moves) == 3:
                p_move = input("Type 'Rock', 'Paper' or 'Scissors' "
                               "to play, 'quit' to leave > ").lower()
            else:
                p_move = input("Type 'Rock', 'Paper', 'Scissors' " +
                               "'Lizard' or 'Spock' "
                               "to play, 'quit' to leave > ").lower()
            if p_move == 'quit':
                return 'quit'
            elif p_move in self.moves:
                return p_move


class Game:

    # Defines players for Game and moves
    def __init__(self, p1, p2, game_type):
        self.p1 = p1
        self.p2 = p2
        if not hasattr(self.p1, 'ID'):
            self.p1.create_id(1)
            self.p2.create_id(2)
        if game_type == 'rps':
            self.p1.moves = ["rock", "paper", "scissors"]
            self.p2.moves = ["rock", "paper", "scissors"]
        else:
            self.p1.moves = ["rock", "paper", "scissors", "lizard", "spock"]
            self.p2.moves = ["rock", "paper", "scissors", "lizard", "spock"]

    def play_round(self):
        move1 = self.p1.move()  # Chooses move for player 1
        move2 = self.p2.move()  # Chooses move for player 2
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)
        print(f"Player {self.p1.ID}: {move1}  Player {self.p2.ID}: {move2}")
        if move1 == 'quit' or move2 == 'quit':
            return 'quit'
        elif move1 == move2:
            return 0  # Tie
        elif beats(move1, move2):
            return 1  # Player 1 wins
        else:
            return 2  # Player 2 wins

    def play_game(self, rounds=0):
        p1_wins = p2_wins = 0
        print("\nRock Paper Scissors, Go!")
        # Question: made "round" global to not have to pass it to each further
        # method. Is there a better way? Or should I always make such variable
        # instance variables?
        # Question: If I create the round variable under Class Game and not
        # inside a method and then try to assign it a value, I get an error.
        # Why, if the code runs top to bottom?
        global round

        if rounds == 0:
            while (True and rounds == 0):
                try:
                    rounds = int(input("Enter the number of rounds (>0) " +
                                       "you want to play: \n"))
                except ValueError:
                    print("\nOops!  That was no valid number.  Try again...\n")
        else:
            rounds = rounds

        if isinstance(self.p1, HumanPlayer):
            print("Welcome to the game, you are Player 1")

        for round in range(1, rounds + 1):
            print(f"\nRound {round}:")
            outcome = self.play_round()
            if outcome == 'quit':
                print("\nThe game was cancelled\n")
                return 'quit'
            elif outcome == 1:  # Player 1 wins, mark with color green
                print(f"\u001b[32mPlayer {self.p1.ID} wins\u001b[0m")
                p1_wins += 1
            elif outcome == 2:  # Player 2 wins, mark with color green
                print(f"\u001b[32mPlayer {self.p2.ID} wins\u001b[0m")
                p2_wins += 1
            else:  # Tie, mark with color yellow
                print(f"\u001b[33m** TIE **\u001b[0m")
            # Define colors for current total score
            if p1_wins > p2_wins:
                color1 = '\u001b[32m'
                color2 = '\u001b[31m'
            elif p1_wins < p2_wins:
                color1 = '\u001b[31m'
                color2 = '\u001b[32m'
            else:
                color1 = color2 = '\u001b[33m'
            print(f"Score > {color1}Player {self.p1.ID} = {p1_wins}," +
                  f"{color2}Player {self.p2.ID} = {p2_wins}\u001b[0m")

        # Define colors for final score
        if p1_wins == p2_wins:
            final_score = "\n\u001b[33mIt's a tie!\u001b[0m"
            color1 = color2 = '\u001b[33m'
            self.outcome = 0
        elif p1_wins > p2_wins:
            final_score = f"\n\u001b[32mPlayer {self.p1.ID} wins\u001b[0m"
            color1 = '\u001b[32m'
            color2 = '\u001b[31m'
            self.outcome = 1
        elif p2_wins > p1_wins:
            final_score = f"\n\u001b[32mPlayer {self.p2.ID} wins\u001b[0m"
            color1 = '\u001b[31m'
            color2 = '\u001b[32m'
            self.outcome = 2

        print(f"\nFinal Score > {final_score}\n" +
              f"{color1}Player {self.p1.ID} = {p1_wins}, " +
              f"{color2}Player {self.p2.ID} = {p2_wins}\u001b[0m")
        return self.outcome


class Tournament:

    # Main method: creates players, cycles through rounds, prints winner
    def play_tournament(self, num_participants, player_type,
                        game_rounds, print_results):
        self.tournament_round = 1
        self.game_rounds = game_rounds
        self.print_results = print_results
        print(f"\nLet the games begin! The tournament has {num_participants}" +
              f" players - {int(math.sqrt(num_participants))} rounds\n")
        self.num_participants = num_participants
        self.create_players(num_participants, player_type)

        # Avoid starting tournament with conflicting strategies
        # (i.e. all playing always "rock") (problem of infinite loop)
        while self.conflicting_strategies(self.participants):
            print("Conflicting strategies - New players were defined\n")
            self.participants.clear()
            self.create_players(num_participants, player_type)

        while len(self.participants) > 1:
            print(f"\nStarting Tournament round: {self.tournament_round}")
            round_outcome = self.play_round(self.participants)
            if round_outcome == "Conflicting strategies!":
                print("\nSorry, the tournament cannot continue, " +
                      "we have a tie between the following players:")
                for ID in range(len(self.participants)):
                    print(f"Participant {self.participants[ID].ID} " +
                          f"Strategy: {type(self.participants[ID]).__name__}")
                print()
                return 'Conflicting strategies!'
            elif round_outcome == 'quit':
                return 'quit'
            else:
                if player_type == "h":
                    if isinstance(self.participants[0], HumanPlayer):
                        print("\nCongratulations, you won the round")
                        time.sleep(5)
                    else:
                        print("\nYou lost, the tournament will " +
                              "continue without you")
                        time.sleep(5)
                if len(self.participants) == 1:
                    print(f"\nWinner of round {self.tournament_round} is:")
                else:
                    print(f"\nWinners of round {self.tournament_round} are:")
                for ID in range(len(self.participants)):
                    if player_type == "h":
                        print(f"Player {self.participants[ID].ID}")
                    else:
                        print(f"Player {self.participants[ID].ID} " +
                              "Strategy: " +
                              f"{type(self.participants[ID]).__name__}")
                self.tournament_round += 1
        if (player_type == "h" and
                isinstance(self.participants[0], HumanPlayer) and
                len(self.participants) == 1):
            print(f"\nYou won the tournament, congratulations!\n")
        else:
            print(f"\nThe tournament winner is Player " +
                  f"{self.participants[0].ID} Strategy: " +
                  f"{type(self.participants[0]).__name__}, " +
                  "congratulations!\n")
        return type(self.participants[0]).__name__

    def create_players(self, num_participants, player_type):
        player_types = ['RockPlayer()', 'RandomPlayer()',
                        'ReflectPlayer()', 'CyclePlayer()']
        self.participants = []
        if player_type == "h":
            print("Welcome to the tournament, you are Player 0")
        else:
            print("The tournament players are:")
        # To test code with customer participants
        # uncomment {1} and {2} and comment {3} below:
        # test_participants = [CyclePlayer(), RockPlayer(),
        #                      ReflectPlayer(), ReflectPlayer(),
        #                      ReflectPlayer(), ReflectPlayer(),
        #                      ReflectPlayer(), RockPlayer()]  # {1}
        for x in range(num_participants):
            # self.participants.append(test_participants[x])  # {2}
            if player_type == "h" and x == 0:
                self.participants.append(HumanPlayer())
                self.participants[0].create_id(0)
                continue
            self.participants.append(eval(random.choice(player_types)))  # {3}
            self.participants[x].create_id(x)

            # Question: before writing the line above, I was trying the
            # function below but it didn´t work.
            # Could you tell me what is wrong?
            # self.participants[x].id = x

            # Question: I also tried creating a variable dynamically using
            # eval(f"self.participant{x} = self.participants[{x}].id")
            # but didn´t work, why?

            if player_type != "h":
                print(f"Player {self.participants[x].ID} " +
                      f"(Strategy = {type(self.participants[x]).__name__})")

    def play_round(self, participants):
        self.participats = participants

        # Skip strategy check for first round, as was already proved in
        # play_tournament()
        if self.tournament_round > 1:
            if self.conflicting_strategies(self.participants) is True:
                return "Conflicting strategies!"

        self.winners = []

        for ID in range(0, len(self.participants), 2):
            # Tournament class only tested for Rock, Paper, Scissors,
            # therefore Game has "rps" predefined
            game = Game(self.participants[ID],
                        self.participants[ID + 1], "rps")
            game.outcome = 0
            if self.print_results:
                while game.outcome == 0:
                    game.outcome = game.play_game(self.game_rounds)
            else:
                with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
                    while game.outcome == 0:
                        game.outcome = game.play_game(self.game_rounds)
            if game.outcome == 'quit':
                return 'quit'
            self.winners.append(self.participants[game.outcome - 1 + ID])
        self.participants.clear()
        self.participants = self.winners

    # Method to avoid infinite loops
    # Rock vs Cycle player in 3 rounds, always a tie
    def conflicting_strategies(self, participants):
        self.participants = participants
        rocks = reflects = randoms = cycles = humans = 0
        for participant in self.participants:
            rocks += isinstance(participant, RockPlayer)
            reflects += isinstance(participant, ReflectPlayer)
            randoms += isinstance(participant, RandomPlayer)
            cycles += isinstance(participant, CyclePlayer)
            humans += isinstance(participant, HumanPlayer)
        # Avoid infinite loop when more than half of the participants:
            # always throw 'Rock'
        if ((rocks > len(self.participants) / 2) or
            # always reflects in multiples of 2 rounds
            (reflects > len(self.participants) / 2 and
             self.game_rounds % 2 == 0) or
            # cycle vs rock in multiples of 3 rounds
            (rocks + cycles > len(self.participants) - rocks and
             self.game_rounds % 3 == 0)):
            return True
        if ((rocks <= 1) and
                (reflects <= 1 or self.game_rounds % 2 != 0) and
                (rocks + cycles <= 1 or self.game_rounds % 3 != 0)):
            return False
        else:
            ordered_players = []
            for x in range(0, len(self.participants), 2):
                if ((isinstance(self.participants[x], RockPlayer) and
                     isinstance(self.participants[x + 1], RockPlayer)) or
                    (isinstance(self.participants[x], ReflectPlayer) and
                     isinstance(self.participants[x + 1], ReflectPlayer) and
                     self.game_rounds % 2 == 0) or
                    (isinstance(self.participants[x], RockPlayer) and
                     isinstance(self.participants[x + 1], CyclePlayer) and
                     self.game_rounds % 3 == 0) or
                    (isinstance(self.participants[x], CyclePlayer) and
                     isinstance(self.participants[x + 1], RockPlayer) and
                     self.game_rounds % 3 == 0)):
                    ID = 0
                    while len(self.participants) > 0:
                        if rocks > 0:
                            if (ID == 0 or not
                                    isinstance(ordered_players[ID-1],
                                               RockPlayer)):
                                swap_ID = find_class(RockPlayer,
                                                     self.participants)
                                ordered_players.append(
                                    self.participants[swap_ID])
                                self.participants.remove(
                                    self.participants[swap_ID])
                                ID += 1
                                rocks -= 1
                                continue
                        if reflects > 0:
                            if (ID == 0 or not
                                (isinstance(ordered_players[ID-1],
                                            ReflectPlayer) and
                                    self.game_rounds % 2 == 0)):
                                swap_ID = find_class(ReflectPlayer,
                                                     self.participants)
                                ordered_players.append(
                                    self.participants[swap_ID])
                                self.participants.remove(
                                    self.participants[swap_ID])
                                ID += 1
                                reflects -= 1
                                continue
                        if randoms > 0:
                            swap_ID = find_class(RandomPlayer,
                                                 self.participants)
                            ordered_players.append(
                                self.participants[swap_ID])
                            self.participants.remove(
                                self.participants[swap_ID])
                            ID += 1
                            randoms -= 1
                            continue
                        if cycles > 0:
                            swap_ID = find_class(CyclePlayer,
                                                 self.participants)
                            ordered_players.append(
                                self.participants[swap_ID])
                            self.participants.remove(
                                self.participants[swap_ID])
                            ID += 1
                            cycles -= 1
                            continue
                        if humans > 0:
                            swap_ID = find_class(HumanPlayer,
                                                 self.participants)
                            ordered_players.append(
                                self.participants[swap_ID])
                            self.participants.remove(
                                self.participants[swap_ID])
                            ID += 1
                            humans -= 1
                            continue
                    self.participants = ordered_players
                    return False


def find_class(obj, list):
    for ID in range(len(list)):
        if isinstance(list[ID], obj):
            return ID
        else:
            ID += 1
    return False


# Question: Why can´t I have the beats function inside the Game class?
# I get the error that the name "beats" is not known
def beats(one, two):
    return ((one == 'rock' and (two == 'scissors' or two == 'lizard')) or
            (one == 'paper' and (two == 'rock' or two == 'spock')) or
            (one == 'scissors' and (two == 'paper' or two == 'lizard')) or
            (one == 'lizard' and (two == 'paper' or two == 'spock')) or
            (one == 'spock' and (two == 'scissors' or 'rock')))


if __name__ == '__main__':

    player_types = ['RockPlayer()', 'RandomPlayer()',
                    'ReflectPlayer()', 'CyclePlayer()']
    game_form = ""
    print("\nWelcome to the Rock, Scissors, Paper (Lizard, Spock) Game.")

    player_type = ""
    while player_type not in ["h", "c"]:
        player_type = input("\nChoose a player type:\n" +
                            "For Human vs Computer enter 'H',\n" +
                            "for Computer vs Computer enter 'C':\n").lower()

    while game_form not in ["t", "g"]:
        game_form = input("\nChoose tournamen or single game:\n" +
                          "For Tournament enter 'T' " +
                          "(only traditional Rock, Paper, Scissor " +
                          "supported),\n" +
                          "For Game enter 'G':\n").lower()
    if game_form == "t":
        players = 0
        while (players == 0 or players-1 == 0 or
                not (players & (players-1) == 0)):
            try:
                players = int(input("\nEnter the number of players " +
                                    "for the tournament.\n" +
                                    "It has to be powers of 2 " +
                                    "(2, 4, 8, 16 etc)\n"))
            except ValueError:
                print("\nOops!  That was no valid number.  Try again...\n")
        rounds = 0
        while rounds == 0:
            try:
                rounds = int(input("\nEnter the number of rounds per game " +
                                   "(>0) you want to play:\n"))
                break
            except ValueError:
                print("\nOops!  That was no valid number.  Try again...\n")
        print_results = ""
        while print_results not in ["y", "n"]:
            print_results = input("\nDo you want to print the results " +
                                  "of each game in the tournament?\n" +
                                  "Enter 'Y' for yes\n" +
                                  "Enter 'N' for no\n").lower()
        tournament = Tournament()
        if print_results == "y":
            print_results = True
        else:
            print_results = False
        tournament.play_tournament(
            players, player_type, rounds, print_results)
    else:
        game_type = ""
        while game_type not in ["rps", "rpsls"]:
            game_type = input("\nChoose game type:\n" +
                              "For Rock, Paper, Scissors enter 'RPS',\n" +
                              "For Rock, Paper, Scissors, Lizard, Spock " +
                              "enter 'RPSLS':\n").lower()
        difficulty = ""
        while difficulty not in ["0", "1", "2", "3"]:
            difficulty = input("\nChoose Computer difficulty:\n" +
                               "Enter '0' for very easy\n" +
                               "Enter '1' for easy\n" +
                               "Enter '2' for medium\n" +
                               "Enter '3' for hard\n")
        if difficulty == '0':  # Always a tie
            player1 = RockPlayer()
            player2 = RockPlayer()
        elif difficulty == '1':
            player1 = RandomPlayer()
            player2 = RandomPlayer()
        elif difficulty == '2':
            player1 = ReflectPlayer()  # Always alternate
            player2 = ReflectPlayer()
        else:
            player1 = CyclePlayer()
            player2 = CyclePlayer()

        if player_type == "h":
            game = Game(HumanPlayer(), player2, game_type)
        else:
            game = Game(player1, player2, game_type)

        game.play_game()

    # # Code to test different scenarios:
    # tournament = Tournament()
    # count = 0
    # winner = []
    # for z in range (1, 6):
    #     for y in range(1, 10):
    #         for x in range(10):
    #             print(x, y, z)
    #             count += 1
    #             with (open(os.devnull, "w")
    #                 as f, contextlib.redirect_stdout(f)):
    #             winner.append(tournament.play_tournament(
    #                 2**z, "c", y, False))
    #             #tournament.play_tournament(8, 9, "c", False)
    # print(count)
    # print(f"The most successful player is " +
    #       f"{max(winner,key=winner.count)}")
