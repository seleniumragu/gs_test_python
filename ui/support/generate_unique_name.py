import random
import string
from datetime import date


class GenerateUniqueName(object):
    prefix = ''
    suffix = ''

    def __init__(self):
        self.suffix = '_' + date.today().strftime('%Y%m%d')+'_'+self._get_random()
        self.prefix = ''.join(random.sample(string.ascii_letters, 7))

    def set_prefix(self):
        self.prefix = ''.join(random.sample(string.ascii_letters, 7))

    def set_suffix(self):
        self.suffix = '_' + date.today().strftime('%Y%m%d')+'_'+self._get_random()

    def get_prefix(self):
        return self.prefix

    def get_suffix(self):
        return self.suffix

    @staticmethod
    def _get_random():
        return str(random.randint(0, 1000))
