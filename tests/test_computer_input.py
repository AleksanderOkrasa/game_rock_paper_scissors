import pytest
from game_control import ComputerInput, BadParameterForCustomDifficultyLevelInput, BadChoiceInput

# $env:PYTHONPATH += ";C:\Users\windo\Documents\GitHub\game_rock_paper_scissors"


@pytest.fixture
def computer_input():
    return ComputerInput('TestComputer', 0)

def test_convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack_with_bad_difficulty_level(computer_input, mocker):
    # raise BadDifficultyLevelInput error calls the function input_difficulty_level_and_convert
    computer_input.difficulty_level = 'invalid'
    mock_foo = mocker.patch('game_control.ComputerInput.input_difficulty_level_and_convert')
    computer_input.convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack()
    mock_foo.assert_called_once_with()

def test_convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack_with_bad_convert_difficulty_level(computer_input):
    computer_input.difficulty_level = 'hard'
    computer_input.convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack()
    assert computer_input.probability_of_counterattack == 0.90
    assert computer_input.reaction_time == 0.5
    
    computer_input.difficulty_level = 'medium'
    computer_input.convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack()
    assert computer_input.probability_of_counterattack == 0.60
    assert computer_input.reaction_time == 1

    computer_input.difficulty_level = 'easy'
    computer_input.convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack()
    assert computer_input.probability_of_counterattack == 0.30
    assert computer_input.reaction_time == 2

@pytest.mark.parametrize("input_values, output",[(["custom", "20", "30"],["custom", 0.2, 3]),])
def test_input_difficulty_level_and_convert_with_custom_values_good_scenario(computer_input, monkeypatch, input_values, output):
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))    
    computer_input.input_difficulty_level_and_convert()
    assert computer_input.difficulty_level == output[0]
    assert computer_input.probability_of_counterattack == output[1]
    assert computer_input.reaction_time == output[2]

@pytest.mark.parametrize("probability_outsite_the_range, reaction_outsite_the_range, probability_bad_type, reaction_bad_type",[(["200", "30"], ["20", "-20"], ["string", "20"], ['20', 'string'])])
def test_input_difficulty_level_and_convert_with_custom_values_bad_scenario(computer_input, mocker, monkeypatch, probability_outsite_the_range, reaction_outsite_the_range, probability_bad_type, reaction_bad_type):
    computer_input.difficulty_level = 'custom'
    
    monkeypatch.setattr('builtins.input', lambda _: probability_outsite_the_range.pop(0))
    mock_foo = mocker.patch('game_control.ComputerInput.convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack')
    computer_input.input_parameters_for_custom_difficulty_level()
    mock_foo.assert_called_once()    

    monkeypatch.setattr('builtins.input', lambda _: reaction_outsite_the_range.pop(0))
    mock_foo = mocker.patch('game_control.ComputerInput.convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack')
    computer_input.input_parameters_for_custom_difficulty_level()
    mock_foo.assert_called_once()    

    monkeypatch.setattr('builtins.input', lambda _: probability_bad_type.pop(0))
    mock_foo = mocker.patch('game_control.ComputerInput.convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack')
    computer_input.input_parameters_for_custom_difficulty_level()
    mock_foo.assert_called_once()    

    monkeypatch.setattr('builtins.input', lambda _: reaction_bad_type.pop(0))
    mock_foo = mocker.patch('game_control.ComputerInput.convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack')
    computer_input.input_parameters_for_custom_difficulty_level()
    mock_foo.assert_called_once()    

def test_generate_random_number_without_parametr(computer_input):
    computer_input.choice_input_and_check()
    assert int(computer_input.choice) in range(1,4)
    
def test_generate_random_number_with_player_choice(computer_input):
    computer_input.probability_of_counterattack = 1
    for number in range(1,4):
        computer_input.choice_input(player_choice = number)
        assert int(computer_input.choice) == number

def test_bad_choice_input(computer_input, mocker):
    computer_input.choice = '4'
    mock_foo = mocker.patch('game_control.ComputerInput.choice_input_and_check')
    computer_input.check_choice_input()
    mock_foo.assert_called_once()
    
    computer_input.choice = 'D'
    mock_foo = mocker.patch('game_control.ComputerInput.choice_input_and_check')
    computer_input.check_choice_input()
    mock_foo.assert_called_once()

    computer_input.choice = '-1'
    mock_foo = mocker.patch('game_control.ComputerInput.choice_input_and_check')
    computer_input.check_choice_input()
    mock_foo.assert_called_once()

