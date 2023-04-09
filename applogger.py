import logging

class SpawnLogger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(level)

        self.file_handler = logging.FileHandler(f'{name}.log')
        self.file_handler.setLevel(level)

        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.console_handler.setFormatter(self.formatter)
        self.file_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)

        self.logger.info(f'Logger {name} created, with level {level}')

    def get_logger(self):
        return self.logger
    
#create an instance of the class
# logger = SpawnLogger('example_95823', logging.INFO).get_logger()