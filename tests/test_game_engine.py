import pytest
from game_engine import GameEngine, YouAreWinner, YouAreLoser

# $env:PYTHONPATH += ";C:\Users\windo\Documents\GitHub\game_rock_paper_scissors"


@pytest.fixture
def engine():
    return GameEngine(11, 3, 5)


def test_pick_winner_for_round(engine):
    engine.User.choice = '1'
    engine.Computer.choice = '3'
    engine.timestamp_player = 6
    engine.pick_a_winner_for_round()
    assert engine.winner == 'computer'

    engine.timestamp_player = 4
    engine.pick_a_winner_for_round()
    assert engine.winner == 'user'

    engine.Computer.choice = '1'
    engine.pick_a_winner_for_round()
    assert engine.winner == None

    engine.Computer.choice = '2'
    engine.pick_a_winner_for_round()
    assert engine.winner == 'computer'    

    engine.User.choice = '2'
    engine.pick_a_winner_for_round()
    assert engine.winner == None  

    engine.User.choice = '3'
    engine.pick_a_winner_for_round()
    assert engine.winner == 'user'


def test_add_points(engine):
    engine.winner = 'user'
    engine.add_points()
    assert engine.user_points == 1
    assert engine.computer_points == 0
    engine.add_points()
    assert engine.user_points == 2
    assert engine.computer_points == 0
    engine.winner = 'computer'
    engine.add_points()
    assert engine.user_points == 2
    assert engine.computer_points == 1
    engine.add_points()
    engine.add_points()
    assert engine.user_points == 2
    assert engine.computer_points == 3
    engine.winner = None
    engine.add_points()
    assert engine.user_points == 2
    assert engine.computer_points == 3


def test_pick_winner_for_game(engine):
    engine.Computer.difficulty_level = 'easy'
    engine.user_points = 3

    with pytest.raises(YouAreWinner):
        engine.check_for_the_end_of_the_game()

    engine.POINTS_TO_WIN = 4
    engine.computer_points = 4

    with pytest.raises(YouAreLoser):
        engine.check_for_the_end_of_the_game()

def check_start_points(engine):
    assert engine.user_points == 0
    assert engine.computer_points == 0
