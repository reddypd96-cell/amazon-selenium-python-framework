

import tempfile

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import config


class DriverFactory:

    @staticmethod
    def get_driver():

        browser = config.BROWSER.lower()

        if browser == "chrome":

            options = webdriver.ChromeOptions()

            
            if config.HEADLESS:
                options.add_argument("--headless=new")

          
            # desired Browser Options
         
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")

           
            options.add_argument("--disable-blink-features=AutomationControlled")

            options.add_experimental_option(
                "excludeSwitches",
                ["enable-automation"]
            )

            options.add_experimental_option(
                "useAutomationExtension",
                False
            )

           #password notifcation blocker
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
                "profile.default_content_setting_values.notifications": 2,
                "autofill.profile_enabled": False,
                "autofill.credit_card_enabled": False,
            }

            options.add_experimental_option("prefs", prefs)

            # ==========================
            # Fresh Chrome Profile per session (avoids profile lock crashes)
            # ==========================
            tmp_profile = tempfile.mkdtemp(prefix="selenium_chrome_")
            options.add_argument(f"--user-data-dir={tmp_profile}")

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )

         
            driver.execute_script("""
                Object.defineProperty(
                    navigator,
                    'webdriver',
                    {
                        get: () => undefined
                    }
                );
            """)

            driver.maximize_window()
            driver.implicitly_wait(config.IMPLICIT_WAIT)

            return driver

        elif browser == "firefox":

            options = webdriver.FirefoxOptions()

            if config.HEADLESS:
                options.add_argument("--headless")

            driver = webdriver.Firefox(options=options)

            driver.maximize_window()
            driver.implicitly_wait(config.IMPLICIT_WAIT)

            return driver

        elif browser == "edge":

            options = webdriver.EdgeOptions()

            if config.HEADLESS:
                options.add_argument("--headless=new")

            driver = webdriver.Edge(options=options)

            driver.maximize_window()
            driver.implicitly_wait(config.IMPLICIT_WAIT)

            return driver

        else:
            raise ValueError(f"Unsupported browser: {browser}")
