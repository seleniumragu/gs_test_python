# -*- coding: utf-8 -*-
import random
from datetime import datetime


class DataUtils(object):
    @staticmethod
    def get_random_int(lower_bound, upper_bound, except_list=None):
        """
        Get random int number
        :param lower_bound: lower bound of random int
        :param upper_bound: upper bound of random int
        :param except_list: except result list
        :return: random int number
        """
        start_time = datetime.now()
        end_time = datetime.now()
        time_available = (end_time - start_time).seconds <= 2
        while time_available is True:
            result = random.randint(lower_bound, upper_bound)
            if result not in except_list:
                return result
        return None


