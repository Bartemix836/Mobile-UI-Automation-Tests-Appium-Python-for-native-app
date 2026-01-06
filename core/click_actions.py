from appium.webdriver.common.appiumby import AppiumBy
import time
import logging
from selenium.common.exceptions import TimeoutException, UnknownMethodException
from selenium.common.exceptions import ElementClickInterceptedException
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.INFO)


class ClickActions:
    def __init__(self, driver):
        self.driver = driver  # Driver

    def click_element(self, selector):
        # Using the driver defined in the class
        element = WebDriverWait(self.driver, 200).until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, selector))
        )
        element.click()

    def click_element_radion(self, selector):
        try:
            element = WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, selector))
            )
            time.sleep(1)
            element.click()
        except Exception as e:
            print(f"Error click element: {e}")
            raise e

    def press_enter_twice(self):
        try:
            # First Enter key press (keycode 66 corresponds to Enter)
            self.driver.press_keycode(66)
            print("First Enter key press performed.")
            time.sleep(1)
            # Second Enter key press (keycode 66 corresponds to Enter)
            self.driver.press_keycode(66)
            print("Second Enter key press performed.")

        except Exception as e:
            print(f"Error while simulating Enter key press: {e}")

    def press_enter_3times(self):
        try:
            # First Enter key press (keycode 66)
            self.driver.press_keycode(66)
            print("First Enter key press performed.")
            time.sleep(1)

            # Press Down arrow (keycode 20)
            self.driver.press_keycode(20)
            print("Down arrow key press performed.")
            time.sleep(1)

            # Second Enter key press
            self.driver.press_keycode(66)
            print("Second Enter key press performed.")

        except Exception as e:
            print(f"Error while simulating key presses: {e}")

    def press_enter_arrow_down_enter(self):
        try:
            # First Enter key press
            self.driver.press_keycode(66)
            print("First Enter key press performed.")
            time.sleep(1)

            # Press Down arrow
            self.driver.press_keycode(20)
            print("Down arrow key press performed.")
            time.sleep(1)

            # Second Enter key press
            self.driver.press_keycode(66)
            print("Second Enter key press performed.")

        except Exception as e:
            print(f"Error while simulating key sequence: {e}")

    def press_enter_esc(self):
        try:
            # Press ESC (only once)
            self.driver.press_keycode(111)
            print("ESC key press performed.")

        except Exception as e:
            print(f"Error while simulating key sequence: {e}")

    def press_down_and_enter(self):
        """Presses Down arrow, then Enter."""
        pyautogui.press('down')
        time.sleep(0.2)
        pyautogui.press('enter')

    def press_enter_key(self):
        """
        Simulates pressing the 'Enter' key or 'checkmark' on the virtual keyboard.
        """
        # Keycode 66 corresponds to the 'Enter' key on Android
        self.driver.press_keycode(66)

    def click_elemet_radiobtnYES(self):
        # Creating UiAutomator selector
        selector = 'new UiSelector().resourceId("UIpath selector'

        try:
            clickable_element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, selector))
            )
            clickable_element.click()
            print(f"Clicked radio-button YES: {selector}")

        except TimeoutException:
            logging.error(f"Timeout: Failed to find or click the element within the allocated time.")
        except ElementClickInterceptedException as e:
            logging.error(f"Element could not be clicked because the click was intercepted: {e}")
        except Exception as e:
            logging.error(f"Error while clicking the element: {e}")
            raise e

