__author__ = 'Ragu.Sekaran'
from selenium.webdriver.common.by import By
import allure

from ui.base_page import BasePage


class TabBar(BasePage):
    home_txt = (By.XPATH, '//h1[text()="Home"]')
    projects_btn = (By.CLASS_NAME, 'icon-projects ')

    # Check this is the home page
    @allure.step
    def check_this_is_home_page(self):
        self.page_operation.element_exists(TabBar.home_txt)

    # Go to projects
    @allure.step
    def click_projects_btn(self):
        self.page_operation.click_element(TabBar.projects_btn)


