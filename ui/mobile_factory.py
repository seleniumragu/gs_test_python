import os
from appium import webdriver
from configs.config_mobile import ConfigMobile
from utils.configuration_mobile import get_parallel_flag, get_platform, get_device_name
from utils.work_id_process import get_work_id


class StartAppiumDriver(object):

    def get_appium_driver_ios(self):

        self.__appiumURL = get_appium_address_value()
        self.__bundleid = ConfigMobile.ios_bundle_id
        self.__xcode_originid = ConfigMobile.xcode_or_id
        self.__jenkinsFlag = ConfigMobile.jenkins_execution_flag
        self.__apppath = get_app_install_path_ios(self.__jenkinsFlag)
        self.__devicename = get_device_name_ios()
        self.__udid = get_device_udid_ios()
        self.__deviceos = get_device_os_ios()
        self.__wdaport = get_wda_value()

        self.__web_driver = invoke_ios_driver(self.__appiumURL, self.__devicename,self.__udid, self.__deviceos,
                                              self.__xcode_originid, self.__bundleid, self.__apppath, self.__wdaport)

        return self.__web_driver


    def get_appium_driver_android(self):

        self.__appiumURL = get_appium_address_value()
        self.__packagename = ConfigMobile.application_package_name
        self.__activityname = ConfigMobile.application_main_activity_name
        self.__jenkinsFlag = ConfigMobile.jenkins_execution_flag
        self.__apppath = get_app_install_path_android(self.__jenkinsFlag)
        self.__systemport = get_system_port()
        self.__devicename = get_device_name_android()
        self.__udid = get_device_udid_android()
        self.__deviceos = get_device_os_android()

        self.__web_driver = invoke_android_driver(self.__appiumURL, self.__devicename, self.__udid, self.__deviceos, self.__packagename ,
                                                  self.__activityname, self.__apppath, self.__systemport)

        return self.__web_driver

    def get_appium_driver_mix(self):

        #for mix type parallel execution, default to select device one to do the execution, android device in process one, ios device in process 2
        if get_work_id() == 1:

            self.__appiumURL = ConfigMobile.appium_url_address_parallel_one
            self.__udid = ConfigMobile.android_device_udid_one
            self.__devicename = ConfigMobile.android_device_name_one
            self.__deviceos = ConfigMobile.android_device_os_one
            self.__packagename = ConfigMobile.application_package_name
            self.__activityname = ConfigMobile.application_main_activity_name
            self.__jenkinsFlag = ConfigMobile.jenkins_execution_flag
            self.__apppath = get_app_install_path_android(self.__jenkinsFlag)
            self.__systemport = get_system_port()

            self.__web_driver = invoke_android_driver(self.__appiumURL, self.__devicename, self.__udid, self.__deviceos,
                                                      self.__packagename,
                                                      self.__activityname, self.__apppath, self.__systemport)

        elif get_work_id() == 2:

            self.__appiumURL = ConfigMobile.appium_url_address_parallel_two
            self.__wdaport = get_wda_value()
            self.__udid = ConfigMobile.ios_device_udid_one
            self.__devicename = ConfigMobile.ios_device_name_one
            self.__deviceos = ConfigMobile.ios_device_os_one
            self.__bundleid = ConfigMobile.ios_bundle_id
            self.__xcode_originid = ConfigMobile.xcode_or_id
            self.__jenkinsFlag = ConfigMobile.jenkins_execution_flag
            self.__apppath = get_app_install_path_ios(self.__jenkinsFlag)

            self.__web_driver = invoke_ios_driver(self.__appiumURL, self.__devicename, self.__udid, self.__deviceos,
                                                  self.__xcode_originid, self.__bundleid, self.__apppath,
                                                  self.__wdaport)

        else:
            raise Exception("Currently framework is design to support 2 mobile device parallel execution,"
                            "can not support more than 2 mobile devices")

        return self.__web_driver


def invoke_ios_driver(appiumurl,devicename,deviceudid,deviceos,xcode_originid,bundleid,app_path,wdaport):

    desired_caps = {}
    desired_caps['automationName'] = "XCUITest"
    desired_caps['platformName'] = "iOS"
    desired_caps['newCommandTimeout'] = 600
    desired_caps['startIWDP'] = True
    desired_caps['locationServicesEnabled'] = True
    desired_caps['noReset'] = False
    desired_caps['useNewWDA'] = True
    desired_caps['xcodeSigningId'] = "iPhone Developer"
    desired_caps['deviceName'] = devicename
    desired_caps['udid'] = deviceudid
    desired_caps['platformVersion'] = deviceos
    desired_caps['xcodeOrgId'] = xcode_originid
    desired_caps['bundleId'] = bundleid
    desired_caps['app'] = app_path
    desired_caps['wdaLocalPort'] = wdaport

    try:
        web_driver = webdriver.Remote(appiumurl, desired_caps)
    except Exception:
        raise Exception("Failed to start ios driver with appium address " + appiumurl)

    return web_driver


def invoke_android_driver(appiumurl,devicename,deviceudid,deviceos,packagename,activityname,app_path,systemport):

    desired_caps = {}
    desired_caps['automationName'] = "UiAutomator2"
    desired_caps['platformName'] = "Android"
    desired_caps['newCommandTimeout'] = 480
    desired_caps['noReset'] = False
    desired_caps['noSign'] = True
    desired_caps['unicodeKeyboard'] = True
    desired_caps['deviceName'] = devicename
    desired_caps['udid'] = deviceudid
    desired_caps['platformVersion'] = deviceos
    desired_caps['appPackage'] = packagename
    desired_caps['appActivity'] = activityname
    desired_caps['app'] = app_path
    desired_caps['systemPort'] = systemport


    try:
        web_driver = webdriver.Remote(appiumurl, desired_caps)
    except Exception:
        raise Exception("Failed to start android driver with appium address " + appiumurl)

    return web_driver


def get_app_install_path_android(jenkinsflag):

    app_path = ''
    package_name = ''
    try:
        if jenkinsflag == 'true':

            root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            file_path = os.path.abspath(os.path.join(root_path, '/iherb_automation/package'))

            Files = os.listdir(file_path)
            if len(Files) > 0:
                i = 0
                for k in range(len(Files)):
                    file_name = Files[k]
                    Files[k] = os.path.splitext(Files[k])[1]
                    str_value = '.apk'
                    if str_value in Files[k]:
                        package_name = file_name
                        i = i + 1

                if i == 1:
                    app_path = os.path.abspath(os.path.join(file_path, package_name))
                else:
                    raise Exception("More than one tested app found under package folder")

            else:
                raise Exception("Tested app is not found under package folder, please check")

        else:
            app_path = ConfigMobile.application_install_path_android
            if app_path == '':
                pass
            else:
                if os.path.exists(app_path):
                    pass
                else:
                    raise Exception("Stop execution, no tested app found per provided path " + app_path)
    except Exception:
        raise Exception("Get exception when get app install path, "
                        "need confirm if package folder exist when use jenkins execution flag as true")

    return app_path


def get_app_install_path_ios(jenkinsflag):

    app_path = ''
    package_name = ''
    try:
        if jenkinsflag == 'true':

            root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            file_path = os.path.abspath(os.path.join(root_path, '/iherb_automation/package'))

            Files = os.listdir(file_path)
            if len(Files) > 0:
                i = 0
                for k in range(len(Files)):
                    file_name = Files[k]
                    Files[k] = os.path.splitext(Files[k])[1]
                    str_value = '.ipa'
                    if str_value in Files[k]:
                        package_name = file_name
                        i = i + 1

                if i == 1:
                    app_path = os.path.abspath(os.path.join(file_path, package_name))
                else:
                    raise Exception("More than one tested app found under package folder")

            else:
                raise Exception("Tested app is not found under package folder, please check")

        else:

            app_path = ConfigMobile.application_install_path_ios
            if app_path == '':
                pass
            else:
                if os.path.exists(app_path):
                    pass
                else:
                    raise Exception("Stop execution, no tested app found per provided path " + app_path)

    except Exception:
        raise Exception("Get exception when get app install path, "
                        "need confirm if package folder exist when use jenkins execution flag as true")

    return app_path


def get_appium_address_value():
    if get_parallel_flag() == 'true':
        if get_work_id() == 1:
            appium_address = ConfigMobile.appium_url_address_parallel_one
        elif get_work_id() == 2:
            appium_address = ConfigMobile.appium_url_address_parallel_two
        else:
            raise Exception("Currently framework is design to support 2 mobile device parallel execution,"
                        "can not support more than 2 mobile devices")
    elif get_parallel_flag() == 'false':
        if get_platform() == "ios":
            appium_address = ConfigMobile.appium_url_address_ios
        else:
            appium_address = ConfigMobile.appium_url_address_android
    else:
        raise Exception("Parallel execution flag value is incorrect, it must be true or false")

    return appium_address


def get_device_name_ios():

    if get_parallel_flag() == 'true':

        if get_work_id() == 1:
            devicename = ConfigMobile.ios_device_name_one
        elif get_work_id() == 2:
            devicename = ConfigMobile.ios_device_name_two
        else:
            raise Exception("Currently framework is design to support 2 mobile device parallel execution,"
                            "can not support more than 2 mobile devices")
    else:
        if (get_device_name() == 'deviceone') or (get_device_name() == 'device1'):
            devicename = ConfigMobile.ios_device_name_one
        else:
            devicename = ConfigMobile.ios_device_name_two

    return devicename


def get_device_udid_ios():

    if get_parallel_flag() == 'true':

        if get_work_id() == 1:
            device_udid = ConfigMobile.ios_device_udid_one
        elif get_work_id() == 2:
            device_udid = ConfigMobile.ios_device_udid_two
        else:
            raise Exception("Currently framework is design to support 2 mobile device parallel execution,"
                            "can not support more than 2 mobile devices")
    else:
        if (get_device_name() == 'deviceone') or (get_device_name() == 'device1'):
            device_udid = ConfigMobile.ios_device_udid_one
        else:
            device_udid = ConfigMobile.ios_device_udid_two

    return device_udid



def get_device_os_ios():

    if get_parallel_flag() == 'true':

        if get_work_id() == 1:
            device_os = ConfigMobile.ios_device_os_one
        elif get_work_id() == 2:
            device_os = ConfigMobile.ios_device_os_two
        else:
            raise Exception("Currently framework is design to support 2 mobile device parallel execution,"
                            "can not support more than 2 mobile devices")
    else:
        if (get_device_name() == 'deviceone') or (get_device_name() == 'device1'):
            device_os = ConfigMobile.ios_device_os_one
        else:
            device_os = ConfigMobile.ios_device_os_two

    return device_os


def get_wda_value():

    if get_parallel_flag() == 'true':
        work_value = 8100 + get_work_id()
    elif get_parallel_flag() == 'false':
        work_value = 8100
    else:
        raise Exception("Parallel execution flag value is incorrect, it must be true or false")

    return work_value



def get_system_port():

    if get_parallel_flag() == 'true':
        system_port = 8201 + get_work_id()
    elif get_parallel_flag() == 'false':
        system_port = 8200
    else:
        raise Exception("Parallel execution flag value is incorrect, it must be true or false")

    return system_port


def get_device_name_android():

    if get_parallel_flag() == 'true':

        if get_work_id() == 1:
            devicename = ConfigMobile.android_device_name_one
        elif get_work_id() == 2:
            devicename = ConfigMobile.android_device_name_two
        else:
            raise Exception("Currently framework is design to support 2 mobile device parallel execution,"
                            "can not support more than 2 mobile devices")
    else:
        if (get_device_name() == 'deviceone') or (get_device_name() == 'device1'):
            devicename = ConfigMobile.android_device_name_one
        else:
            devicename = ConfigMobile.android_device_name_two

    return devicename



def get_device_udid_android():

    if get_parallel_flag() == 'true':

        if get_work_id() == 1:
            device_udid = ConfigMobile.android_device_udid_one
        elif get_work_id() == 2:
            device_udid = ConfigMobile.android_device_udid_two
        else:
            raise Exception("Currently framework is design to support 2 mobile device parallel execution,"
                            "can not support more than 2 mobile devices")
    else:
        if (get_device_name() == 'deviceone') or (get_device_name() == 'device1'):
            device_udid = ConfigMobile.android_device_udid_one
        else:
            device_udid = ConfigMobile.android_device_udid_two

    return device_udid


def get_device_os_android():

    if get_parallel_flag() == 'true':

        if get_work_id() == 1:
            device_os = ConfigMobile.android_device_os_one
        elif get_work_id() == 2:
            device_os = ConfigMobile.android_device_os_two
        else:
            raise Exception("Currently framework is design to support 2 mobile device parallel execution,"
                            "can not support more than 2 mobile devices")
    else:
        if (get_device_name() == 'deviceone') or (get_device_name() == 'device1'):
            device_os = ConfigMobile.android_device_os_one
        else:
            device_os = ConfigMobile.android_device_os_two

    return device_os
