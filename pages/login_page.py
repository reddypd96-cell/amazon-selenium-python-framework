from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class LoginPage(BasePage):

    MOBILE_NUMBER_FIELD = (By.XPATH, "//input[@id='ap_email_login']")
    CONTINUE_BUTTON = (By.ID, "continue")
    PASSWORD_FIELD = (By.XPATH, "//input[@id='ap_password']")
    SIGN_IN_BUTTON = (By.ID, "signInSubmit")

    def enter_mobile_number(self, mobile_number):
        field = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.MOBILE_NUMBER_FIELD)
        )
        field.clear()
        field.send_keys(mobile_number)
        self.click(self.CONTINUE_BUTTON)
        return self

    def enter_password(self, password):
        field = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD)
        )
        field.clear()
        field.send_keys(password)
        self.click(self.SIGN_IN_BUTTON)

        from pages.home_page import HomePage
        return HomePage(self.driver)
