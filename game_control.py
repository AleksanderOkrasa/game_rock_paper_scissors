from abc import ABC, abstractclassmethod

from msvcrt import getch

from logging_and_error_handling import Log

class GameInput(ABC):
    def __init__(self, player, game_id):
        self.player = player
        self.log = Log(game_id)
        self.log.create_log_file_and_set_log_configuration()

    def __str__(self):
        return self.player
    
    @abstractclassmethod
    def choice_input(self, choice = None):
        pass

    def check_choice_input(self, choice):
        if not self.is_good_choice_input():
            raise(BadChoiceInput(f'enter value: {choice}'))

    def is_good_choice_input(self):
        return choice.isdigit() and int(choice) in range(1,4)
    
class UserInput(GameInput):
    def choice_input(self, choice = None):
        print('Type a choice [1 - rock, 2 - paper, 3 - scissors]')
        choice = getch().decode('utf-8')
        self.log.info(f'{self.player} enter {choice}')
        return choice
    
class BadChoiceInput(Exception):
    pass
user = UserInput('Player', game_id=1)
choice = user.choice_input()
print(user.check_choice_input(choice))
