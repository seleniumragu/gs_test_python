# -*- coding: utf-8 -*-
import base64
import time
import allure
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.ie.webdriver import DEFAULT_TIMEOUT
from ui.browser import Browser
from ui.element_manager import ElementManager
from ui.mobile import get_current_mobile_driver
from utils.configuration_mobile import get_platform


class PageOperationMobile(ElementManager):

    def __init__( self, context ):

        self.driver = get_current_mobile_driver()

        browser = context.browser
        if not isinstance(browser, Browser):
            raise TypeError('Invalid browser')

        self.browser = browser

        super(PageOperationMobile, self).__init__(
            browser.get_webdriver()
        )

    def attach_description_and_screen_shot(self, description="this is step description"):
        """
        attach screen and description into allure report at any detail step
        :param description: description of step result
        """
        try:
            if description == 'this is step description':
                pass
            else:
                allure.attach(description)
        except Exception:
            raise Exception("Get exception error when attach step description into allure report")

        try:
            allure.attach(self.driver.get_screenshot_as_png())
        except Exception:
            raise Exception("Get exception error when take screen shot and attach to allure report")

    def verify_object_exists(self, locator, timeout=DEFAULT_TIMEOUT):
        """
        verify object exist on current page or not
        :param locator: Tuple type like (by, value)
        :param timeout: Timeout for smart wait
        """
        find_flag = False

        try:
            self.driver.implicitly_wait(2)
        except Exception:
            exception = str(Exception).format()
            raise Exception(
                "Get exception error when change selenium default wait time, error is " + exception)

        try:
            for i in range(0, timeout):
                list_object = self.driver.find_elements(*locator)
                if len(list_object) > 0:
                    find_flag = True
                    break
                time.sleep(1)

        except Exception:
            exception = str(Exception).format()
            raise Exception(
                "Can not find elements with provided locator " + str(locator) + ", Exception error:" + exception)


        try:
            self.driver.implicitly_wait(0)
        except Exception:
            exception = str(Exception).format()
            raise Exception(
                "Can not find elements with provided locator " + str(locator) + ", Exception error:" + exception)

        return find_flag

    def wait_elements_loading(self, locator, timeout=DEFAULT_TIMEOUT):
        """
        just wait for elements loading, if element is not displayed, no error
        :param locator: Tuple type like (by, value)
        :param timeout: Timeout for smart wait
        """
        self.driver.implicitly_wait(1)

        try:
            if get_platform().lower() == 'ios':
                for i in range(0, timeout):
                    list_object = self.driver.find_elements(*locator)
                    if len(list_object) > 0:
                        if list_object.__getitem__(0).is_displayed():
                            break
                    time.sleep(1)
            else:
                for i in range(0, timeout):
                    list_object = self.driver.find_elements(*locator)
                    if len(list_object) > 0:
                        break
                    time.sleep(1)
        except Exception:
            exception = str(Exception).format()
            raise Exception(
                "Can not find elements with provided locator " + str(locator) + ", Exception error:" + exception)

        self.driver.implicitly_wait(0)

    def click_element(self, locator, timeout=DEFAULT_TIMEOUT, description="click object"):
        """
        click the element until it displayed with smart wait
        :param locator: Tuple type like (by, value)
        :param timeout: Timeout for smart wait
        :param description: describe this action, it will displayed in allure report
        """
        if self.verify_object_exists(locator, timeout):
            try:
                self.driver.find_element(*locator).click()
                time.sleep(3)
                self.attach_description_and_screen_shot(description + "done")
            except Exception:
                exception = str(Exception).format()
                AssertionError(description + " get exception error, "
                                             "element " + str(locator) + " is not clickable. "
                                                                         "Exception error show as " + exception)
        else:
            raise AssertionError(description + " failed, element not displayed")

    def input_text_common(self, locator, value, timeout=DEFAULT_TIMEOUT, description="input field name"):
        """
        input value into element until it displayed with smart wait
        :param locator: Tuple type like (by, value)
        :param value: text value to input
        :param timeout: Timeout for smart wait
        :param description: describe input value into which field
        """
        if self.verify_object_exists(locator, timeout):
            try:
                self.driver.find_element(*locator).click()
                self.driver.find_element(*locator).clear()
                self.driver.find_element(*locator).send_keys(value)
                time.sleep(3)
                self.attach_description_and_screen_shot("Set " + description + " value as '" + value + "'")
            except Exception:
                exception = str(Exception).format()
                raise AssertionError("Set " + description + " value get error, "
                                                            "it is not editable, exception error is " + exception)
        else:
            raise AssertionError("Set " + description + " value, but " + description + " is not displayed")

    def clear_text_common(self, locator, timeout=DEFAULT_TIMEOUT, description="clear field name"):
        """
        clear the value in element until it displayed with smart wait
        :param locator: Tuple type like (by, value)
        :param timeout: Timeout for smart wait
        :param description: describe which field to clear value
        """
        if self.verify_object_exists(locator, timeout):
            try:
                self.driver.find_element(*locator).click()
                self.driver.find_element(*locator).clear()
                time.sleep(3)
                self.attach_description_and_screen_shot("Clear " + description + " value done")
            except Exception:
                raise AssertionError("Clear " + description + " value get error, it is not editable")
        else:
            raise AssertionError("Clear " + description + " value, but " + description + " is not displayed")

    def get_object_number(self, locator, timeout=DEFAULT_TIMEOUT):
        """
        get the number of objects with same locator
        :param locator: Tuple type like (by, value)
        :param timeout: Timeout for smart wait
        """
        object_number = 0
        self.driver.implicitly_wait(1)

        try:
            for i in range(0, timeout):
                list_object = self.driver.find_elements(*locator)
                if len(list_object) > 0:
                    object_number = len(list_object)
                    break
                time.sleep(1)
        except Exception:
            raise AssertionError("Can not find element via provided locator " + str(locator))

        self.driver.implicitly_wait(0)

        return object_number

    def verify_error_message_single(self, number=0, error_msg=''):
        """
        verify only one error message displayed on current page
        :param number: actual error message number
        :param error_msg: error message description
        """
        if number <= 0:
            raise AssertionError("Verify error message '" + error_msg + "' displayed, actual it is NOT displayed")
        elif number == 1:
            self.attach_description_and_screen_shot(
                "Verify error message '" + error_msg + "' displayed, and it is displayed")
        else:
            raise AssertionError(
                "Verify error message '" + error_msg + "' displayed, actual found multi same error message")

    def close_keyboard(self):
        """
        close the keyboard if displayed
        """
        if get_platform() == 'ios':
            try:
                keyboard_done = (MobileBy.IOS_PREDICATE, 'name == "Done"')
                self.driver.find_element(*keyboard_done).click()
            except Exception:
                pass
        else:
            try:
                self.driver.hide_keyboard()
            except Exception:
                pass

    def get_decode_password(self, decode_value):
        """
        attach screen and description into allure report at any detail step
        :param decode_value: decode value
        """
        data_bytes = decode_value.encode("utf-8")
        value = base64.b64decode(data_bytes)
        decode_value = value.decode("utf-8")
        return decode_value

    def swipe_from_element0_to_element1_ios(self, element0, element1):
        """
        user to swipe from object0 to object1 - mobile only function - ios
        :param element0: Tuple type like (By.ID, value)
        :param element1:  Tuple type like (By.ID, value)
        """

        if self.element_exists(element0, 2):
            if self.driver.find_element(*element0).is_displayed():
                element_0 = self.driver.find_element(*element0)
            else:
                raise AssertionError("Swipe from element " + str(element0).format() + " to element "
                                     + str(element1).format() + " , but element " + str(element0).format()
                                     + " is not visible")
        else:
            raise AssertionError("Swipe from element " + str(element0).format() + " to element "
                                 + str(element1).format() + " , but element " + str(element0).format()
                                 + " is not displayed")

        if self.element_exists(element1, 2):
            if self.driver.find_element(*element1).is_displayed():
                element_1 = self.driver.find_element(*element1)
            else:
                raise AssertionError("Swipe from element " + str(element0).format() + " to element "
                                     + str(element1).format() + " , but element " + str(element1).format()
                                     + " is not visible")
        else:
            raise AssertionError("Swipe from element " + str(element0).format() + " to element "
                                 + str(element1).format() + " , but element " + str(element1).format()
                                 + " is not displayed")

        try:
            touch_action = TouchAction(self.driver)
            touch_action.long_press(el=element_0).move_to(el=element_1).release().perform()
        except Exception:
            raise AssertionError("Swipe from element " + str(element0).format() + " to element "
                                 + str(element1).format() + " , but get exception when swipe ")

    def swipe_from_element0_element1_android(self, element0, element1):
        """
        user to swipe from object0 to object1 - mobile only function - android
        :param element0: Tuple type like (By.ID, value)
        :param element1:  Tuple type like (By.ID, value)
        """
        # for ios device, need check element visible before swipe
        if self.element_exists(element0, 5):
            element_0 = self.driver.find_element(*element0)
        else:
            raise AssertionError("Swipe from element " + str(element0).format() + " to element "
                                 + str(element1).format() + " , but element " + str(element0).format()
                                 + " is not displayed")

        if self.element_exists(element1, 5):
            element_1 = self.driver.find_element(*element1)
        else:
            raise AssertionError("Swipe from element " + str(element0).format() + " to element "
                                 + str(element1).format() + " , but element " + str(element1).format()
                                 + " is not displayed")

        try:
            touch_action = TouchAction(self.driver)
            touch_action.long_press(el=element_0).move_to(el=element_1).release().perform()
        except Exception:
            raise AssertionError("Swipe from element " + str(element0).format() + " to element "
                                 + str(element1).format() + " , but get exception when swipe ")

    def swipe_function_from_to_common(self, startx, starty, endx, endy):
        """
        swipe from position a to b - mobile only function
        :param startx: start x coordinate value
        :param starty: start y coordinate value
        :param endx: end x coordinate value
        :param endy: end y coordinate value
        """
        try:
            touch_action = TouchAction(self.driver)
            touch_action.long_press(x=startx, y=starty).move_to(x=endx, y=endy).release().perform()
        except Exception as exception:
            raise AssertionError("Get exception error when use swipe function, error as below: " +
                                 str(exception).format())

    def swipe_to_page_top_android(self):
        """
        swipe to the top of the page for android device
        """
        try:

            i = 0
            findFlag = False
            skipFlag = False

            while (findFlag is False) and (skipFlag is False):

                beforeswipe = self.driver.page_source

                width = self.driver.get_window_size()['width']
                height = self.driver.get_window_size()['height']
                startX = width / 2
                startY = height / 4
                endX = startX
                endY = (height / 4) * 3

                touch_action = TouchAction(self.driver)
                touch_action.long_press(x=startX, y=startY).move_to(x=endX, y=endY).release().perform()

                afterswipe = self.driver.page_source

                if beforeswipe == afterswipe:
                    findFlag = True

                i = i + 1
                if (i > 30) and (findFlag is False):
                    skipFlag = True
                    raise AssertionError("Swipe 30 times, still not get the Top of the page, "
                                         "please check if the page is hang up")

        except Exception as exception:
            raise AssertionError("Get exception error when do swipe function, exception error as "
                                 + str(exception).format())

    def swipe_to_page_bottom_android(self):
        """
        swipe to the bottom of the page for android device
        """
        try:

            i = 0
            findFlag = False
            skipFlag = False

            while (findFlag is False) and (skipFlag is False):

                beforeswipe = self.driver.page_source

                width = self.driver.get_window_size()['width']
                height = self.driver.get_window_size()['height']
                startX = width / 2
                startY = (height / 4) * 3
                endX = startX
                endY = height / 4

                touch_action = TouchAction(self.driver)
                touch_action.long_press(x=startX, y=startY).move_to(x=endX, y=endY).release().perform()

                afterswipe = self.driver.page_source

                if beforeswipe == afterswipe:
                    findFlag = True

                i = i + 1
                if (i > 30) and (findFlag is False):
                    skipFlag = True
                    raise AssertionError("Swipe 30 times, still not get the Top of the page, "
                                         "please check if the page is hang up")

        except Exception as exception:
            raise AssertionError("Get exception error when do swipe function, exception error as "
                                 + str(exception).format())

    def swipe_to_page_top_ios(self):
        """
        swipe to the top of the page for ios device
        """
        try:

            i = 0
            findFlag = False
            skipFlag = False

            while (findFlag is False) and (skipFlag is False):

                beforeswipe = str(self.driver.page_source)
                beforeswipe_array = beforeswipe.split("XCUIElementTypeWindow")[2]

                width = self.driver.get_window_size()['width']
                height = self.driver.get_window_size()['height']
                startX = width / 2
                startY = height / 4
                endX = startX
                endY = (height / 4) * 3

                touch_action = TouchAction(self.driver)
                touch_action.long_press(x=startX, y=startY).move_to(x=endX, y=endY).release().perform()
                time.sleep(3)

                afterswipe = str(self.driver.page_source)
                afterswipe_array = afterswipe.split("XCUIElementTypeWindow")[2]


                if beforeswipe_array == afterswipe_array:
                    findFlag = True
                    break

                i = i + 1
                if (i > 30) and (findFlag is False):
                    skipFlag = True
                    raise AssertionError("Swipe 30 times, still not get the Top of the page, "
                                         "please check if the page is hang up")

        except Exception as exception:
            raise AssertionError("Get exception error when do swipe function, exception error as "
                                 + str(exception).format())

    def swipe_to_page_bottom_ios(self):
        """
        swipe to the bottom of the page for ios device
        """
        try:

            i = 0
            findFlag = False
            skipFlag = False

            while (findFlag is False) and (skipFlag is False):

                beforeswipe = str(self.driver.page_source)
                beforeswipe_array = beforeswipe.split("XCUIElementTypeWindow")[2]

                width = self.driver.get_window_size()['width']
                height = self.driver.get_window_size()['height']
                startX = width / 2
                startY = (height / 4) * 3
                endX = startX
                endY = height / 4

                touch_action = TouchAction(self.driver)
                touch_action.long_press(x=startX, y=startY).move_to(x=endX, y=endY).release().perform()

                afterswipe = str(self.driver.page_source)
                afterswipe_array = afterswipe.split("XCUIElementTypeWindow")[2]

                if beforeswipe_array == afterswipe_array:
                    findFlag = True

                i = i + 1
                if (i > 30) and (findFlag is False):
                    skipFlag = True
                    raise AssertionError("Swipe 30 times, still not get the Top of the page, "
                                         "please check if the page is hang up")

        except Exception as exception:
            raise AssertionError("Get exception error when do swipe function, exception error as "
                                 + str(exception).format())

    def swipe_to_page_bottom_to_find_element_android(self, locator):
        """
        swipe up to page bottom to find the element - for android device
        :param locator: Tuple type like (By.ID, value)
        """
        try:

            i = 0
            exitFlag = False
            findFlag = False

            while (exitFlag is False) and (findFlag is False):

                existFlag = self.verify_object_exists(locator)
                if existFlag is True:
                    findFlag = True
                else:
                    findFlag = False

                if findFlag is False:

                    beforeswipe = str(self.driver.page_source)

                    width = self.driver.get_window_size()['width']
                    height = self.driver.get_window_size()['height']
                    startX = width / 2
                    startY = (height / 5) * 4
                    endX = startX
                    endY = (height / 10) * 3

                    touch_action = TouchAction(self.driver)
                    touch_action.long_press(x=startX, y=startY).move_to(x=endX, y=endY).release().perform()

                    afterswipe = str(self.driver.page_source)

                    if beforeswipe == afterswipe:
                        exitFlag = True
                        findFlag = False

                    i = i + 1
                    if i > 30:
                        exitFlag = True
                        findFlag = False

        except Exception as exception:
            raise AssertionError("Get exception error when do swipe function, exception error as "
                                 + str(exception).format())

        return findFlag

    def swipe_to_page_bottom_to_find_element_ios(self, locator):
        """
        swipe up to page bottom to find the element - for ios device
        :param locator: Tuple type like (By.ID, value)
        """
        try:

            i = 0
            exitFlag = False
            findFlag = False

            while (exitFlag is False) and (findFlag is False):

                existFlag = self.verify_object_exists(locator)
                if existFlag is True:
                    if self.driver.find_element(*locator).is_displayed():
                        findFlag = True
                    else:
                        findFlag = False
                else:
                    findFlag = False

                if findFlag is False:

                    beforeswipe = str(self.driver.page_source)
                    beforeswipe_array = beforeswipe.split("XCUIElementTypeWindow")[2]

                    width = self.driver.get_window_size()['width']
                    height = self.driver.get_window_size()['height']
                    startX = width / 2
                    startY = (height / 5) * 4
                    endX = startX
                    endY = (height / 10) * 3

                    touch_action = TouchAction(self.driver)
                    touch_action.long_press(x=startX, y=startY).move_to(x=endX, y=endY).release().perform()

                    afterswipe = str(self.driver.page_source)
                    afterswipe_array = afterswipe.split("XCUIElementTypeWindow")[2]

                    if beforeswipe_array == afterswipe_array:
                        exitFlag = True
                        findFlag = False

                    i = i + 1
                    if i > 30:
                        exitFlag = True
                        findFlag = False

        except Exception as exception:
            raise AssertionError("Get exception error when do swipe function, exception error as "
                                 + str(exception).format())

        return findFlag

    def swipe_to_page_top_to_find_element_android(self, locator):
        """
        swipe down to page top to find the element - for android device
        :param locator: Tuple type like (By.ID, value)
        """
        try:

            i = 0
            exitFlag = False
            findFlag = False

            while (exitFlag is False) and (findFlag is False):

                existFlag = self.verify_object_exists(locator)
                if existFlag is True:
                    findFlag = True
                else:
                    findFlag = False

                if findFlag is False:

                    beforeswipe = str(self.driver.page_source)

                    width = self.driver.get_window_size()['width']
                    height = self.driver.get_window_size()['height']
                    startX = width / 2
                    startY = (height / 10) * 3
                    endX = startX
                    endY = (height / 5) * 4

                    touch_action = TouchAction(self.driver)
                    touch_action.long_press(x=startX, y=startY).move_to(x=endX, y=endY).release().perform()

                    afterswipe = str(self.driver.page_source)

                    if beforeswipe == afterswipe:
                        exitFlag = True
                        findFlag = False

                    i = i + 1
                    if i > 30:
                        exitFlag = True
                        findFlag = False

        except Exception as exception:
            raise AssertionError("Get exception error when do swipe function, exception error as "
                                 + str(exception).format())

        return findFlag

    def swipe_to_page_top_to_find_element_ios(self, locator):
        """
        swipe down to page top to find the element - for ios device
        :param locator: Tuple type like (By.ID, value)
        """
        try:

            i = 0
            exitFlag = False
            findFlag = False

            while (exitFlag is False) and (findFlag is False):

                existFlag = self.verify_object_exists(locator)
                if existFlag is True:
                    if self.driver.find_element(*locator).is_displayed():
                        findFlag = True
                    else:
                        findFlag = False
                else:
                    findFlag = False

                if findFlag is False:

                    beforeswipe = str(self.driver.page_source)
                    beforeswipe_array = beforeswipe.split("XCUIElementTypeWindow")[2]

                    width = self.driver.get_window_size()['width']
                    height = self.driver.get_window_size()['height']
                    startX = width / 2
                    startY = (height / 10) * 3
                    endX = startX
                    endY = (height / 5) * 4

                    touch_action = TouchAction(self.driver)
                    touch_action.long_press(x=startX, y=startY).move_to(x=endX, y=endY).release().perform()

                    afterswipe = str(self.driver.page_source)
                    afterswipe_array = afterswipe.split("XCUIElementTypeWindow")[2]

                    if beforeswipe_array == afterswipe_array:
                        exitFlag = True
                        findFlag = False

                    i = i + 1
                    if i > 30:
                        exitFlag = True
                        findFlag = False

        except Exception as exception:
            raise AssertionError("Get exception error when do swipe function, exception error as "
                                 + str(exception).format())

        return findFlag

    def set_picker_wheel_value_ios(self, value, index=0):
        """
        set value for picker wheel in ios, only for the picker wheel support send_keys function.
        if not, suggest scroll_next_to_set_picker_wheel_value_ios or scroll_previous_to_set_picker_wheel_value_ios
        :param value: value want to be selected
        :param index: if more than one picker wheel displayed, need provide the index, start from 0
        """
        if value == '':
            raise AssertionError("Can not set picker wheel value as empty, please check test data")
        else:
            obj_pickwheel = self.driver.find_elements_by_xpath("//XCUIElementTypePickerWheel")
            if len(obj_pickwheel) > index:
                try:
                    obj_pickwheel.__getitem__(index).send_keys(value)
                except Exception:
                    raise AssertionError("Get errors when set picker wheel value, error is " + str(Exception).format())
            else:
                raise AssertionError("Wanted picker wheel field is not displayed on current page")

    def scroll_next_to_set_picker_wheel_value_ios(self,index=0):
        """
        scroll to select next value in current picker wheel
        :param index: if more than one picker wheel displayed, need provide the index, start from 0
        """
        obj_pickwheel = self.driver.find_elements_by_xpath("//XCUIElementTypePickerWheel")
        if len(obj_pickwheel) > index:
            try:
                params = {'order': 'next', 'offset': '0.15', "element": obj_pickwheel.__getitem__(index).id}
                self.driver.execute_script('mobile: selectPickerWheelValue', params)
            except Exception:
                raise AssertionError("Get errors when set picker wheel value, error is " + str(Exception).format())
        else:
            raise AssertionError("Wanted picker wheel field is not displayed on current page")

    def scroll_previous_to_set_picker_wheel_value_ios(self,index=0):
        """
        scroll to select next value in current picker wheel
        :param index: if more than one picker wheel displayed, need provide the index, start from 0
        """
        obj_pickwheel = self.driver.find_elements_by_xpath("//XCUIElementTypePickerWheel")
        if len(obj_pickwheel) > index:
            try:
                params = {'order': 'previous', 'offset': '0.15', "element": obj_pickwheel.__getitem__(index).id}
                self.driver.execute_script('mobile: selectPickerWheelValue', params)
            except Exception:
                raise AssertionError("Get errors when set picker wheel value, error is " + str(Exception).format())
        else:
            raise AssertionError("Wanted picker wheel field is not displayed on current page")
