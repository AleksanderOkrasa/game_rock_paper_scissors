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
        round_time = threading.Thread(target=self.round_time)
        player_choice = threading.Thread(target=self.user.choice_input_and_check)
        computer_ai = threading.Thread(target=self.computer_artificial_intelligence)
        self.start_time = time.time()
        self.user.choice = None
        round_time.start()
        player_choice.start()
        computer_ai.start()
        while True:
            if self.user.choice is not None:
                if self.user.choice.isdigit() and int(self.user.choice) in range(1,4):
                    time_of_player_choice = time.time()
                    break
  
        self.timestamp_player = (time_of_player_choice - self.start_time)
        round_time.join()

    def computer_artificial_intelligence(self):
        while True:
            if self.elapsed_time >= (self.time_of_round - self.computer.reaction_time):
                if self.user.choice is not None:
                    if self.user.choice.isdigit() and int(self.user.choice) in range(1,4):
                        self.computer.choice_input_and_check(player_choice = self.user.choice)
                else:
                    self.computer.choice_input_and_check()
                break

    def round_time(self):
        while True:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
            # print(self.elapsed_time)
            if self.elapsed_time >= self.time_of_round:
                break
            

if __name__ == '__main__':
    game = GameEngine(4)
    game.set_difficulty_level('easy')
    game.round()
    # print(game.timestamp_player)
