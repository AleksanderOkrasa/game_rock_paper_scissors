from abc import ABC, abstractclassmethod
from msvcrt import getch

import random

from logging_and_error_handling import Log, handle_errors, BadChoiceInput, BadInputDifficultyLevel
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
    def choice_input(self):
        pass

    @handle_errors
    def check_choice_input(self):
        if not self.is_good_choice_input():
            raise(BadChoiceInput(f'enter value: {self.choice}'))

    def is_good_choice_input(self):
        return self.choice.isdigit() and int(self.choice) in range(1,4)
    
class UserInput(GameInput):
    def choice_input(self):
        print('Type a choice [1 -> rock] [2 -> paper] [3 -> scissors]')
        self.choice = getch().decode('utf-8')
        self.log.info(f'{self.player} enter {self.choice}')

class ComputerInput(GameInput):

    @handle_errors
    def input_difficulty_level_and_convert(self, difficulty_level = None):
        if difficulty_level is None:
            self.difficulty_level = input('enter a difficulty level [easy, medium, hard, custom]: ')
        else:
            self.difficulty_level=difficulty_level 
        self.convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack()

    @handle_errors
    def convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack(self):
        if self.difficulty_level == 'hard':
            self.probability_of_counterattack = 0.90
            self.reaction_time = 0.3
        elif self.difficulty_level == 'medium':
            self.probability_of_counterattack = 0.60
            self.reaction_time = 0.6
        elif self.difficulty_level == 'easy':
            self.probability_of_counterattack = 0.30
            self.reaction_time = 1.0
        elif self.difficulty_level == 'custom':
            self.probability_of_counterattack = input('Enter a probability of counterattack [0.33 - 1.00]: ')
            self.reaction_time = input('Enter a reaction of time [in seconds, example: 0.5]')
        else:
            raise BadInputDifficultyLevel({self.difficulty_level})
        self.log.info(f'difficulty level = {self.difficulty_level}\n\t\t\t    probability of counterattack = {self.probability_of_counterattack}\n\t\t\t    reaction time = {self.reaction_time}')
    

    def choice_input(self):
        self.choice = self.generate_random_number()

    def generate_random_number(self, player_choice = None):
        if player_choice:
            if random.random() < self.probability_of_counterattack:
                return player_choice
            else:
                return random.randint(1, 3)
        else:
            return random.randint(1,3)

# user = UserInput('Player', game_id=1)
# choice = user.choice_input_and_check()

computer = ComputerInput('Computer', game_id=1)
computer.input_difficulty_level_and_convert('medium')
print(computer.generate_random_number(player_choice=3))
print(computer.generate_random_number())

