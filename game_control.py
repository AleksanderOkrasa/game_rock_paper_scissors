from abc import ABC, abstractclassmethod

from msvcrt import getch

class GameInput(ABC):
    def __init__(self, player):
        self.player = player

    def __str__(self):
        return self.player
    
    @abstractclassmethod
    def choice_input(self, choice = None):
        pass

    def check_choice_input(self, choice):
        if not self.is_good_choice_input():
            print(f'Bad input [ {choice} ]; try again')
            raise(BadChoiceInput(f'enter value: {choice}'))

    def is_good_choice_input(self):
        return choice.isdigit() and int(choice) in range(1,4)
    
class UserInput(GameInput):
    def choice_input(self, choice = None):
        print('Type a choice [1 - rock, 2 - paper, 3 - scissors]')
        choice = getch().decode('utf-8')
        return choice
    
class BadChoiceInput(Exception):
    pass
user = UserInput('Player')
choice = user.choice_input()
print(user.check_choice_input(choice))
