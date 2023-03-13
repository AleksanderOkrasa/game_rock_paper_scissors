import threading
import time

from game_control import UserInput, ComputerInput

class GameEngine():
    def __init__(self, time_of_round):
        self.time_of_round = time_of_round
        self.user = UserInput('Player', 9)
        self.computer = ComputerInput('Computer', 9)

    def set_difficulty_level(self, *args):
        self.computer.input_difficulty_level_and_convert(*args)

    def round(self):

        self.start_time = time.time()
        self.user.choice = None

        round_time = threading.Thread(target=self.round_time)
        player_choice = threading.Thread(target=self.user.choice_input_and_check)
        wait_for_player_choice = threading.Thread(target=self.wait_for_player_choice)
        computer_ai = threading.Thread(target=self.computer_artificial_intelligence)

        round_time.start()
        player_choice.start()
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
                self.timestamp_computer = (time.time() - self.start_time)
                break

    def round_time(self):
        while True:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
            if self.elapsed_time >= self.time_of_round:
                break
            

if __name__ == '__main__':
    game = GameEngine(4)
    game.set_difficulty_level('hard')
    game.round()
    print(game.timestamp_player)
    print(game.timestamp_computer)
    # print(game.timestamp_player)
