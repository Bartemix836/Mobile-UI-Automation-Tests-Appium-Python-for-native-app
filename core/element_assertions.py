from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.INFO)


class ElementAssertions:
    def __init__(self, driver):
        self.driver = driver

    def is_element_visible(self, selector):
        """
        Checks whether the element indicated by the selector is visible.

        :param selector: Element selector (e.g. UiSelector for Appium)
        :return: True if the element is visible; False otherwise
        """
        try:
            element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)
            return element.is_displayed()
        except Exception:
            return False

    def verify_error_message(self, expected_message, timeout=10):
        """
        Verifies an error message.

        :param expected_message: Expected fragment of the error message
        :param timeout: Maximum wait time in seconds
        """
        try:
            error_element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//android.widget.TextView[contains(@text, 'Niepoprawny format kodu')]")
                )
            )
            error_text = error_element.text

            if expected_message in error_text:
                print(f"Error message matches: {error_text}")
            else:
                raise AssertionError(
                    f"Expected: '{expected_message}', but got: '{error_text}'"
                )

        except Exception as e:
            print(f"No error message found. Expected: '{expected_message}', error: {e}")
            return False

        return True

    def check_text_on_page(self, expected_text):
        """Checks whether the given text is present in the target element."""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.ID, "UIpath selector"))
            )
            actual_text = element.text.strip()

            if actual_text == expected_text:
                print(f"User changed: {actual_text}")
            else:
                raise AssertionError(
                    f"Expected '{expected_text}', but found '{actual_text}'"
                )

        except Exception as e:
            raise AssertionError(f"Element not found or other error: {e}")

    def check_text_in_element(self, expected_text):
        """Checks whether the given text is present in the element."""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "UIpath selector"))
            )

            actual_text = element.text.strip()

            if expected_text == actual_text:
                print(f"User changed: '{actual_text}'")
            else:
                raise AssertionError(
                    f"Expected '{expected_text}', but found '{actual_text}'"
                )

        except Exception as e:
            raise AssertionError(f"Element not found or other error: {e}")

    def check_element_by_xpath(self, xpath: str):
        """Checks whether an element with the given XPATH exists."""
        try:
            elements = self.driver.find_elements(AppiumBy.XPATH, xpath)
            if elements:
                print(f"Element with XPATH '{xpath}' was found.")
                return True
            else:
                raise AssertionError(f"Element with XPATH '{xpath}' was not found.")
        except Exception as e:
            raise AssertionError(f"Error while searching for XPATH '{xpath}': {e}")

    def check_text_content_desc(self, text):
        """Checks whether an element with the given content-desc exists."""
        try:
            elements = self.driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().descriptionContains("{text}")'
            )
            if elements:
                print(f"Text '{text}' was found on the page.")
                return True
            else:
                raise AssertionError(f"Text '{text}' was not found on the page.")
        except Exception as e:
            raise AssertionError(f"Error while searching for text '{text}': {e}")

    def check_today_date_in_text(self):
        """Checks whether today's date (DD.MM.YYYY) is present in any text element."""
        try:
            today = datetime.now().strftime("%d.%m.%Y")
            elements = self.driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().textContains("{today}")'
            )
            if elements:
                print(f"Date '{today}' was found in element text.")
                return True
            else:
                raise AssertionError(f"Date '{today}' was not found in element text.")
        except Exception as e:
            raise AssertionError(f"Error while searching for date '{today}': {e}")

    def check_text_content_descF(self, text):
        """Checks whether an element with the given content-desc exists (non-failing)."""
        try:
            elements = self.driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().descriptionContains("{text}")'
            )
            if elements:
                print(f"Text '{text}' was found on the page.")
                return True
            else:
                print(f"Text '{text}' was not found, but this is an expected result.")
                return False
        except Exception as e:
            print(f"Error while searching for text '{text}': {e}")
            return False

    def check_and_click_checkbox(self):
        """Checks checkbox state and clicks it if not selected."""
        checkbox = self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Jestem członkiem OFE/mam subkonto")'
        )

        is_checked = checkbox.get_attribute("checked")

        if is_checked == "false":
            self.execute_step(
                "STEP: Select checkbox 'Jestem członkiem OFE/mam subkonto'",
                lambda: self.click_element(
                    'new UiSelector().description("Jestem członkiem OFE/mam subkonto")'
                )
            )
            time.sleep(1)
        else:
            print("Checkbox is already selected. Proceeding.")
