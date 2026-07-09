from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from config import config


class HomePage(BasePage):

    SEARCH_BOX = (By.ID, "twotabsearchtextbox")
    SEARCH_BUTTON = (By.ID, "nav-search-submit-button")
    ACCOUNT_LIST_LINK = (By.ID, "nav-link-accountList")

    def load(self):
        self.open(config.BASE_URL)
        return self

    def go_to_sign_in(self):
        account = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.ACCOUNT_LIST_LINK)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", account
        )
        try:
            account.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", account)

        WebDriverWait(self.driver, 20).until(
            lambda d: "/ap/" in d.current_url.lower()
        )

        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    def search_for(self, term):
        self.type_text(self.SEARCH_BOX, term)
        self.click(self.SEARCH_BUTTON)

        from pages.search_results_page import SearchResultsPage
        return SearchResultsPage(self.driver)
