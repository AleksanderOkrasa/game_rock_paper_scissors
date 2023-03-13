from game_engine import GameEngine



if __name__ == "__main__":

    points_to_win = input('enter a needed points to win (press enter for default 3 wins): ')
    time_of_round = input('enter a time of round (press enter for default 5 seconds): ')

    if points_to_win == "":
        points_to_win = 3
    if time_of_round == "":
        time_of_round = 5

    game = GameEngine(10, points_to_win, time_of_round)

    game.set_difficulty_level()

    game.play()