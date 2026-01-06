import allure
import pytest
import time
import logging

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

logging.basicConfig(level=logging.INFO)


class StepExecutor:
    def __init__(self, driver):
        self.driver = driver  # Driver

    def execute_step(self, description: object, step_function: object, repeat_count: object = 1) -> object:
        """
        Executes a step exactly `repeat_count` times, even if the step succeeds.

        :param description: Step description
        :param step_function: Function that executes the step
        :param repeat_count: Number of repeats (optional, default is 1)
        """
        with allure.step(description):
            print(f"Starting step: {description}, repetitions: {repeat_count}")

            for i in range(repeat_count):
                try:
                    print(f"{description} - Attempt {i + 1}/{repeat_count}")
                    step_function()  # Call the passed function
                    allure.attach(
                        body=f"{description} - Success (Attempt {i + 1})",
                        name="Success",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    print(f"{description} - Success after attempt {i + 1}")
                except Exception as e:
                    print(f"{description} - Error after attempt {i + 1}: {e}")
                    allure.attach(
                        body=f"{description} - Error (Attempt {i + 1}): {e}",
                        name="Error",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    if i == repeat_count - 1:
                        pytest.fail(f"{description} - Error after {repeat_count} attempts: {e}")

                if i < repeat_count - 1:
                    print(f"{description} - Waiting before the next attempt...")
                    time.sleep(1)  # delay

            print(f"{description} - Completed {repeat_count} attempts.")

    def expand_notification_shade(self, hold_ms: int = 300, pull_percent: float = 0.85) -> None:
        """
        Expands the top notification bar with a gesture like a physical user:
            1) Long‑press at the top edge,
            2) Smoothly drag down.

        :param hold_ms: Time to hold the finger at the start (ms)
        :param pull_percent: How far to drag down (fraction of screen height, 0–1)
        """

        # Switch to the native context (when the app uses a WebView)
        try:
            if self.driver.current_context != "NATIVE_APP":
                self.driver.switch_to.context("NATIVE_APP")
        except Exception:
            pass

        # Screen size
        size = self.driver.get_window_size()
        width, height = size["width"], size["height"]

        start_x = width // 2
        start_y = max(1, int(height * 0.005))  # Very close to the top edge
        pull_percent = max(0.2, min(0.98, pull_percent))  # Range safeguard
        end_y = int(height * pull_percent)

        # W3C Actions with pointer type "touch" (string!)
        actions = ActionChains(self.driver)
        finger = PointerInput("touch", "finger")  # ← CHANGE: "touch" instead of PointerInput.TOUCH
        actions.w3c_actions = ActionBuilder(self.driver, finger)

        # Long‑press at the top
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(max(0.05, hold_ms / 1000.0))

        # Drag down and release
        actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
        actions.w3c_actions.pointer_action.release()

        actions.perform()

    def fast_scroll(self):
        """
        Instantly scrolls to the end of a scrollable view using the flingToEnd(3) method.
        :param driver: Appium driver object.
        """
        try:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiScrollable(new UiSelector().scrollable(true)).flingToEnd(3)'
            )
            print("Fast scroll to the end of the page completed.")
        except NoSuchElementException:
            print("Unable to scroll the page. Make sure the view is scrollable.")

    def scroll_page(self, scroll_percent=15, max_scrolls=15):
        """
        Scrolls the page down by a given percentage of the screen height
        until the end of the view is reached or the maximum number of scrolls is met.

        :param scroll_percent: Percentage of the screen height to scroll (e.g. 15 for 15%)
        :param max_scrolls: Maximum number of scroll attempts
        """
        try:
            size = self.driver.get_window_size()
            screen_height = size["height"]
            start_x = size["width"] // 2

            # Calculate scroll distance based on percentage
            scroll_distance = int(screen_height * (scroll_percent / 100))

            start_y = int(screen_height * 0.8)
            end_y = start_y - scroll_distance

            previous_page_source = ""

            for i in range(max_scrolls):
                current_page_source = self.driver.page_source

                if current_page_source == previous_page_source:
                    print(
                        f"Scrolling stopped – end of page reached after {i} scrolls."
                    )
                    break

                self.driver.swipe(
                    start_x,
                    start_y,
                    start_x,
                    end_y,
                    duration=200
                )
                print(f"Scroll {i + 1}: scrolled {scroll_percent}% of the screen height")

                previous_page_source = current_page_source
                time.sleep(0.5)

            time.sleep(1)

        except Exception as e:
            raise RuntimeError(f"Error while scrolling the page: {e}")

    def swipe_from_center_to_right(self, hold_ms: int = 100) -> None:
        """
        Simulates a finger swipe from the center of the screen to the right edge.

        :param hold_ms: Time to hold the finger before swiping (milliseconds)
        """
        size = self.driver.get_window_size()
        width, height = size["width"], size["height"]

        start_x = width // 2
        start_y = height // 2

        end_x = int(width * 0.95)
        end_y = start_y

        actions = ActionChains(self.driver)
        finger = PointerInput("touch", "finger")
        actions.w3c_actions = ActionBuilder(self.driver, finger)

        # Touch down in the center
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(max(0.05, hold_ms / 1000.0))

        # Swipe to the right
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()

        actions.perform()
