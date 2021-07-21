# -*- coding: utf-8 -*-
from behave.fixture import fixture_call_params
from behave.fixture import use_composite_fixture_with
from behave.fixture import use_fixture

from features.fixture import fixture_browser, fixture_mobile_parameter_set, fixture_mobile
from features.fixture import fixture_sql_database
from features.fixture import fixture_api_session
from features.fixture import fixture_test_configuration

from features.fixture_context import fixture_all
from features.fixture_context import fixture_feature
from features.fixture_context import fixture_scenario


from fnmatch import fnmatchcase

from utils.logger import logger


class FixtureInitiator(object):
    def __init__(self, context, feature):
        self.context, self.feature = context, feature

    def init_fixture(self):
        tags = self.feature.tags
        for tag in tags:
            if fnmatchcase(tag, '*.sql_database.*'):
                use_composite_fixture_with(
                    self.context, (
                        fixture_call_params(fixture_sql_database, tag),
                    )
                )
            if fnmatchcase(tag, '*.api.*'):
                use_composite_fixture_with(
                    self.context, (
                        fixture_call_params(fixture_api_session, tag),
                    )
                )
            if fnmatchcase(tag, '*.browser.*'):
                use_composite_fixture_with(
                    self.context, (
                        fixture_call_params(fixture_browser, tag),
                    )
                )
            if fnmatchcase(tag, '*.mobile.*'):
                use_composite_fixture_with(
                    self.context, (
                        fixture_call_params(fixture_mobile_parameter_set, tag),
                    )
                )


def before_step(context, step):
    pass


def before_scenario(context, scenario):

    try:
        userdata = context.config.userdata
        driver_type = userdata.get('browser', 'chrome')
    except Exception:
        driver_type = 'chrome'

    if driver_type == 'appium':
        use_composite_fixture_with(
            context, (
                fixture_call_params(
                    fixture_mobile
                ),
            )
        )

    use_composite_fixture_with(
        context, (
            fixture_call_params(
                fixture_scenario,
                scenario
            ),
        )
    )


def before_feature(context, feature):
    use_composite_fixture_with(
        context, (
            fixture_call_params(
                fixture_feature,
                feature
            ),
        )
    )
    fixture_initiator = FixtureInitiator(context, feature)
    fixture_initiator.init_fixture()


def before_all(context):
    context.logger = logger
    context.logger.setLevel(
        context.config.logging_level
    )

    use_fixture(
        fixture_all, context
    )

    use_fixture(
        fixture_test_configuration, context
    )
