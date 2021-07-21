import os

import yaml


class ConfigYaml(object):
    def __call__(
            self, path='config_preprod.yaml', *args, **kwargs
    ):
        try:
            with open(
                    os.path.abspath(
                        os.path.join(
                            os.path.dirname(__file__),
                            path
                        )
                    ), 'r'
            ) as yml:
                conf_data = yaml.safe_load(yml)
        except IOError:
            raise
        except:
            conf_data = {}

        return conf_data
