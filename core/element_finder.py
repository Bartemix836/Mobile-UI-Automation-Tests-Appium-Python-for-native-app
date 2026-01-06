import dateutil.utils
import openpyxl
import pytest
from selenium.common import NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
import subprocess
import pyperclip
import re
import logging
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


logging.basicConfig(level=logging.INFO)



class ElementFinder:
    def __init__(self, driver):
        self.driver = driver  # Driver