# -*- coding: utf-8 -*-


class BrowserManager(object):
    browsers = []

    def add_browser_queue(self, browser):
        self.browsers.append(browser)

    def get_browser(self, index=-1):
        return self.browsers[index]

    def clear_browsers(self):
        for browser in self.browsers[::-1]:
            try:
                browser.quit()
            except Exception:  # Ignore errors while closing browser
                pass
            else:
                self.browsers.pop()

        # BrowserManager.browsers.clear()
