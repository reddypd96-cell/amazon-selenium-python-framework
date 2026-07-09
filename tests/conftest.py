import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from drivers.driver_factory import DriverFactory
from config import config


@pytest.fixture
def driver():
    drv = DriverFactory.get_driver()
    yield drv
    drv.quit()


@pytest.fixture(autouse=True)
def _attach_screenshot_on_failure(request, driver):
    yield
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        from pages.base_page import BasePage
        BasePage(driver).screenshot(request.node.name)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
