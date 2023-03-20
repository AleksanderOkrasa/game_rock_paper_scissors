import tkinter as tk
import threading
import time


from game_control import ComputerInput, UserInput
from game_engine import GameEngine
from logging_and_error_handling import Log, handle_errors

import time

class GameGUI(GameEngine):
    def __init__(self, master):
        
        self.master = master
        self.master.title("Rock Paper Scissors")
        self.master.geometry("500x300")
        self.font = 20


        self.start_button = tk.Button(self.master, text="Start", font = self.font, command=self.start_game)
        self.start_button.pack(padx=70)
        self.timer = tk.Label(self.master, font = self.font, text="")
        self.timer.pack(pady=25)
        self.is_running = False
  
        self.elapsed_time = 1
        self.TIME_OF_ROUND = 5

        self.game_engine(1, 1)
        self.set_difficulty_level('easy')

    def game_engine(self, game_id, points_to_win=3 ,time_of_round=5):
        self.log = Log(game_id)
        self.log.create_log_file_and_set_log_configuration()
        self.TIME_OF_ROUND = time_of_round
        self.POINTS_TO_WIN = points_to_win
        self.OPTIONS = {'1':'rock', '2':'paper', '3':'scissors'}
        self.User = UserInput('Player', 9)
        self.Computer = ComputerInput('Computer', 9)
        self.user_points = 0
        self.computer_points = 0
        
    def show_player_choice(self):
        self.user_choice_area.config(text=str(self.OPTIONS[self.User.choice]))
        self.master.update()

    def show_computer_choice(self):
        self.computer_choice_area.config(text=str(self.OPTIONS[self.Computer.choice]))
        self.master.update()

    @handle_errors
    def start_game(self):
        self.is_running = True
        self.start_button.config(state="disabled")
        self.create_choices_buttons()
        self.show_choices_buttons()
        self.show_elapsed_time()
        self.play()
        self.is_running = False
        self.start_button.config(state="normal")

    def create_choices_buttons(self):
        self.you_string = tk.Label(self.master, font = self.font, text="you")
        self.computer_string = tk.Label(self.master, font = self.font, text="computer")
        self.user_choice_area = tk.Label(self.master, font = self.font, text="")
        self.computer_choice_area = tk.Label(self.master, font = self.font, text = "")
        self.rock_button = tk.Button(self.master, text="Rock", font = self.font, command=self.choice_rock)
        self.paper_button = tk.Button(self.master, text="Paper", font = self.font, command=self.choice_paper)
        self.scissors_button = tk.Button(self.master, text="Scissors", font = self.font, command=self.choice_scissors)
        
    def choice_rock(self):
        self.User.choice = '1'
        self.disable_choices_buttons()
        
    def choice_paper(self):
        self.User.choice = '2'
        self.disable_choices_buttons()

    def choice_scissors(self):
        self.User.choice = '3'
        self.disable_choices_buttons()

    def show_choices_buttons(self):
        padding = 10
        self.you_string.place(relx=0.2, y= 120, width = 100)
        self.user_choice_area.place(relx=0.2, y= 150, width = 100)

        self.computer_string.place(relx=0.6, y = 120, width = 100)
        self.computer_choice_area.place(relx=0.6, y= 150, width = 100)

        self.rock_button.place(relx=0.1, width = 100, rely = 0.7)
        self.paper_button.place(relx=0.4, width = 100, rely = 0.7)
        self.scissors_button.place(relx=0.7, width = 100, rely = 0.7)
        
        
    def disable_choices_buttons(self):
        self.rock_button.config(state='disabled')
        self.paper_button.config(state='disabled')
        self.scissors_button.config(state='disabled')



    # def show_elapsed_time(self):
    #     self.label.config(text=int(self.elapsed_time))
    #     self.master.update()
    #     self.elapsed_time += 1
    @handle_errors
    def round_handling(self):
        self.enable_choices_buttons()
        self.start_time = time.time()
        self.User.choice = None
        self.elapsed_time=0
        # player_choice = threading.Thread(target=self.User.choice_input_and_check)
        wait_for_player_choice = threading.Thread(target=self.wait_for_player_choice)
        computer_ai = threading.Thread(target=self.computer_artificial_intelligence)

        
        # player_choice.start()
        computer_ai.start()
        wait_for_player_choice.start()

        self.round_time()


        # player_choice.join()
        wait_for_player_choice.join()

    def enable_choices_buttons(self):
        self.rock_button.config(state='normal')
        self.paper_button.config(state='normal')
        self.scissors_button.config(state='normal')


    def round_time(self):
        while True:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
            self.show_elapsed_time()
            self.timer.config(text=float(self.elapsed_time))
            self.master.update()
            if self.elapsed_time >= self.TIME_OF_ROUND:
                break


if __name__ == '__main__':
    root = tk.Tk()  
    my_gui = GameGUI(root)
    root.mainloop()
