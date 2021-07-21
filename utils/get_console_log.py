import logging
from ui.base_page import BasePage


class GetConsoleLog(object):

    def __init__(self, context):
        self.logger = logging.getLogger('send_result')
        self.driver = BasePage(context).get_driver()

    def get_console_log(self):
        return self.driver.get_log('browser')

    def output_all_console_log(self):
        console_log = self.get_console_log()
        for log in console_log:
            self.logger.info(f'Level of console log is: {log["level"]}, log message is: {log["message"]}')

    def output_all_warning_log(self):
        console_log = self.get_console_log()
        for log in console_log:
            if log["level"].lower() == 'warning':
                self.logger.info(f'Level of console log is: {log["level"]}, log message is: {log["message"]}')

    def output_all_error_log(self):
        console_log = self.get_console_log()
        for log in console_log:
            if log["level"].lower() == 'error':
                self.logger.info(f'Level of console log is: {log["level"]}, log message is: {log["message"]}')
