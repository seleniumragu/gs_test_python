# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import uuid

import yaml
from allure import attach
from allure import attachment_type
from behave import fixture
from behave.textutil import text
from page_model.logout_page import LogoutPage

import time

from utils.logger import logger
from utils.yml_data import YMLData

STORE_LOCATION = os.path.join(
    tempfile.gettempdir(),
    '.store.force'
)


class BehavePatcher(object):
    def __init__(self):
        pass

    def __init__(self, context, step):
        self.context, self.step = context, step

    def insert_png_to_allure_report(self, name='Screenshot'):
        name = 'Screenshot'
        if not hasattr(self.context, 'browser'):
            return
        if self.context.browser:
            try:
                attach(
                    name=name,
                    body=self.context.browser.get_screen_shot_as_png(),
                    attachment_type=attachment_type.PNG
                )
            except Exception:
                raise RuntimeError(
                    'Failed to insert screenshot to allure report'
                )


def setup_all(context):
    context.data, context.loaded_yml_files = load_context_data()

    if 'features' not in vars(context.data):
        context.data = YMLData(
            **dict(features=[])
        )

    if not os.path.exists(STORE_LOCATION):
        os.makedirs(STORE_LOCATION)

    return context.data


# def teardown_all(context):
#     clean_up_test_data(context.data)
#     save_context_data(context.data)
#     remove_obsolete_files(
#         context.loaded_yml_files
#     )


def setup_feature(context, feature):
    names = [
        _feature.name
        for _feature in context.data.features
    ]

    if feature.name not in names:
        context.data.features += [
            dict(
                name=feature.name,
                scenarios=[]
            )
        ]
    else:
        if feature.name != names[-1]:
            _feature = context.data.features.pop(
                names.index(feature.name)
            )
            context.data.features.append(_feature)

    return context.data.features[-1]


def teardown_feature(context, feature):
    context.data.features[-1].status = feature.status.name


def setup_scenario(context, scenario):
    feature = context.data.features[-1]

    names = [
        _scenario.name
        for _scenario in feature.scenarios
    ]

    if scenario.name not in names:
        feature.scenarios += [
            dict(name=scenario.name)
        ]
    else:
        if scenario.name != names[-1]:
            _scenario = feature.scenarios.pop(
                names.index(scenario.name)
            )

            feature.scenarios.append(_scenario)

    return context.data.features[-1].scenarios[-1]


def log_out_from_ui(context, scenario):
    if not hasattr(context, "browser"):
        return
    home_page = LogoutPage(context)
    home_page.logout()


def take_snapshot_for_ui(context, scenario):
    if not hasattr(context, "browser"):
        return
    scenario_data = context.data.features[-1].scenarios[-1]
    if scenario.status.name != 'passed':
        BehavePatcher(context, scenario).insert_png_to_allure_report("Fail Step Screenshot")


def teardown_scenario(context, scenario):
    scenario_data = context.data.features[-1].scenarios[-1]
    if scenario_data:
        scenario_data.status = scenario.status.name
        attach(
            name=text(scenario_data.name),
            body=yaml.dump(scenario_data),
            attachment_type=attachment_type.YAML,
            extension='yml'
        )


@fixture
def fixture_all(context):
    setup_all(context)

    yield

    # teardown_all(context)


@fixture
def fixture_feature(context, feature):
    setup_feature(context, feature)
    yield
    teardown_feature(context, feature)


@fixture
def fixture_scenario(context, scenario):
    context.logger.info(
        'RUNNING - Scenario: {}'.format(scenario.name)
    )
    setup_scenario(context, scenario)
    yield
    take_snapshot_for_ui(context, scenario)
    # clean_up_scenario_data(context, scenario)
    teardown_scenario(context, scenario)
    # log_out_from_ui(context, scenario)
    context.logger.info(
        '{} - Scenario: {}'.format(
            scenario.status.name.upper(),
            scenario.name
        )
    )
    time.sleep(0.5)


def remove_obsolete_files(files):
    for fp in files:
        try:
            if os.path.exists(fp):
                os.remove(fp)
        except IOError as ioe:
            logger.warning(ioe)
        except Exception as ex:
            logger.error(ex)


def remove_empty_directory(
        location=STORE_LOCATION
):
    try:
        if not os.listdir(location):
            shutil.rmtree(
                location,
                ignore_errors=True
            )
    except FileNotFoundError:
        logger.debug(
            'YML file directory ({}) was not found'.format(
                location
            )
        )


def save_context_data(data):
    remove_empty_directory()

    if not data:
        return

    if not isinstance(data, YMLData):
        raise TypeError(
            'Invalid context data'
        )

    try:
        if not os.path.exists(STORE_LOCATION):
            os.makedirs(STORE_LOCATION)

        dump_file = os.path.join(
            STORE_LOCATION,
            '{}.yml'.format(uuid.uuid4())
        )

        data.dump(dump_file)
    except:
        raise

    return dump_file


def load_context_data(
        file_location=STORE_LOCATION
):
    context_data = YMLData()
    loaded_files = []

    try:
        if file_location and os.path.exists(file_location):
            for root, _, files in os.walk(file_location):
                for file in files:
                    yml_file = os.path.join(root, file)

                    context_data += context_data.load(
                        yml_file
                    )

                    loaded_files.append(yml_file)
    except:
        pass

    return context_data, loaded_files
