from logger.logger import Logger


class PrintLogger(Logger):

    def log(self, line: str) -> None:
        print(line)
