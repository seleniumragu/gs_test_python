import os
import sys

from behave import fixture


from page_model.login_page import LoginPage
from ui.browser import Browser
from ui.browser_manager import BrowserManager
from ui.browser import BrowserType
from utils.config_manager import ConfigManager
from utils.configuration_mobile import ConfigurationSet
from utils.logger import logger
from utils.sql_database_manager import SqlDatabaseManager
from utils.work_id_process import ProcessManage


@fixture
def fixture_browser(context, tag, *args, **kwargs):
    user_browser_tag = ""
    if hasattr(context, "user_browser_tag"):
        user_browser_tag = context.user_browser_tag

    project_tag = tag[tag.rindex('.') + 1:]
    context.ui_config = context.test_config['ui'][project_tag]

    try:
        context.browserManager = BrowserManager()
        if user_browser_tag == 'appium':
            pass
            # browser_type = BrowserType.APPIUM
            # context.browserManager.add_browser_queue(
            #     Browser(
            #         base_url=context.ui_config['base_url'],
            #         browser_type=browser_type,
            #         command_executor=ConfigMobile.appium_command_Executor,
            #         desired_capabilities=ConfigMobile.android_desired_capabilities
            #     )
            # )
        else:
            # if True:
            if os.environ.get('AUTOMATION_DOCKER_ENV') is not None:
                logger.info(" set AUTOMATION_DOCKER_ENV")
                # browser_type = BrowserType.HEADLESS_CHROME
                browser_type = BrowserType.HEADLESS_CHROME_WITH_PROXY
                logger.info("browser_type=" + browser_type)
            else:
                browser_type = context.ui_config['browser']
                logger.info("browser_type=" + browser_type)

            if sys.platform.startswith('Linux'):
                exec_path = '/usr/bin/google-chrome'
                os.environ['webdriver.chrome.driver'] = \
                    exec_path
                context.executable_path = exec_path

                context.browserManager.add_browser_queue(
                    Browser(
                        base_url=context.ui_config['base_url'],
                        browser_type=browser_type,
                        executable_path=exec_path
                    )
                )
            if user_browser_tag == 'zalenium':
                browser_type = browser_type
                context.browserManager.add_browser_queue(
                    Browser(
                        base_url=context.ui_config['base_url'],
                        browser_type=browser_type,
                        command_executor=ConfigZalenium.zalenium_command_executor,
                        desired_capabilities=ConfigZalenium.chrome_caps
                    )
                )
            else:
                context.browserManager.add_browser_queue(
                    Browser(base_url=context.ui_config['base_url'], browser_type=browser_type)
                )

            context.browser_type = browser_type
            context.browser = context.browserManager.get_browser()
            context.browser.maximize_window()
            login_page = LoginPage(context)
            login_page.load()

        yield context.browser
    finally:
        if context.browser:
            context.browser.quit()

        if context.browserManager:
            context.browserManager.clear_browsers()


@fixture
def fixture_sql_database(context, tag, *args, **kwargs):
    tag = tag[tag.rindex('.')+1:]
    database_tag = 'database_' + tag
    sql_db_config_dict = context.test_config['sql_database']
    host = sql_db_config_dict['server']
    user = sql_db_config_dict['user']
    pwd = sql_db_config_dict['password']
    database_name = sql_db_config_dict[database_tag]

    try:
        sql_database = SqlDatabaseManager(host, user, pwd, database_name)
        sql_database.connect_database()
        context.sql_database = sql_database
        yield sql_database
    finally:
        sql_database.close_database()


@fixture
def fixture_api_session(context, tag, *args, **kwargs):
    tag = tag[tag.rindex('.')+1:]
    api_config_dict = context.test_config['api'][tag]

    base_url = api_config_dict['base_url']
    username = api_config_dict['username']
    password = api_config_dict['password']

    api_session = BaseSession(base_url, username, password)
    if username and password:
            api_session.set_auth()
    context.api_session = api_session



@fixture
def fixture_mobile_parameter_set(context, tag, *args, **kwargs ):
    # if you want to debug, give a default value for each parameter

    userdata = context.config.userdata

    try:
        parallel_flag_p = userdata.get('parallel_flag', 'false')
        if parallel_flag_p == "" or parallel_flag_p is None:
            raise Exception("For mobile execution, parameter parallel_flag is required in command")
        else:
            context.parallel_flag = parallel_flag_p.lower()
    except:
        raise Exception("For mobile execution, parameter parallel_flag is required in command")

    if context.parallel_flag == 'true':
        try:
            process_id_p = context.config.userdata['process_id'].lower()
        except Exception:
            process_id_p = ''

        if process_id_p == "" or process_id_p is None:
            raise Exception("For parallel execution, parameter process_id is required in command")
        else:
            context.process_id = process_id_p.lower()
    else:
        context.process_id = "default"

    try:
        platform_value_p = userdata.get('platform', 'android')
        if platform_value_p == "" or platform_value_p is None:
            raise Exception("For mobile execution, parameter platform is required in command")
        else:
            context.platform_value = platform_value_p
    except Exception:
        raise Exception("For mobile execution, parameter platform is required in command")

    try:
        device_name_p = userdata.get('device', 'deviceone')
        if device_name_p == "" or platform_value_p is None:
            raise Exception("For mobile execution, parameter device is required in command")
        else:
            context.device_name = device_name_p
    except Exception:
        raise Exception("For mobile execution, parameter device is required in command")

    ProcessManage.setupworkprocess(context.parallel_flag,context.process_id)
    ConfigurationSet.initiateconfigvalue(context.parallel_flag,context.platform_value,context.device_name)


@fixture
def fixture_mobile(context, *args, **kwargs):

    try:
        context.browserManager = BrowserManager()
        browser_type = BrowserType.APPIUM
        platform_value = context.platform_value
        parallel_flag = context.parallel_flag
        DriverManagement.set_up_mobile_driver_manage(platform_value,parallel_flag)

        context.browserManager.add_browser_queue(
            Browser(
                base_url = "",
                browser_type=browser_type
            )
        )

        context.browser_type = browser_type
        context.browser = context.browserManager.get_browser()

        yield context.browser
    finally:
        try:
            if context.browserManager:
                context.browserManager.clear_browsers()
        except Exception:
            pass


@fixture
def fixture_test_configuration(context):
    ConfigManager().add_config_context(context)
