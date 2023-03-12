import threading
import time

from game_control import UserInput

class GameEngine():
    def __init__(self, time_of_round):
        self.time_of_round = time_of_round
        self.user_input = UserInput('Player1', 9)

    def round(self):
        round_time = threading.Thread(target=self.round_time)
        player_choice = threading.Thread(target=self.user_input.choice_input_and_check)
        self.start_time = time.time()
        self.user_input.choice = None
        round_time.start()
        player_choice.start()
        while True:
            if self.user_input.choice is not None:
                if self.user_input.choice.isdigit() and int(self.user_input.choice) in range(1,4):
                    time_of_player_choice = time.time()
                    break
  
        self.timestamp_player = int((time_of_player_choice - self.start_time) * 1000)
        round_time.join()

    
    def round_time(self):
        while True:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            if elapsed_time >= self.time_of_round:
                break

if __name__ == '__main__':
    game = GameEngine(3)
    game.round()
    print(game.timestamp_player)
    print(game.user_input.choice)