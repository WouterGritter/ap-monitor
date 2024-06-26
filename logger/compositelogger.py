from logger.logger import Logger


class CompositeLogger(Logger):

    def __init__(self, loggers: list[Logger]):
        self.loggers = loggers

    def log(self, line: str) -> None:
        for logger in self.loggers:
            logger.log(line)

    def add_logger(self, logger: Logger):
        self.loggers.append(logger)
