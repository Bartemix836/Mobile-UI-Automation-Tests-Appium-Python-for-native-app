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
@allure.feature("Test case 02 - change view for 'Simple' and entry to Assests section ")
@allure.story("Run installed app")
def test_TC_02_change_view(driver_setup):
    driver = driver_setup

    click_actions = ClickActions(driver)
    step_executor = StepExecutor(driver)
    element_assertions = ElementAssertions(driver)

    # STEP 1: Change view for Exchange
    step_executor.execute_step("STEP 1: Change view mode",
            lambda: click_actions.click_element('new UiSelector().resourceId("com.okinc.okex.gp:id/chip_container")'))
    time.sleep(2)

    # STEP 2: Select Simple view
    step_executor.execute_step("STEP 2: Select Simple view",
            lambda: click_actions.click_element('new UiSelector().resourceId("com.okinc.okex.gp:id/icon").instance(0)'))
    time.sleep(7)

    # Assertion - checking if is actived Simple view:
    step_executor.execute_step(" Assertion - checking if is actived Simple view:",
            lambda: element_assertions.is_element_visible('new UiSelector().resourceId("com.okinc.okex.gp:id/mode_name").text("Simple")'))
    time.sleep(3)

    # STEP 3: Scroll down page 1/3 page
    step_executor.execute_step("STEP 3: Scroll down page 1/3 page",
                               lambda: step_executor.scroll_page(7,5))
    time.sleep(3)

    # STEP 4: Select All assests section
    step_executor.execute_step("STEP 4: Select All assests section",
            lambda: click_actions.click_element('new UiSelector().resourceId("com.okinc.okex.gp:id/filter_chip_layout").instance(1)'))
    time.sleep(3)

    # STEP 5: Click 'View all' button:
    step_executor.execute_step("STEP 5: Click 'View all' button:",
            lambda: click_actions.click_element('new UiSelector().resourceId("com.okinc.okex.gp:id/view_all_btn")'))
    time.sleep(3)

    # Assertion - checking if is actived Assets section:
    step_executor.execute_step("Assertion - checking if is actived Assets section:",
            lambda: element_assertions.is_element_visible('new UiSelector().resourceId("com.okinc.okex.gp:id/header_title").text("Assets")'))
    time.sleep(3)

    # STEP 6: Overview app
    step_executor.execute_step("STEP 6: Close app",
            lambda: driver.press_keycode(187))
    time.sleep(1)


    # STEP 7: Move view from middle to right:
    step_executor.execute_step("STEP 7: Move view from middle to right:",
            lambda: step_executor.swipe_from_center_to_right())
    time.sleep(1)


    # STEP 8: Click 'Clear all' button:
    step_executor.execute_step("STEP 8: Click 'Clear all' button: ",
            lambda: click_actions.click_element('new UiSelector().resourceId("com.google.android.apps.nexuslauncher:id/clear_all")'))
    time.sleep(1)

    allure.attach(body="Test case 02 - change view for 'Simple' and entry to Assests section", name="Test report", attachment_type=allure.attachment_type.TEXT)
