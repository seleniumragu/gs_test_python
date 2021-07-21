# -*- coding: utf-8 -*-
import time
from contextlib import contextmanager

from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.ie.webdriver import DEFAULT_TIMEOUT
from selenium.webdriver.common.action_chains import ActionChains

from ui.support import WaitUtils


class ElementManager(object):
    timeout = 30
    interval = 0.5

    def __init__(self, anchor):
        if not isinstance(anchor, (WebDriver, WebElement)):
            raise TypeError('Not supported anchor type')

        self.anchor = anchor

        if isinstance(anchor, WebElement):
            self.driver = self.anchor.parent
        else:
            self.driver = self.anchor

    def element_exists(
            self, locator, timeout=DEFAULT_TIMEOUT
    ):
        try:
            if self.find_element(locator, timeout):
                return True
            else:
                return False
        except:
            return False

    def element_visible(
            self, locator, timeout=DEFAULT_TIMEOUT
    ):
        try:
            elements = WaitUtils.wait_for_elements_visible(
                self.anchor,
                locator,
                self.interval,
                timeout
            )
        except TimeoutException:
            return False
        else:
            return True

    def element_dismissed(
            self, locator, timeout=DEFAULT_TIMEOUT
    ):
        try:
            WaitUtils.wait_for_element_invisible(
                self.anchor,
                locator,
                self.interval,
                timeout or self.timeout
            )
        except TimeoutException:
            return False
        else:
            return True

    def find_element_and_click(self, locator, timeout=DEFAULT_TIMEOUT):
        element = None
        try:
            element = WaitUtils.wait_for_elements_visible(self.anchor,
                                                          locator,
                                                          self.interval,
                                                          timeout or self.timeout)
            element = WaitUtils.wait_for_elements_present(self.anchor,
                                                          locator,
                                                          self.interval,
                                                          timeout or self.timeout)

            element = WaitUtils.wait_for_element_clickable(
                self.anchor,
                locator,
                self.interval,
                timeout or self.timeout
            )

        except TimeoutException:
            raise TimeoutException('Element is not clickable')
        # else:
        #
        #     _ = element.location_once_scrolled_into_view
        #     element.click()

        element.location_once_scrolled_into_view

        actions = ActionChains(self.driver)
        actions.move_to_element(element)\
            .click(element)\
            .perform()

    def find_element_and_input(
            self, locator, input_value,timeout=DEFAULT_TIMEOUT
    ):
        self.element_visible(locator)

        element = self.find_element(locator, timeout=timeout)

        if not element:
            raise TimeoutException('Unable to locate the element')

        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element.clear()
        element.send_keys(input_value)

    def find_element_and_return_text(
            self, locator, timeout=DEFAULT_TIMEOUT
    ):
        element = self.find_element(locator, timeout)

        return element.text if element else ''

    def find_elements(
            self, locator,
            until_number=1,
            timeout=timeout
    ):
        elements = []
        query_timeout = 30
        timeout = time.time() + (timeout or self.timeout)

        while True:
            try:
                elements = WaitUtils.wait_for_elements_visible(
                    self.anchor,
                    locator,
                    self.interval,
                    query_timeout
                )
            except TimeoutException:
                if time.time() > timeout:
                    elements = self.anchor.find_elements(*locator)

            if len(elements) >= until_number:
                break
            else:
                if time.time() > timeout:
                    elements = []

                    break
        return elements

    def find_element(self, locator, timeout=DEFAULT_TIMEOUT):
        elements = self.find_elements(
            locator,
            timeout=timeout
        )

        if elements:
            return elements[0]
        else:
            return None

    def select_element(self, element, timeout=DEFAULT_TIMEOUT):
        # TODO: supposed to accept locator here
        if not isinstance(element, WebElement):
            raise TypeError(
                'Not supported element (type={})'.format(
                    type(element)
                )
            )

        try:
            WaitUtils.wait_for_element_presents(
                self.driver, element,
                timeout or self.timeout
            )
        except TimeoutException:
            pass

        if element.tag_name.lower() == 'select':
            element = Select(element)

        return element

    @contextmanager
    def switch_to_iframe(
            self, locator, timeout=DEFAULT_TIMEOUT, ignore_error=False
    ):
        """
        ContextManager for switching into/out from frame
        :param locator: frame locator or element
        :param timeout: Timeout for smart wait
        :param ignore_error: Ignore timeout exception if True
        :return: N/A
        """
        switched_to_frame = False

        try:
            switched_to_frame = WaitUtils.wait_for_frame_available(
                self.driver,
                locator,
                self.interval,
                timeout
            )
        except TimeoutException:
            if ignore_error:
                yield
            else:
                raise TimeoutException(
                    'Unable to find the frame '
                    '({}:{}) and switch to it'.format(
                        *locator
                    )
                )
        else:
            yield
        finally:
            if switched_to_frame:
                try:
                    self.driver.switch_to.parent_frame()
                except NoSuchWindowException:
                    pass
                except Exception as ex:
                    pass
