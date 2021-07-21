# -*- coding: utf-8 -*-
import time
from ui.mobile import get_current_mobile_driver
from ui.page_operation_mobile import PageOperationMobile


class BasePageMobile(object):

    def __init__(self, context):
        self.driver = get_current_mobile_driver()
        self.context = context
        self.page_operation_mobile = PageOperationMobile(context)

    def get_mobile_driver(self):
        """
        to get the driver
        :return: mobile driver
        """
        return self.driver

    def get_driver_context(self):
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

