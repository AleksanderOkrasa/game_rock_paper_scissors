import pytest

from game_control import UserInput
from msvcrt import getch

# $env:PYTHONPATH += ";C:\Users\windo\Documents\GitHub\game_rock_paper_scissors"


@pytest.fixture
def user_input():
    return UserInput('TestPlayer', 1)

def test_player_name(user_input):
    assert user_input.player == 'TestPlayer'

def test_check_choice_input_good_scenario(user_input):
    user_input.choice = '1'
    assert user_input.is_good_choice_input()
    user_input.choice = '2'
    assert user_input.is_good_choice_input()
    user_input.choice = '3'
    assert user_input.is_good_choice_input()

def test_check_choice_input_bad_scenario(user_input):
    user_input.choice = 'd'
    assert not user_input.is_good_choice_input()
    user_input.choice = '-1'
    assert not user_input.is_good_choice_input()
    user_input.choice = '4'
    assert not user_input.is_good_choice_input()

def test_bad_choice_input(user_input, mocker):
    user_input.choice = '0'
    mock_foo = mocker.patch('game_control.UserInput.choice_input_and_check')
    user_input.check_choice_input()
    mock_foo.assert_called_once()

