import os

from appium import webdriver
from selenium import webdriver as SeleniumDriver
from selenium.common.exceptions import NoAlertPresentException
from browsermobproxy import Server

from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager

from utils.logger import logger


class BrowserType:
    IE = "ie"
    FIREFOX = "firefox"
    HEADLESS_FIREFOX = "headless_firefox"
    CHROME = "chrome"
    HEADLESS_CHROME = "headless_chrome"
    CHROME_WEB_VIEW = "chrome_webview"
    ANDROID = "android"
    OPERA = "opera"
    SAFARI = "safari"
    EDGE = "edge"
    APPIUM = "appium"
    PHANTOMJS = "phantomjs"
    ZALENIUM = "zalenium"
    CHROME_WITH_PROXY = "chromewithproxy"
    HEADLESS_CHROME_WITH_PROXY = "headlesschromewithproxy"


class BrowserUserAgentType:
    safari_ios = "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
    android_browser = "--user-agent=Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
    chrome_mobile = "--user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    opera_mobile_blink_rendering_engine = "--user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-A310F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36 OPR/42.7.2246.114996"
    operaMobilePrestoRenderingEngine = "--user-agent=Opera/9.80 (Android 4.1.2; Linux; Opera Mobi/ADR-1305251841) Presto/2.11.355 Version/12.10"
    OperaMini = "--user-agent=Opera/9.80 (J2ME/MIDP; Opera Mini/5.1.21214/28.2725; U; ru) Presto/2.8.119 Version/11.10"
    Opera_Mini_iOS_WebKit = "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) OPiOS/10.2.0.93022 Mobile/11D257 Safari/9537.53"
    FirefoxAndroid = "--user-agent=Mozilla/5.0 (Android 7.0; Mobile; rv:54.0) Gecko/54.0 Firefox/54.0"
    Fire_fox_iOS = "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) FxiOS/7.5b3349 Mobile/14F89 Safari/603.2.4"
    UCBrowser = "--user-agent=Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G935F Build/NRD90M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.3.8.976 U3/0.8.0 Mobile Safari/534.30"
    Dolphin = "--user-agent=Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36"
    PuffinAndroid = "--user-agent=Mozilla/5.0 (Linux; Android 5.1.1; SM-N750K Build/LMY47X; ko-kr) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Puffin/6.0.8.15804AP"
    Puffin_iOS = "--user-agent=Mozilla/5.0 (Linux; Android 5.1.1; SM-N750K Build/LMY47X; ko-kr) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Puffin/6.0.8.15804AP"
    Samsung_Browser = "--user-agent=Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G955U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36"
    Yandex_Browser = "--user-agent=Mozilla/5.0 (Linux; Android 6.0; Lenovo K50a40 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.137 YaBrowser/17.4.1.352.00 Mobile Safari/537.36"
    MIUIBrowser = "--user-agent=Mozilla/5.0 (Linux; U; Android 7.0; en-us; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.0.3"
    IEMobile = "--user-agent=Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; Microsoft; Lumia 950)"
    EdgeMobile = "--user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.14977"
    BlackBerryBrowser = "--user-agent=Mozilla/5.0 (BB10; Kbd) AppleWebKit/537.35+ (KHTML, like Gecko) Version/10.3.3.2205 Mobile Safari/537.35+"


class Browser(object):
    def __init__(self, base_url, browser_type=BrowserType.CHROME, **browser_args):
        """
        To execute the scripts with different browsers
        :param base_url: url to automate
        :param browser_type: browser type for automation
        :param browser_args: browser arguments
        """
        docker_proxy_path = os.path.join("/app", "browsermob-proxy-2.1.4", "bin", "browsermob-proxy")
        local_proxy_path = "C:/Python38-32/libs/browsermob-proxy-2.1.4-bin/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"

        self.base_url = base_url
        browser_type_in_lower = browser_type.lower()
        if browser_type_in_lower == "ie":
            self.__browser_type = BrowserType.IE
            self.__web_driver = SeleniumDriver.Ie(**browser_args)
        elif browser_type_in_lower == "firefox" or browser_type_in_lower == "ff":
            self.__browser_type = BrowserType.FIREFOX
            # self.__web_driver = SeleniumDriver.Firefox(**browser_args)
            self.__web_driver = SeleniumDriver.Firefox(executable_path=GeckoDriverManager().install())
        elif browser_type_in_lower == "edge":
            self.__browser_type = BrowserType.EDGE
            self.__web_driver = SeleniumDriver.Edge(**browser_args)
            # self.__web_driver = SeleniumDriver.Edge(EdgeChromiumDriverManager().install())
        elif browser_type_in_lower == "headless_firefox":
            self.__browser_type = BrowserType.HEADLESS_FIREFOX
            options = SeleniumDriver.FirefoxOptions()
            options.add_argument('-headless')
            options.add_argument('window-size=1200x1300')  # optional
            self.__web_driver = SeleniumDriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_options=options)
        elif browser_type_in_lower == "chrome":
            self.__browser_type = BrowserType.CHROME
            # self.__web_driver = SeleniumDriver.Chrome(**browser_args)
            # To download the files into the current working directory
            options = SeleniumDriver.ChromeOptions()
            prefs = {'download.default_directory': os.getcwd()}
            options.add_experimental_option('prefs', prefs)
            # options.add_argument("--log-level=3")
            # options.add_experimental_option("excludeSwitches", ["enable-logging"])
            # self.__web_driver = SeleniumDriver.Chrome(**browser_args)
            self.__web_driver = SeleniumDriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
        elif browser_type_in_lower == "chromewithproxy":
            logger.info("use chromewithproxy")
            current_file_path = os.path.abspath(__file__)
            proxy_path = local_proxy_path
            logger.info("proxy_path=" + proxy_path)
            logger.info("chromewithproxy: instance proxy")
            # server = Server(proxy_path, options={'port': 9999})
            server = Server(proxy_path)
            logger.info("chromewithproxy: start proxy")
            server.start()
            logger.info("chromewithproxy: proxy is up")
            proxy = server.create_proxy(params={"trustAllServers": "true"})
            chrome_options = SeleniumDriver.ChromeOptions()
            chrome_options.add_argument("--ignore-certificate-errors");
            chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
            self.__web_driver = SeleniumDriver.Chrome(options=chrome_options)
            proxy.new_har('req', options={'captureHeaders': True, 'captureContent': True})
            self.chrome_proxy_server = server
            self.chrome_proxy = proxy
        elif browser_type_in_lower == "headlesschromewithproxy":
            logger.info("will use headlesschromewithproxy")
            current_file_path = os.path.abspath(__file__)
            logger.info("current_file_path=" + current_file_path)
            proxy_path = docker_proxy_path
            # proxy_path = local_proxy_path
            logger.info("proxy_path=cd  " + proxy_path)
            logger.info("headlesswithproxy: instance proxy")

            # server = Server(proxy_path, options={'port': 9999})
            server = Server(proxy_path)
            logger.info("headlesswithproxy: start browser proxy")
            # os.system("echo '.........'")
            # os.system("which python")
            # os.system("which java")
            # os.system("java -version")
            # os.system("echo ......... end")

            server.start()
            logger.info("headlesswithproxy: proxy is up")
            proxy = server.create_proxy(params={"trustAllServers": "true"})
            options = SeleniumDriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('window-size=1200x1300')  # optional
            options.add_argument("--ignore-certificate-errors");
            options.add_argument('--proxy-server={0}'.format(proxy.proxy))
            self.__web_driver = SeleniumDriver.Chrome(options=options)
            proxy.new_har('req', options={'captureHeaders': True, 'captureContent': True})
            self.chrome_proxy_server = server
            self.chrome_proxy = proxy
        elif browser_type_in_lower == "headless_chrome":
            self.__browser_type = BrowserType.HEADLESS_CHROME
            options = SeleniumDriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            # To download the files into the current working directory
            prefs = {'download.default_directory': os.getcwd()+'/home/jenkins/agent/workspace/backoffice/Promos/promo_mgr_integaration_tests/features'}
            options.add_experimental_option('prefs', prefs)
            options.add_argument('window-size=1300x1400')  # optional
            # if you want to run with different mobile emulation (webview) just change the browser user agent
            # if you want to run the headless browser with webview just uncomment below line
            # options.add_argument(BrowserUserAgentType.ChromeMobile)
            self.__web_driver = SeleniumDriver.Chrome(chrome_options=options)
        elif browser_type_in_lower == "chrome_webview":
            self.__browser_type = BrowserType.CHROME
            options = SeleniumDriver.ChromeOptions()
            # if you want to run with different mobile emulation (webview) just change the browser user agent
            options.add_argument(BrowserUserAgentType.chrome_mobile)
            self.__web_driver = SeleniumDriver.Ie(**browser_args)
            # self.__web_driver = SeleniumDriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        elif browser_type_in_lower == "android":
            self.__browser_type = BrowserType.ANDROID
            self.__web_driver = SeleniumDriver.Android(**browser_args)
        elif browser_type_in_lower == "opera":
            self.__browser_type = BrowserType.OPERA
            # self.__web_driver = SeleniumDriver.Opera(**browser_args)
            self.__web_driver = SeleniumDriver.Opera(executable_path=OperaDriverManager().install())
        elif browser_type_in_lower == "safari":
            self.__browser_type = BrowserType.SAFARI
            self.__web_driver = SeleniumDriver.Safari(**browser_args)
        elif browser_type_in_lower == "appium":
            self.__web_driver = webdriver.Remote(**browser_args)
        elif browser_type_in_lower == "phantomjs":
            self.__browser_type = BrowserType.PHANTOMJS
            self.__web_driver = SeleniumDriver.PhantomJS(**browser_args)
        elif browser_type_in_lower == "zalenium":
            self.__web_driver = webdriver.Remote(**browser_args)
        else:
            raise Exception("The browser type [%s] is not supported." % browser_type)

    def get_browser(self):
        """
        To get the specific browser
        :return: self
        """
        return self

    def get_webdriver(self):
        """
        To get the webdriver
        :return: webdriver
        """
        return self.__web_driver

    def get_browser_type(self):
        """
        To get the browser type
        :return: browser type
        """
        return self.__browser_type

    def start_session(self, desired_capabilities, browser_profile=None):
        """
        To start the session
        :param desired_capabilities: desired capabilities to start the session
        :param browser_profile: None
        """
        self.__web_driver.start_session(desired_capabilities, browser_profile)

    def set_page_load_timeout(self, timeout):
        """
        To set the page load timeout
        :param timeout: timeout seconds
        """
        self.__web_driver.set_page_load_timeout(timeout / 1000.0)

    def set_script_timeout(self, time_to_wait):
        """
        To set the script timeout
        :param time_to_wait: time to do the wait
        """
        self.__web_driver.set_script_timeout(time_to_wait / 1000.0)

    def set_wait_element_interval(self, interval):
        """
        To set wait for the element interval
        :param interval: interval time
        """
        self.__wait_element_interval = interval

    def get_wait_element_interval(self):
        """
        To get wait for the element interval
        :return: interval time
        """
        return self.__wait_element_interval

    def set_wait_element_timeout(self, timeout):
        """
        Do set the element smart wait
        :param timeout: timeout seconds
        """
        self.__wait_element_timeout = timeout

    def get_wait_element_timeout(self):
        """
        Do get wait for an element
        :return:
        """
        return self.__wait_element_timeout

    def execute_script(self, script, *args):
        return self.__web_driver.execute_script(script, *args)

    def execute_async_script(self, script, *args):
        return self.__web_driver.execute_async_script(script, *args)

    def open(self, url):
        self.__web_driver.get(url)

    def get_title(self):
        return self.__web_driver.title

    def get_page_source(self):
        return self.__web_driver.page_source

    def back(self):
        self.__web_driver.back()

    def forward(self):
        self.__web_driver.forward()

    def refresh(self):
        self.__web_driver.refresh()

    def quit(self):
        self.__web_driver.quit()

    def maximize_window(self):
        """
        To maximize window
        """
        self.__web_driver.maximize_window()

    def get_current_url(self):
        """
        To get the current url
        :return: current url
        """
        return self.__web_driver.current_url

    def switch_to_frame(self, frame_reference):
        """
        To switch to iframe
        :param frame_reference: frame reference to switch
        """
        self.__web_driver.switch_to.frame(frame_reference)

    def switch_to_parent_frame(self):
        """
        To switch to the parent frame
        """
        self.__web_driver.switch_to.parent_frame()

    def switch_to_default_content(self):
        """To switch back to the default content"""
        self.__web_driver.switch_to.default_content()

    def get_alert(self):
        """
        To get the alert
        :return: switch to alert
        """
        return self.__web_driver.switch_to.alert

    def is_alert_present(self):
        """
        To verify alert present or not
        :return: true or false
        """
        try:
            alert = self.__web_driver.switch_to.alert
            return True
        except NoAlertPresentException:
            return False

    # def wait_for_alert_present(self):
    #     Utils.wait_for(self.is_alert_present)

    def get_cookies(self):
        """
        To get the cookies
        :return: cookies
        """
        return self.__web_driver.get_cookies()

    def get_cookie(self, name):
        """
        To get the cookies by name
        :param name: name of the cookie
        :return: cookie by name
        """
        return self.__web_driver.get_cookie(name)

    def delete_cookie(self, name):
        """
        To delete a cookie
        :param name: name to delete the cookie
        """
        self.__web_driver.delete_cookie(name)

    def delete_all_cookies(self):
        """
        To delete all cookies
        """
        self.__web_driver.delete_all_cookies()

    def add_cookie(self, cookie_dict):
        """
        To add a cookie
        :param cookie_dict: cookie dictionary to add
        """
        self.__web_driver.add_cookie(cookie_dict)

    def get_desired_capabilities(self):
        """
        To get the desired capabilities
        :return: desired capabilities
        """
        return self.__web_driver.desired_capabilities

    def get_screen_shot_as_file(self, filename):
        """
        To get the screen shot in a file
        :param filename: filename to store the screenshot
        :return: file name
        """
        return self.__web_driver.get_screenshot_as_file(filename)

    def get_screen_shot_as_png(self):
        """
        To get the screen shot as png
        :return: screen shot png
        """
        return self.__web_driver.get_screenshot_as_png()

    def get_screen_shot_as_base64(self):
        """
        To get the screen shot as base 64
        :return: screen shot as base 64
        """
        return self.__web_driver.get_screenshot_as_base64()

    save_screen_shot = get_screen_shot_as_file

    def get_current_window_handle(self):
        """
        To get the current window handle
        :return: current window handle
        """
        return self.__web_driver.current_window_handle

    def get_window_handles(self):
        """
        To get the current window handles
        :return: current window handles
        """
        return self.__web_driver.window_handles

    def switch_to_window(self, window_reference):
        """
        To switch to the window
        :param window_reference: window preference to switch
        """
        self.__web_driver.switch_to.window(window_reference)

    def close_window(self, window_reference="current"):
        """
        To closed the current window
        :param window_reference: current window reference
        """
        if window_reference == "current":
            self.__web_driver.close()
        else:
            current_window = self.get_current_window_handle()
            self.switch_to_window(window_reference)
            self.__web_driver.close()
            self.switch_to_window(current_window)

    def set_window_size(self, width, height, window_reference="current"):
        """
        To set the window size
        :param width: width of the window
        :param height: height of the window
        :param window_reference: current window
        """
        self.__web_driver.set_window_size(width, height, window_reference)

    def get_window_size(self, window_reference="current"):
        """
        To get the window size
        :param window_reference: current window
        :return: current window size
        """
        return self.__web_driver.get_window_size(window_reference)

    def set_window_position(self, x, y, window_reference="current"):
        """
        To set the window position
        :param x: x co-ordinates of the current window
        :param y: y co-ordinates of the current window
        :param window_reference: current window
        """
        self.__web_driver.set_window_position(x, y, window_reference)

    def get_window_position(self, window_reference="current"):
        """
        To get the current window position
        :param window_reference: current window
        :return: window position
        """
        return self.__web_driver.get_window_position(window_reference)

    def get_orientation(self):
        """
        To get the orientation
        :return: orientation
        """
        return self.__web_driver.orientation

    def set_orientation(self, value):
        """
        To set the orientation
        :param value: to set the orientation
        """
        self.__web_driver = value

    def get_application_cache(self):
        """
        To get the application cache
        :return: application cache
        """
        return self.__web_driver.application_cache

    def get_log_types(self):
        """
        To get the log types
        :return: log types
        """
        return self.__web_driver.log_types

    def get_log(self, log_type):
        """
        To get the logs
        :param log_type:log type to get
        :return:
        """
        return self.__web_driver.get_log(log_type)

    def switch_to_context(self, name):
        """
        To switch to the context
        :param name: name of the context
        :return: current context
        """
        self.__web_driver._switch_to.context(name)
        return self.__web_driver.current_context

    def scroll_to(self, from_location=0, to_location=0):
        """
        To scroll to specific location
        :param from_location:
        :param to_location:
        :return:
        """
        self.__web_driver.execute_script("window.scrollTo({}, {});".format(from_location, to_location))

    def scroll_down(self):
        # SeleniumUtils.scroll_to_direction(self._selenium_context(), "Down")

        self.scroll_to(0, self.__web_driver.get_window_size('current'))

    def __str__(self):
        return "Browser [WebDriver: %s][SessionId: %s]" % (self.__web_driver.name, self.__web_driver.session_id)
