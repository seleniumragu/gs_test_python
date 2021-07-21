# -*- coding: utf-8 -*-
from abc import abstractmethod


class Serializable(object):
    @abstractmethod
    def dump(self, path):
        pass

    @classmethod
    @abstractmethod
    def load(cls, path):
        pass
