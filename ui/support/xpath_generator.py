class XPathGenerator(object):
    # xPath methods generate xPath based on label
    @staticmethod
    def single_input(label):
        """
        Param: Label name
        Return Xpath for the single line input field
        """
        return "//td[contains(@class,'labelCol')]//label[text()='" + label + "']/following::input[1]"

    @staticmethod
    def multi_line_input(label):
        """
        Param: Label name
        Return Xpath for the multiple line input field
        """
        return "//td[contains(@class,'labelCol')]//label[text()='" + label + "']/following::textarea[1]"

    @staticmethod
    def single_select(label):
        """
        Param: Label name
        Return Xpath for the select input field
        """
        return "//td[contains(@class,'labelCol')]//label[text()='" + label + "']/following::select[1]"

    @staticmethod
    def select_option(label, value):
        """
        Param: Label name, option value
        Return Xpath for the select option field
        """
        return "//td[contains(@class,'labelCol')]//label[text()='" + label + "']/following::select[1]/option[text()='" + value + "']"

    @staticmethod
    def lookup(label):
        """
        Param: Label name
        Return Xpath for the look up input field
        """
        return "//td[contains(@class,'labelCol')]//label[text()='" + label + "']/following::input[7]"

    @staticmethod
    def single_field(label):
        """
        Param: Label name
        Return Xpath for the single line input field
        """
        return "//td[text()='" + label + "']/following::td[1]"

    @staticmethod
    def single_field_with_help_icon(label):
        """
        Param: Label name
        Return Xpath for the single line input field
        """
        return "//td/span[text()='" + label + "']/following::td[1]"

    @staticmethod
    def continue_on_record_type_page():
        """
        Return Xpath for the record type page
        """
        return "//td[@id='bottomButtonRow']/input[@name='save']"

    @staticmethod
    def cancel_on_record_type_page():
        """
        Return Xpath for the record type page
        """
        return "//td[@id='bottomButtonRow']/input[@name='cancel']"

    @staticmethod
    def customized_button(name):
        """
        Return Xpath for customized button
        """
        return "//input[@value='" + name + "']"

    @staticmethod
    def button_on_section_standard(section_name, button_name, position=None):
        """
        sectionName should be as "Campaign Edit" or "Campaign Detail", based on current page
        """
        p = "top"
        if position is not None:
            p = position
        return "//div//h2[text()='" + section_name + "']/following::td[@id='" + p + "ButtonRow']/input[@name='" + button_name + "']"

    @staticmethod
    def button_on_section_standard_by_name(self, section_name, button_name, position="top"):
        """
        Return Xpath for button on section
        """
        return self.buttonOnSectionStandard(section_name, button_name, position)

    @staticmethod
    def save_on_section_standard_top(self, section_name):
        """
        Return Xpath for save on section standard top
        """
        return self.buttonOnSectionStandard(section_name, "save")

    @staticmethod
    def save_new_on_section_standard_top(self, section_name):
        """
        Return Xpath for save new on section standard top
        """
        return self.buttonOnSectionStandard(section_name, "save_new")

    @staticmethod
    def cancel_on_section_standard_top(self, section_name):
        return self.buttonOnSectionStandard(section_name, "cancel")

    @staticmethod
    def edit_on_section_standard_top(self, section_name):
        """
        Return Xpath for edit on section standard top
        """
        return self.buttonOnSectionStandard(section_name, "edit")

    @staticmethod
    def share_on_section_standard_top(self, section_name):
        """
        Return Xpath for share on section standard top
        """
        return self.buttonOnSectionStandard(section_name, "share", "top")

    @staticmethod
    def activate_on_section_standard_top(self, section_name):
        """
        Return Xpath for activate on section standard top
        """
        return self.buttonOnSectionStandard(section_name, "activate", "top")

    @staticmethod
    def deactivate_on_section_standard_top(self, section_name):
        """
        Return Xpath for deactivate on section standard top
        """
        return self.buttonOnSectionStandard(section_name, "deactivate", "top")

    @staticmethod
    def save_on_section_standard_bottom(self, section_name):
        """
        Return Xpath for save on section standard bottom
        """
        return self.buttonOnSectionStandard(section_name, "save", "bottom")

    @staticmethod
    def save_new_on_section_standard_bottom(self, section_name):
        """
        Return Xpath for save new on section standard bottom
        """
        return self.buttonOnSectionStandard(section_name, "save_new", "bottom")

    @staticmethod
    def cancel_on_section_standard_bottom(self, section_name):
        """
        Return Xpath for cancel on section standard bottom
        """
        return self.buttonOnSectionStandard(section_name, "cancel", "bottom")

    @staticmethod
    def edit_on_section_standard_bottom(self, section_name):
        """
        Return Xpath for edit on section standard bottom
        """
        return self.buttonOnSectionStandard(section_name, "edit", "bottom")

    @staticmethod
    def share_on_section_standard_bottom(self, section_name):
        """
        Return Xpath for share on section standard bottom
        """
        return self.buttonOnSectionStandard(section_name, "share", "bottom")

    @staticmethod
    def activate_on_section_standard_bottom(self, section_name):
        """
        Return Xpath for activate on section standard bottom
        """
        return self.buttonOnSectionStandard(section_name, "activate", "bottom")

    @staticmethod
    def deactivate_on_section_standard_bottom(self, section_name):
        """
        Return Xpath for deactivate new on section standard bottom
        """
        return self.buttonOnSectionStandard(section_name, "deactivate", "bottom")

    @staticmethod
    def iframe(iframe_class):
        """
        Return Xpath for iframe
        """
        return "//iframe[contains(@class,'" + iframe_class + "')]"

    @staticmethod
    def iframe_by_title(iframe_title):
        """
        Return Xpath for iframe by title
        """
        return "//iframe[@title='" + iframe_title + "']"

    @staticmethod
    def button_by_text(text):
        return "//button[text()='" + text + "']"

    @staticmethod
    def group_calendar_block():
        """
        Return Xpath for group calendar by block
        """
        return "//div[contains(@class,'scheduler_default_event')][0]"

    # Exception
    @staticmethod
    def message_on_top():
        # regard that there is only one error div in page
        """
        Return Xpath for message on top
        """
        return "//div[@class='pbError']"

    @staticmethod
    def message_follows_fields():
        """
        Return Xpath for message follows fields
        """
        return "//div[@class='errorMsg']"

    @staticmethod
    def message_follows_field(label):
        """
        Return Xpath for message follows field
        """
        return "//td[contains(@class,'labelCol')]//label[text()='" + label + "']/following::div[@class='errorMsg'][1]"

    @staticmethod
    def insufficient_privileges():
        """
        Return Xpath for insufficient privileges
        """
        return "//span[text()='Insufficient Privileges']"
