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

class UserInput(GameInput):
    def choice_input(self, choice = None):
        print('Type a choice [1 - rock, 2 - paper, 3 - scissors]')
        choice = getch().decode('utf-8')
        return choice
    
user = UserInput('Player')
print(user.choice_input())
