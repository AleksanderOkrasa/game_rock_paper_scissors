from abc import ABC, abstractclassmethod
from msvcrt import getch

import random

from logging_and_error_handling import Log, handle_errors, BadChoiceInput, BadDifficultyLevelInput, BadParameterForCustomDifficultyLevelInput
class GameInput(ABC):
    def __init__(self, player, game_id):
        self.player = player
        self.log = Log(game_id)
        self.log.create_log_file_and_set_log_configuration()

    def __str__(self):
        return self.player
    
    def choice_input_and_check(self, **kwargs):
        self.choice_input(**kwargs)
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
    def choice_input(self, **kwargs):
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
            self.reaction_time = 0.5
        elif self.difficulty_level == 'medium':
            self.probability_of_counterattack = 0.60
            self.reaction_time = 1.0
        elif self.difficulty_level == 'easy':
            self.probability_of_counterattack = 0.30
            self.reaction_time = 2
        elif self.difficulty_level == 'custom':
            self.input_parameters_for_custom_difficulty_level()
        else:
            raise BadDifficultyLevelInput(self.difficulty_level)
        self.log.info(f'difficulty level = {self.difficulty_level}\n\t\t\t    probability of counterattack = {self.probability_of_counterattack}\n\t\t\t    reaction time = {self.reaction_time}')

    def input_parameters_for_custom_difficulty_level(self):
            input_probability = input('Enter a probability of counterattack [1 - 100]: ')
            probability_of_counterattack = self.check_custom_difficulty_level_parameters(input_probability)
            self.probability_of_counterattack = float(probability_of_counterattack * 0.01)

            input_reaction_time = input('Enter a reaction of time [in miliseconds, example: 5 -> 0.5 sec, max 100]')
            reaction_time = self.check_custom_difficulty_level_parameters(input_reaction_time)
            self.reaction_time = float(reaction_time * 0.1)

    @handle_errors
    def check_custom_difficulty_level_parameters(self, parameter):
        if parameter.isdigit() and int(parameter) in range(1, 100):
            return int(parameter)
        else:
            raise BadParameterForCustomDifficultyLevelInput(parameter)
        
    
    def choice_input(self, **kwargs):
        self.choice = str(self.generate_random_number(**kwargs))

    def generate_random_number(self, player_choice = None):
        if player_choice:
            if random.random() < self.probability_of_counterattack:
                return player_choice
            else:
                return  random.randint(1, 3)
        else:
            return random.randint(1,3)


if __name__ == '__main__':
    user = UserInput('Player', game_id=1)
    user.choice_input_and_check()
    computer = ComputerInput('Computer', 1)
    computer.input_difficulty_level_and_convert('custom')
    computer.choice_input_and_check(player_choice=3)
    # print(computer.generate_random_number())
