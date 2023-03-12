from abc import ABC, abstractclassmethod

from msvcrt import getch

from logging_and_error_handling import Log, handle_errors, BadChoiceInput
class GameInput(ABC):
    def __init__(self, player, game_id):
        self.player = player
        self.log = Log(game_id)
        self.log.create_log_file_and_set_log_configuration()

    def __str__(self):
        return self.player
    
    def choice_input_and_check(self):
        self.choice_input()
        self.check_choice_input()

    @abstractclassmethod
    def choice_input(self, choice = None):
        pass

    @handle_errors
    def check_choice_input(self):
        if not self.is_good_choice_input():
            raise(BadChoiceInput(f'enter value: {self.choice}'))

    def is_good_choice_input(self):
        return self.choice.isdigit() and int(self.choice) in range(1,4)
    
class UserInput(GameInput):
    def choice_input(self, choice = None):
        print('Type a choice [1 -> rock] [2 -> paper] [3 -> scissors]')
        self.choice = getch().decode('utf-8')
        self.log.info(f'{self.player} enter {self.choice}')

user = UserInput('Player', game_id=1)
choice = user.choice_input_and_check()
