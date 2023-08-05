import logging


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SVTLogger:
    _logger_instance = None

    @staticmethod
    def get_instance():
        pass

    def __init__(self, test_name):
        self.logger = logging.getLogger("svtLogger-{}".format(test_name))
        self.logger.setLevel(logging.DEBUG)

        # fh = logging.FileHandler('svt_{}_execution.log'.format(test_name))
        # fh_formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s - %(levelname)s - %(message)s')
        # fh.setFormatter(fh_formatter)
        # self.logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh_formatter = logging.Formatter('%(funcName)s - %(levelname)s - %(message)s')
        sh.setFormatter(sh_formatter)
        self.logger.addHandler(sh)

    def get_logger(self):
        return self.logger
