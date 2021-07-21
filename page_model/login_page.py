__author__ = 'Ragu.Sekaran'

from selenium.webdriver.common.by import By

from ui.base_page import BasePage


class LoginPage(BasePage):
    # PageObject definition
    input_username = (By.ID, 'email')
    input_password = (By.ID, 'password')
    button_sign_in = (By.XPATH, '//span[text()="Login"]')

    def load(self):
        self.page_operation.goto_url()
        return self

    def enter_username(self, value):
        self.page_operation.input_element(self.input_username, value)

    def enter_password(self, value):
        self.page_operation.input_element(self.input_password, value)

    def click_sign_in_btn(self):
        self.page_operation.click_element(self.button_sign_in)

    def ui_login(self):
        login_user = self.context.login_user
        username = self.context.ui_config['test_user'][login_user]['Username']
        password = self.context.ui_config['test_user'][login_user]['Password']

        self.enter_username(username)
        self.enter_password(password)
        self.click_sign_in_btn()
