import os
import sys
import time
import allure
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.driver_setup import create_driver
from core.click_actions import ClickActions
from core.step_executor import StepExecutor
from core.element_assertions import ElementAssertions



@pytest.fixture(scope="function")
#Running app
def driver_setup():
    driver = create_driver()
    yield driver
    try:
        driver.quit()
    except Exception:
        pass


@pytest.mark.order(1)
@allure.feature("Test case 01 - run app ")
@allure.story("Run installed app")
def test_TC_01_run_apps(driver_setup):
    driver = driver_setup

    click_actions = ClickActions(driver)
    step_executor = StepExecutor(driver)
    element_assertions = ElementAssertions(driver)

    # STEP 1: Change view for Exchange
    step_executor.execute_step("STEP 1: Change view for Exchange",
            lambda: click_actions.click_element('new UiSelector().resourceId("com.okinc.okex.gp:id/chip_container")'))
    time.sleep(2)

    # STEP 2: Select Exchange view
    step_executor.execute_step("STEP 2: Select Exchange view",
            lambda: click_actions.click_element('new UiSelector().description("tradeAdvanceModeOptionId")'))
    time.sleep(7)

    # Assertion - checking if is actived Exchane view:
    step_executor.execute_step(" Assertion - checking if is actived Exchane view:",
            lambda: element_assertions.is_element_visible('new UiSelector().resourceId("com.okinc.okex.gp:id/mode_name").text("Exchange")'))
    time.sleep(2)


    allure.attach(body="Test case 01 - run app ", name="Test report", attachment_type=allure.attachment_type.TEXT)
