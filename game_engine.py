import threading
import time

from game_control import UserInput, ComputerInput
from logging_and_error_handling import handle_errors, Log, YouAreWinner, YouAreLoser


class GameEngine():
    def __init__(self, game_id, points_to_win=3 ,time_of_round=5):
        self.log = Log(game_id)
        self.log.create_log_file_and_set_log_configuration()
        self.TIME_OF_ROUND = time_of_round
        self.POINTS_TO_WIN = points_to_win
        self.OPTIONS = {'1':'rock', '2':'paper', '3':'scissors'}
        self.User = UserInput('Player', 9)
        self.Computer = ComputerInput('Computer', 9)
        self.user_points = 0
        self.computer_points = 0

    def set_difficulty_level(self, *args):
        self.Computer.input_difficulty_level_and_convert(*args)
        self.log.info(f'difficulty level = {self.Computer.difficulty_level}\n\t\t\t    probability of counterattack = {self.Computer.probability_of_counterattack}\n\t\t\t    reaction time = {self.Computer.reaction_time}')


    @handle_errors
    def play(self):
        while True:
            self.round()
            self.log.info(f'you have handed over the choice in time: {self.timestamp_computer}')
            self.log.info(f'your choice = {self.OPTIONS[self.User.choice]}, computer choice = {self.OPTIONS[self.Computer.choice]}')
            if self.user_points == self.POINTS_TO_WIN:
                break
                raise YouAreWinner(self.Computer.difficulty_level, self.user_points, self.computer_points)
            elif self.computer_points == self.POINTS_TO_WIN:
                break
                raise YouAreLoser(self.Computer.difficulty_level, self.user_points, self.computer_points)
            self.log.info(f'your points: {self.user_points}, computer points: {self.computer_points}')


    def round(self):
        self.round_handling()
        self.pick_a_winner_for_round()
        if self.winner is not None:
            print('\n')
            self.log.info(f'a winner of round is {self.winner}')
            self.add_points()

    @handle_errors
    def round_handling(self):
        self.start_time = time.time()
        self.User.choice = None

        round_time = threading.Thread(target=self.round_time)
        player_choice = threading.Thread(target=self.User.choice_input_and_check)
        wait_for_player_choice = threading.Thread(target=self.wait_for_player_choice)
        computer_ai = threading.Thread(target=self.computer_artificial_intelligence)

        
        player_choice.start()
        time.sleep(0.04)
        round_time.start()
        time.sleep(0.3)
        computer_ai.start()
        wait_for_player_choice.start()

        player_choice.join()
        round_time.join()
        wait_for_player_choice.join()

    def wait_for_player_choice(self):
        while True:
            if self.User.choice is not None:
                if self.User.is_good_choice_input:
                    time_of_player_choice = time.time()
                    self.show_player_choice()
                    break
        self.timestamp_player = (time_of_player_choice - self.start_time)

    def show_player_choice(self):
        print(f'\n\rYour choice: {self.OPTIONS[self.User.choice]}\n')

    def computer_artificial_intelligence(self):
        while True:
            if self.elapsed_time >= (self.TIME_OF_ROUND - self.Computer.reaction_time):
                if self.User.choice is not None:
                    if self.User.is_good_choice_input:
                        self.Computer.choice_input_and_check(player_choice = self.User.choice)
                else:
                    self.Computer.choice_input_and_check()
                self.show_computer_choice()
                self.timestamp_computer = (time.time() - self.start_time)
                break

    def show_computer_choice(self):
        print(f'\n\rComputer choice: {self.OPTIONS[self.Computer.choice]}\n')


    def round_time(self):
        while True:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
            self.show_elapsed_time()
            if self.elapsed_time >= self.TIME_OF_ROUND:
                break

    def show_elapsed_time(self):
        print(f'\relapsed time: {self.elapsed_time}\t\t', end='', flush=True)


    def pick_a_winner_for_round(self):
        if self.user_choice_was_after_time():
            print('\n')
            self.log.warning(f'you handed over the choice after time ({self.timestamp_player}')
            self.winner = 'computer'
        elif self.User.choice == self.Computer.choice:
            self.winner = None
        elif self.User.choice == '1' and self.Computer.choice == '3' or \
            self.User.choice == '2' and self.Computer.choice == '1' or \
            self.User.choice == '3' and self.Computer.choice == '2':
                self.winner = 'user'
        else:
            self.winner = 'computer'
        

    def user_choice_was_after_time(self):
        return self.timestamp_player > self.TIME_OF_ROUND

    def add_points(self):
        if self.winner == 'user':
            self.user_points += 1
        elif self.winner == 'computer':
            self.computer_points += 1

if __name__ == '__main__':
    game = GameEngine(10, 2)
    game.set_difficulty_level('easy')
    game.play()


