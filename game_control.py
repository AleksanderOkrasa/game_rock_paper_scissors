from abc import ABC, abstractclassmethod

class GameInput(ABC):
    def __init__(self, player):
        self.player = player

    def __str__(self):
        return self.player
    
    @abstractclassmethod
    def input(self, choice = None):
        pass

