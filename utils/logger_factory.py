import logging
import os
import platform
import string

from behave.runner import Context

from utils.config_manager import ConfigManager


class Logger:

    def __init__(self, logger: logging):
        self.logger = logger

    def info(self, formatStr: string, *objs):
        self.logger.info(formatStr.format(*objs))

    def debug(self, formatStr: string, *objs):
        self.logger.debug(formatStr.format(*objs))

    def error(self, formatStr: string, *objs):
        self.logger.error(formatStr.format(*objs))

class LoggerFactory:
    """
    LoggerFactory is to save Logger instance for each class
    """
    LEVEL = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'ERROR': logging.ERROR
    }

    loggerDict = {}

    @staticmethod
    def getLogger(className) -> Logger:
        if className in LoggerFactory.loggerDict.keys():
            logger = LoggerFactory.loggerDict[className]
            if not logger:
                logger = LoggerFactory.__initLogger(className)
        else:
            logger = LoggerFactory.__initLogger(className)
        return logger

    @staticmethod
    def get_log_positon(context):
        workspace = context.test_config['project']
        pwd = os.getcwd()
        if 'Windows' in platform.system():
            pwd = os.getenv('path')
        else:
            pwd = os.getenv('path')
        print(pwd)
        return pwd

    # create an instance of logger
    @staticmethod
    def __initLogger(className) -> Logger:
        logger = logging.getLogger(className)
        context = Context
        ConfigManager().add_config_context(context)
        log_config_dict = context.test_config['log']
        # config level of logger: DEBUG/INFO
        logging_level = log_config_dict['level']
        logger.setLevel(LoggerFactory.LEVEL[logging_level])
        # config formatter of logger
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')
        type = log_config_dict['type'].split(',')

        if 'CONSOLE' in type:
            # create logging SteamHandler for console
            handler = logging.StreamHandler()
            # add handler to logger
            logger.addHandler(handler)
            # add formatter
            handler.setFormatter(formatter)
        #     TODO this part should be further tested in seperated automation project
        #           1. How to get path more easily
        #             2. How to be indepandent of context or path of environ
        # if 'FILE' in type:
        #     project_folder = LoggerFactory.get_log_positon(context)
        #     file = f'{project_folder}/logs/{log_config_dict["file"]}'
        #     # create logging FileHandler
        #     handler = logging.FileHandler(file)
        #     # add handler to logger
        #     logger.addHandler(handler)
        #     # add formatter
        #     handler.setFormatter(formatter)

        localLogger = Logger(logger)
        LoggerFactory.loggerDict[className] = localLogger
        return localLogger
