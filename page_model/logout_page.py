# -*- coding: utf-8 -*-
from ui.base_page import BasePage
from selenium.webdriver.common.by import By


class LogoutPage(BasePage):
    class Locators(object):
        mnu_user_panel = (By.CLASS_NAME, 'icon-cog ')
        btn_logout = (
            By.XPATH,
            '//p[text()="Logout"]'
        )

    def logout(self):
        if self.is_logged_in:
            self.page_operation.click_element(
                self.Locators.mnu_user_panel
            )

            self.page_operation.click_element(
                self.Locators.btn_logout
            )

            self.hard_sleep(3)

            # TODO: DEAL WITH ANY ALERTS

    @property
    def is_logged_in(self):
        return self.page_operation.element_exists(
            self.Locators.mnu_user_panel
        )
