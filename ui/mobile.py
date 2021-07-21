# -*- coding: utf-8 -*-
from typing import Type
from appium.webdriver.webdriver import WebDriver
from ui.mobile_factory import StartAppiumDriver

driverManager = WebDriver


class DriverManagement(object):

    def __init__( self, platformvalue,parallelflag):

        self.parallel_flag = parallelflag
        self.platform_value = platformvalue

        obj_driver = StartAppiumDriver()

        if self.platform_value.lower() == 'ios':
            self.web_driver = obj_driver.get_appium_driver_ios()
        elif self.platform_value == 'android':
            self.web_driver = obj_driver.get_appium_driver_android()
        elif self.platform_value == 'mix':
            if self.parallel_flag == 'true':
                self.web_driver = obj_driver.get_appium_driver_mix()
            else:
                raise Exception("When set platform value as mix, parallel execution flag must be true")
        else:
            raise Exception("Parameter 'execution platform' value must be provided, "
                            "value should be ios or android or mix for appium execution,"
                            "value should be chrome or ie or other browser name if it is web testing")

        global driverManager

        try:
            if self.web_driver.session_id is None:
                raise Exception("Failed to initiate driver, execution break")
            else:
                driverManager = self.web_driver
        except Exception:
            raise Exception("Failed to initiate driver, execution break")

    @classmethod
    def set_up_mobile_driver_manage(cls,platform_value,parallel_flag):
        cls(platformvalue=platform_value,parallelflag=parallel_flag)


def get_current_mobile_driver() -> Type[WebDriver]:
    return driverManager

