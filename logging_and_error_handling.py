import logging
import os


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