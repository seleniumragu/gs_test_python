# -*- coding: utf-8 -*-
from configs.config_yaml import ConfigYaml


class ConfigManager(object):
    config_yaml = ConfigYaml()

    def add_config_context(self, context, bu=None, profile=None):
        # user_data = context.config.userdata
        # env_tag = user_data.get('env', 'test')
        env_tag = 'test'
        if not hasattr(context, 'test_config'):
            context.test_config = self.config_yaml(
                'config_{}.yaml'.format(
                    env_tag
                )
            )
