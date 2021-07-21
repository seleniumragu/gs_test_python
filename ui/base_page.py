# -*- coding: utf-8 -*-
import time

from ui.page_operation import PageOperation


class BasePage(object):
    def __init__(self, context):
        self.context = context
        self.page_operation = PageOperation(context)

    def load(self):
        """
        To load the page
        """
        pass

    def open_url(self):
        """
        To open the url
        """
        self.page_operation.goto_url()

    def get_driver(self):
        """
        to get the driver
        :return: browser
        """
        return self.context.browser

    @staticmethod
    def hard_sleep(seconds):
        """
        Do the smart wait for a particular seconds
        :param seconds: Seconds to wait
        """
        time.sleep(seconds)

