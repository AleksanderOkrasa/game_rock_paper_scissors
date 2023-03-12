import inspect
import logging
import os
import sys
import traceback


def handle_errors(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except KeyboardInterrupt:
            self.log.error(f'a function was interrupted by a user (ctrl + c)')
            exit(2)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if isinstance(e, BadChoiceInput):
                self.log.warning(f'{exc_type.__name__}: {e}; try again')
                return self.choice_input_and_check()
            elif isinstance(e, BadDifficultyLevelInput):
                self.log.warning(f'{exc_type.__name__}: {e}; try again')
                return self.input_difficulty_level_and_convert()
            elif isinstance(e, BadParameterForCustomDifficultyLevelInput):
                self.log.warning(f'{exc_type.__name__}: {e}; try again')
                return self.convert_difficulty_level_to_and_reaction_time_and_probability_of_counterattack()

            
            else:
                traceback.format_exception(exc_type, exc_value, exc_traceback)
                # filename = exc_traceback.tb_frame.f_code.co_filename
                # indicates the exact location in the code where the error occurred 
                self.log.error(f"Exception in function {func.__name__}, {exc_type.__name__}: {exc_value}")
                exit(1)
    return wrapper

    
class BadChoiceInput(Exception):
    pass
class BadDifficultyLevelInput(Exception):
    pass
class BadParameterForCustomDifficultyLevelInput(Exception):
    pass

class Log():
    # class controlling the creation of logs
    def __init__(self, game_id):
        self.logs_directory = 'logs'
        self.path_to_log = f'{self.logs_directory}/game_id_{str(game_id)}.log'
        self.logger = logging.getLogger(str(game_id))

    def create_log_file_and_set_log_configuration(self):
        if self.logs_directory_not_exists():
            self.create_directory()
        self.create_log_file()
        self.set_log_configiguration()

    def create_directory(self):
        if not os.path.isdir(self.logs_directory):
            os.makedirs(self.logs_directory)

    def logs_directory_not_exists(self):
        if not os.path.isdir(self.logs_directory):
            return True

    def create_log_file(self):
        self.file_handler = logging.FileHandler(self.path_to_log)
 
    def set_log_configiguration(self):
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        formatter = logging.Formatter("%(asctime)s  :::  %(levelname)s \t::: %(message)s", datefmt='%H:%M:%S')

        self.file_handler.setFormatter(formatter)
        self.file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
 
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(console_handler)

    def error(self, message):
        return (self.logger.error(message))

    def info(self, message):
        return (self.logger.info(message))

    def warning(self, message):
        return (self.logger.warning(message))

    def debug(self, message):
        return (self.logger.debug(message))