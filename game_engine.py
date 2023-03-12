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
        round_time.start()
        player_choice.start()
        round_time.join()
        player_choice.join()
        print(round_time)
        self.timestamp = round_time
        while True:
            if player_choice is not None:
                time_of_player_choice = time.time()
                break
        print(player_choice)
        self.timestamp_player = int((self.start_time - time_of_player_choice) * 1000)

    
    def round_time(self):
        while True:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            if elapsed_time >= self.time_of_round:
                break
            timestamp = int((current_time - self.start_time) * 1000)
        return timestamp

if __name__ == '__main__':
    game = GameEngine(3)
    game.round()
    print(game.timestamp)
    print(game.timestamp_player)