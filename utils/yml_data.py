# -*- coding: utf-8 -*-
import yaml

from .serializable import Serializable


class YMLData(yaml.YAMLObject, Serializable):
    yaml_tag = '!YMLData'

    def __init__(self, **kwargs):
        super(YMLData, self).__init__()

        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __getattr__(self, item):
        return self.__getattribute__(item)

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __setattr__(self, name, value):
        assert (name is not None) and getattr(
            name, 'strip', lambda: None
        )()

        vars(self).update(
            **{
                name: self.normalize_data(value)
            }
        )

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __iadd__(self, other):
        _data = self.normalize_data(other)

        if not isinstance(_data, type(self)):
            raise ValueError(
                'Assigning invalid value: ({})'.format(
                    other
                )
            )

        for key, value in vars(_data).items():
            vars(self).update(
                **{
                    key: value
                }
            )

        return self

    def dump(self, path):
        try:
            for key, value in vars(self).copy().items():
                if hasattr(value, '__dict__') and (
                        not isinstance(
                            value, yaml.YAMLObject
                        )
                ):
                    self.__delattr__(key)

            with open(path, 'w') as stream:
                yaml.dump(self, stream)
        except Exception:
            raise

    @classmethod
    def load(cls, path):
        try:
            with open(path, 'r') as stream:
                data = yaml.safe_load(stream)
        except IOError as ioe:
            data = dict(
                errno=ioe.errno,
                filename=ioe.filename,
                strerror=ioe.strerror
            )
        except Exception:
            raise

        return cls.normalize_data(data)

    @classmethod
    def normalize_data(cls, data):
        if isinstance(data, YMLData):
            return data

        if hasattr(data, '__dict__'):
            return YMLData(**vars(data))

        if isinstance(data, dict):
            return YMLData(**data)

        if isinstance(data, list):
            return [
                cls.normalize_data(datum)
                for datum in data
            ]

        return yaml.safe_load(
            yaml.safe_dump(data)
        )
