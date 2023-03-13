import threading
import time

from game_control import UserInput, ComputerInput
from logging_and_error_handling import handle_errors, Log


class GameEngine():
    def __init__(self, time_of_round):
        self.time_of_round = time_of_round
        self.options = {'1':'rock', '2':'paper', '3':'scissors'}
        self.user = UserInput('Player', 9)
        self.computer = ComputerInput('Computer', 9)

    @handle_errors
    def set_difficulty_level(self, *args):
        self.computer.input_difficulty_level_and_convert(*args)

    def pick_a_winner(self):
        if self.user_choice_was_after_time():
            self.winner = 'computer'
        elif self.user.choice == self.computer.choice:
            self.winner = None
        elif self.user.choice == '1' and self.computer.choice == '3' or \
            self.user.choice == '2' and self.computer.choice == '1' or \
            self.user.choice == '3' and self.computer.choice == '2':
                self.winner = 'user'
        else:
            self.winner = 'computer'

    def user_choice_was_after_time(self):
        return self.timestamp_player > self.time_of_round

    @handle_errors
    def round(self):
        self.start_time = time.time()
        self.user.choice = None

        round_time = threading.Thread(target=self.round_time)
        player_choice = threading.Thread(target=self.user.choice_input_and_check)
        wait_for_player_choice = threading.Thread(target=self.wait_for_player_choice)
        computer_ai = threading.Thread(target=self.computer_artificial_intelligence)

        
        player_choice.start()
        round_time.start()
        computer_ai.start()
        wait_for_player_choice.start()

        player_choice.join()
        round_time.join()

    def wait_for_player_choice(self):
        while True:
            if self.user.choice is not None:
                if self.user.is_good_choice_input:
                    time_of_player_choice = time.time()
                    break
        self.timestamp_player = (time_of_player_choice - self.start_time)

    def computer_artificial_intelligence(self):
        while True:
            if self.elapsed_time >= (self.time_of_round - self.computer.reaction_time):
                if self.user.choice is not None:
                    if self.user.is_good_choice_input:
                        self.computer.choice_input_and_check(player_choice = self.user.choice)
                else:
                    self.computer.choice_input_and_check()
                print(f'\n\rComputer choice: {self.options[self.computer.choice]}\n')
                self.timestamp_computer = (time.time() - self.start_time)
                break

    def round_time(self):
        while True:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
            print(f'\relapsed time: {self.elapsed_time}\t\t', end='', flush=True)
            if self.elapsed_time >= self.time_of_round:
                break
            


if __name__ == '__main__':
    game = GameEngine(4)
    game.set_difficulty_level('easy')
    game.round()
    print('\n')
    print(game.timestamp_player)
    print(game.timestamp_computer)
    game.pick_a_winner()
    print(game.winner)
    # print(game.timestamp_player)
