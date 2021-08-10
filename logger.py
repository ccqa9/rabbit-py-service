import logging

class Logging(object):
    level=logging.INFO

    def __init__(self):
        LOG_FORMAT = ('%(levelname) -5s %(asctime)s %(name) -10s %(funcName) '
                    '-15s %(lineno) -5d: %(message)s')
        logging.basicConfig(level=self.level, format=LOG_FORMAT)
        self._logger = logging.getLogger()

    def logger(self):
        return self._logger           