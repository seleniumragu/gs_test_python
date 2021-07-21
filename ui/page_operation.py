# -*- coding: utf-8 -*-

import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from ui.browser import Browser
from ui.element_manager import ElementManager
from ui.support import WaitUtils
from selenium.webdriver.ie.webdriver import DEFAULT_TIMEOUT
from datetime import datetime


class PageOperation(ElementManager):

    def __init__(self, context):
        browser = context.browser
        if not isinstance(browser, Browser):
            raise TypeError('Invalid browser')

        self.browser = browser

        super(PageOperation, self).__init__(
            browser.get_webdriver()
        )

    # Get current url
    def get_url(self):
        """
        To get the current url
        """
        return self.browser.get_current_url()

    # Go to identify url
    def goto_url(self, url=''):
        """
        To go the specific url page
        :param url: url to go
        """
        self.browser.open(self.browser.base_url+url)

    def get_page_source(self):
        """
        To get the page source
        """
        return self.browser.get_pageSource()

    # Scroll the page to point or size
    def page_down(self, size=400):
        """
        To Scroll page for a specific size
        :param size: for scrolling page down for particular size
        """
        self.browser.execute_script("window.scrollTo(0, {});".format(size))

    # Scroll back
    def page_up(self):
        """
        To scroll page up
        """
        self.browser.execute_script("window.scrollTo(0, 0);")

    # Wait page load
    def _loading_finish(self):
        """
        Wait for page loading to finish
        """
        try:
            WaitUtils.wait_for_element_invisible(
                self.driver,
                Elements.Any_api_call_loading
            )

            WaitUtils.wait_for_element_invisible(
                self.driver,
                (By.CLASS_NAME, 'slds-spinner_container'),
                timeout=60
            )
        except Exception as ex:
            logger.error(ex)
        pass

    # Navigate to url
    def navigate_to(self, url):
        """
        navigate to specific page
        :param url: url to navigate the page
        """
        self.browser.open(url)
        self.browser.close_window()

    def click_element(
            self, locator, until_condition=None, timeout=DEFAULT_TIMEOUT
    ):
        """
        Do the smart wait and find the element by locator then click
        :param locator: Tuple type like (by, value)
        :param until_condition: The click action will replay until this condition return true
        :param timeout: Timeout for smart wait
        """
        # self._loading_finish()
        self.find_element_and_click(locator, timeout)
        start_time = datetime.now()
        if until_condition is not None:
            end_time = datetime.now()
            time_available = (end_time - start_time).seconds <= timeout
            while (not until_condition()) and time_available:
                self.find_element_and_click(locator, timeout)
                time.sleep(self.interval)
                # self.Hard_Sleep(self.interval)
                end_time = datetime.now()
                time_available = (end_time - start_time).seconds <= timeout

    def delete_element(
            self, locator, delete_value, xpath_value, timeout=DEFAULT_TIMEOUT
    ):
        """
        Do the smart wait and delete the element by locator then delete the value
        :param locator: Tuple type like (by, value)
        :param delete_value: value to delete the element
        :param xpath_value: xpath value to delete the element
        :param timeout: Timeout for smart wait
        """
        elements_list = self.find_elements(locator, timeout=timeout)
        for ele in elements_list:
            if delete_value in ele.text:
                link_delete = ele.find_element_by_xpath(xpath_value)
                link_delete.click()
                self.accept_alert()

                break

    def input_element(self, locator, input_value, timeout=DEFAULT_TIMEOUT):
        """
        Do the smart wait and find the element by locator then input the value
        :param locator: Tuple type like (by, value)
        :param input_value: str type value to input
        :param timeout: Timeout for smart wait
        """
        self.find_element_and_input(
            locator, input_value, timeout
        )

    def get_text_element(self, locator, timeout=DEFAULT_TIMEOUT):
        """
        Do the smart wait and find the element by locator then return the text
        :param locator: Tuple type like (by, value)
        :param timeout: Timeout for smart wait
        :return: the text in the element
        """
        return self.find_element_and_return_text(locator, timeout)

    def element_dismissed(self, locator, timeout=DEFAULT_TIMEOUT):
        """
        Identify if element with the specified locator is hidden/dismissed
        :param locator: Tuple type like (By.ID, value)
        :param timeout: Timeout for smart wait
        :return: Boolean
        """
        # self._loading_finish()
        return super(PageOperation, self).element_dismissed(
            locator, timeout
        )

    def element_exists(self, locator, timeout=DEFAULT_TIMEOUT):
        """
        Identify if element exists with the specified locator
        :param locator: Tuple type like (By.ID, value)
        :param timeout: Timeout for smart wait
        :return: Boolean
        """
        return super(PageOperation, self).element_exists(
            locator, timeout
        )

    def element_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        """
        Identify if element exists with the specified locator
        :param locator: Tuple type like (By.ID, value)
        :param timeout: Timeout for smart wait
        :return: Boolean
        """
        return super(PageOperation, self).element_visible(
            locator, timeout
        )

    def find_elements(
            self, locator, until_number=1, timeout=DEFAULT_TIMEOUT
    ):
        """
        Return a list of elements which matching the locator
        :param locator: Tuple type like (By.ID, value)
        :param until_number: wait until the total element count reaches the number
        :param timeout: Timeout for smart wait
        :return: WebElement instances (default=2)
        """
        # self._loading_finish()
        return super(PageOperation, self).find_elements(
            locator, until_number, timeout
        )

    def find_element(self, locator, timeout=DEFAULT_TIMEOUT):
        """
        Return the element which matching the locator
        :param locator: Tuple type like (By.ID, value)
        :param timeout: Timeout for smart wait
        :return: WebElement instance
        """
        return super(PageOperation, self).find_element(
            locator, timeout
        )

    def assert_element_exist(self, locator, timeout=DEFAULT_TIMEOUT):
        """
        Do the smart wait and assert the element is existed or not,
        raise assert exception when it does not exist
        :param locator: Tuple type like (by, value)
        :param timeout: Timeout for smart wait
        """
        assert self.element_exists(
            locator, timeout
        ), 'The element does not exist after timeout limitation,' \
           'The element locator is ByType: {}, ByValue: {}'.format(*locator)

    def search_input_by_label(self, name, value):
        """
        Do the smart wait and find the element by locator then input the value
        :param name: label name can be part of
        :param value: str type value to input
        """
        xpath = '../following-sibling::td'
        ElementManager(
            self.find_sibling_element_by_tag_and_text(
                'label', name, xpath
            )
        ).find_element_and_input(
            (By.CSS_SELECTOR, 'span>input'), value
        )

    def search_input_by_label_with_span(self, name, value):
        """
        Do the smart wait and find the element by locator
        then input the value and the label have other property
        :param name: label name can be part of
        :param value: str type value to input
        """
        xpath = '../../following-sibling::td'
        ElementManager(
            self.find_sibling_element_by_tag_and_text(
                'label', name, xpath
            )
        ).find_element_and_input(
            (By.CSS_SELECTOR, 'span>input'), value
        )

    # Get element by label
    def _get_label_element(self, name):
        """
        get label element by name
        :param name: the name of the element
        :return: text in the element
        """
        return self._get_element_by_tag_and_text('label', name)

    # Generate the random suffix by current datetime
    @staticmethod
    def generate_random_suffix():
        """
        To generate the random suffix
        :return: random suffix
        """
        suffix = time.strftime('-%y%m%d%H%M', time.localtime(time.time()))
        return suffix

    def search_by_icon(self, name, value):
        """
        SearchItems the element by icon name
        :param value: the name of button
        """
        # self.click_element(
        #     (By.CSS_SELECTOR, "img[title='" + name + " Lookup (New Window)'")
        # )
        # sessions = self.browser.get_window_handles()
        # if sessions:
        #     popup_window = sessions[-1]
        #     self.browser.switch_to_window(popup_window)
        #
        #     with self.switch_to_iframe('searchFrame'):
        #         self.input_element(Elements.button_lksrch, value)
        #         self.click_element(Elements.link_go)
        #     with self.switch_to_iframe('resultsFrame'):
        #         self.click_element((By.LINK_TEXT, value))
        #
        #     self.browser.switch_to_window(sessions[0])
        # else:
        #     raise AssertionError('No popup window displayed')
        pass

    def select_by_label_by_visible_text(self, name, value):
        """
        Do the smart wait and find the element by locator then select the value
        :param name: label name can be part of
        :param value: str type value to select
        """
        xpath = '../following-sibling::td'
        dropdown = ElementManager(
            self.find_sibling_element_by_tag_and_text(
                'label', name, xpath
            )
        ).find_element(
            (By.TAG_NAME, 'select')
        )
        select = self.select_element(dropdown)
        select.select_by_visible_text(value)

    def select_option(self, locator, option_text):
        """
        To select an option
        :param locator: Tuple type like (by, value)
        :param option_text: option text to select
        """
        select = self.select_element(
            self.find_element(locator)
        )
        # self.find_element_and_click(locator=locator) #Keep this line in case of future tunning
        select.select_by_visible_text(option_text)

    def select_option_by_index(self, locator, index=0):
        """
        select option using option index
        :param locator: Tuple type like (by, value)
        :param index: option index to select
        """
        select = self.select_element(
            self.find_element(locator)
        )
        select.select_by_index(index)

    def toggle_checkbox(self, locator, on=True, timeout=DEFAULT_TIMEOUT):
        """
        Do the smart wait and find the element by locator then click the toggle checkbox
        :param locator: Tuple type like (by, value)
        :param on: toggle checkbox param on
        :param timeout: Timeout for smart wait
        """
        element = self.find_element(locator)
        if element and element.is_selected() != on:
            self.find_element_and_click(
                locator, timeout
            )

    def accept_alert(self):
        """
        To accept the alert
        :return: alert text
        """
        alert = None

        try:
            alert = WaitUtils.wait_for_alert_presents(
                self.driver
            )
            alert_text = alert.text
            alert.accept()
        except Exception:
            if alert:
                alert.dismiss()

            raise
        else:
            _ = self.driver.switch_to.active_element

        return alert_text

    def accept_confirm(self, confirm_button):
        """
        To accept the alert
        :param confirm_button: Confirm button to click
        """

        def condition():
            """
            To click the confirm button in the alert
            :return: element dismissed
            """
            return self.element_dismissed(confirm_button, 1)
        self.click_element(confirm_button, condition)

    def click_element_in_list(self, locator, list_position=0):
        """
        To click the element in the list
        :param locator: Tuple type like (by, value)
        :param list_position: list position to click the element
        """
        elements = self.find_elements(
            locator, 2
        )
        elements[list_position].click()

    def search_by_icon_result_in_list(self, name, value):
        """
        To search by icon in the list
        :param name: name to search by icon
        :param value: search by icon value
        """
        self.click_element(
            (By.CSS_SELECTOR, "img[title='" + name + " Lookup (New Window)'")
        )
        sessions = self.browser.get_window_handles()
        if sessions:
            self.browser.switch_to_window(sessions[1])

            with self.switch_to_iframe('searchFrame'):
                select = self.select_element(
                    self.find_element(
                        (By.TAG_NAME, 'select')
                    )
                )
                select.select_by_index(2)

                self.input_element(Elements.button_lksrch, value)
                self.click_element(Elements.link_go)

            with self.switch_to_iframe('resultsFrame'):
                self.click_element_in_list(
                    (By.PARTIAL_LINK_TEXT, value)
                )

            self.browser.switch_to_window(sessions[0])
        else:
            raise AssertionError('No popup window displayed')

    def search_by_icon_result_by_index(self, name, value, index=1):
        # self.click_element(
        #     (By.CSS_SELECTOR, "img[title='" + name + " Lookup (New Window)'")
        # )
        # sessions = self.browser.get_window_handles()
        # if sessions:
        #     popup_window = sessions[-1]
        #     self.browser.switch_to_window(popup_window)
        #
        #     with self.switch_to_iframe('searchFrame'):
        #         self.input_element(Elements.button_lksrch, value)
        #         self.click_element(Elements.link_go)
        #
        #     with self.switch_to_iframe('resultsFrame'):
        #         self.click_element_in_list(
        #             (By.PARTIAL_LINK_TEXT, value), index
        #         )
        #     self.browser.switch_to_window(sessions[0])
        # else:
        #     raise AssertionError('No popup window displayed')
        pass

    def mouse_move_to_element_with_offset_and_click(
            self, element, x_offset=-2, y_offset=0
    ):
        """
        To do the mouse move action using x,y co-ordinates
        :param element: Tuple type like (by, value)
        :param x_offset: x co-ordinate to move the mouse
        :param y_offset: y co-ordinate to move the mouse
        """
        ActionChains(self.driver).move_to_element_with_offset(
            element, x_offset, y_offset
        ).click().perform()

    def mouse_hover_on_element(self, locator):
        """
        To do the mouse hover action using the element
        :param locator: Tuple type like (by, value)
        """
        element = self.find_element(locator)
        ActionChains(
            self.driver
        ).move_to_element(element).perform()

    def click_element_in_iframe(
            self, iframe_locator, button_locator
    ):
        """
        To click the element inside the iframe
        :param iframe_locator: Tuple type like (by, value)
        :param button_locator: Tuple type like (by, value)
        """
        with self.switch_to_iframe(iframe_locator):
            self.click_element(button_locator)

    # Get text by label name
    def get_text_by_label(self, value):
        """
        To get the text by label
        :param value: label value to get the text
        :return: label text
        """
        element = self.find_sibling_element_by_tag_and_text(
            'td', value
        )
        return element.text if element else ''

    # Checked checkbox by label name
    def checked_by_label(self, name):
        """
        To click the element by label
        :param name: name value to click the element using label
        """
        ElementManager(
            self.find_sibling_element_by_tag_and_text('td', name)
        ).find_element_and_click(
            (By.TAG_NAME, 'input')
        )

    def find_sibling_element_by_tag_and_text(
            self, tag, text,
            sibling_path='./following-sibling::div'
    ):
        """
        To find the sibling element by tag and text values
        :param tag: tag name to find the sibling element
        :param text: tag name text
        :param sibling_path: sibling path to find the sibling element
        :return: element
        """
        element = self._get_element_by_tag_and_text(
            tag, text
        )

        if not element:
            logger.debug(
                'Unable to locate element by tag ({})'.format(text)
            )
        else:
            element = ElementManager(element).find_element(
                (By.XPATH, sibling_path)
            )
            if not element:
                logger.debug(
                    'Unable to locate element by xpath ({})'.format(
                        sibling_path
                    )
                )

        return element

    def _get_element_by_tag_and_text(self, tag, text):
        """
        To get element by tag and text values
        :param tag: tag name to get the text
        :param text: tag name text
        :return: element
        """
        element = None

        for element in self.find_elements(
                (By.TAG_NAME, tag)
        ):
            if element.text.startswith(text):
                break

        return element

    def search_by_icon_using_window_index(self, windowone,windowtwo, name, value):
        """
        SearchItems the element by icon name
        :param value: the name of button
        """
        # self.click_element(
        #     (By.CSS_SELECTOR, "img[title='" + name + " Lookup (New Window)'")
        # )
        # try:
        #     session = self.browser.get_window_handles()
        #     self.browser.switch_to_window(session[windowtwo])
        #
        #     with self.switch_to_iframe('searchFrame'):
        #         self.input_element(Elements.button_lksrch, value)
        #         self.click_element(Elements.link_go)
        #     with self.switch_to_iframe('resultsFrame'):
        #         self.click_element((By.LINK_TEXT, value))
        #
        #     self.browser.switch_to_window(session[windowone])
        # except:
        #     logger.warning('Index exceeded')
        pass

    def mouse_move_to_element(
            self, element
    ):
        """
        To move the mouse using the mouse actions
        :param element: element to move the mouse
        """
        ActionChains(self.driver).move_to_element(
            element
        ).click().perform()
