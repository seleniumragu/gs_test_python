from page_model.login_page import LoginPage
from behave import then, step, given

from page_model.home_page import TabBar
from page_model.logout_page import LogoutPage
from utils.yml_data import YMLData
from utils.logger import logger


def _load_cookies(browser, filename):
    for cookie in getattr(
            YMLData.load(filename),
            'cookies', []
    ):
        try:
            browser.add_cookie(vars(cookie))
        except Exception as ex:
            logger.error(ex)


# CN
@given('{login_user} I am an admin user I can enter the username and password')
def step_impl(context, login_user):
    context.login_user = login_user
    login_page = LoginPage(context)
    login_page.ui_login()


@then('I can see the home page')
def step_impl(context):
    context.tabs_page = TabBar(context)
    context.tabs_page.check_this_is_home_page()


@step('Logout the current user')
def step_logout(context):
    LogoutPage(
        context.browser
    ).logout()

