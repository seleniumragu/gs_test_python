from selenium.webdriver.common.by import By

from ui.base_page import BasePage
from ui.support.generate_unique_name import GenerateUniqueName


class ProjectsPage(BasePage):
    # PageObject definition
    projectName = []
    new_project_btn = (By.XPATH, '//span[text()="new project"]')
    new_project_txt = (By.XPATH, '//h1[text()="Home"]')
    project_name = (By.ID, 'input-field-name')
    project_des = (By.ID, 'textarea-field-nameTextArea')
    add_btn = (By.XPATH, '//span[text()="Add"]')
    project_headlines_txt = (By.CLASS_NAME, 'saved-project__headline__name__text')

    def click_new_project_btn(self):
        self.page_operation.click_element(self.new_project_btn)

    def check_new_project_txt(self):
        self.page_operation.element_exists(self.new_project_txt)

    def enter_project_name(self):
        project_name_value = '[Test] Automation' + GenerateUniqueName()._get_random()
        ProjectsPage.projectName.append(project_name_value)
        self.page_operation.input_element(self.project_name, project_name_value)

    def enter_project_description(self, value):
        self.page_operation.input_element(self.project_des, value)

    def click_add_btn(self):
        self.page_operation.click_element(self.add_btn)
        self.hard_sleep(3)
        self.page_operation.element_exists(self.project_headlines_txt, self.projectName)


class CreateSimulation(BasePage):
    # PageObject definition
    simulationName = []
    project_expand_icon = (By.CLASS_NAME, 'icon-carat ')
    new_simulation_btn = (By.XPATH, '//span[text()="new simulation"]')
    new_simulation_txt = (By.XPATH, '//h1[text()="New Simulation"]')
    simulation_name = (By.ID, 'input-field-name')
    simulation_des = (By.ID, 'textarea-field-description')
    next_btn = (By.XPATH, '//span[text()="Next"]')
    created_simulation_txt = (By.CLASS_NAME, 'saved-config__container saved-config__container--no-progress')

    def click_project_expand_icon(self):
        self.page_operation.click_element(self.project_expand_icon)

    def click_new_simulation_btn(self):
        self.page_operation.click_element(self.new_simulation_btn)

    def check_new_simulation_txt(self):
        self.page_operation.element_exists(self.new_simulation_txt)

    def enter_simulation_name(self):
        simulation_name_value = '[Test] Simulation' + GenerateUniqueName()._get_random()
        ProjectsPage.projectName.append(simulation_name_value)
        self.page_operation.input_element(self.simulation_name, simulation_name_value)

    def enter_simulation_description(self, value):
        self.page_operation.input_element(self.simulation_des, value)

    def click_next_btn(self):
        self.page_operation.click_element(self.next_btn)
        self.hard_sleep(3)

    def simulation_exists(self):
        self.page_operation.element_exists(self.created_simulation_txt, self.simulationName)





