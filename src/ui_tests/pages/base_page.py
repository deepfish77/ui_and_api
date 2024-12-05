import os
import time
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Should be in config file. for the sake of exercise its here
BASE_PAGE = "https://m.twitch.tv/"
# For saving screen shots to a file
SCREENSHOT_PATH = "C:/AutoCourse/practiceback/selenium_automation/screenshots"


class BasePage(object):

    # rendering_status_element - This element is the selected element that when rendered, it means
    # that the page is rendered successfully - should be populated in inherited classes

    def __init__(self, web_driver):
        self.base_url = BASE_PAGE
        self.driver = web_driver
        self.timeout = 30
        self.url = ""

    def find_element(self, loc):
        return self.driver.find_element(loc.get("by"), loc.get("value"))

    def open(self, window_size_width=600, window_size_height=1024):

        curr_url = self.base_url + self.url
        self.driver.get(curr_url)
        self.driver.set_window_size(window_size_width, window_size_height)
        # self.driver.maximize_window()

    def is_elm_initialized(self, rendering_status_element, wait_timeout=30):

        page_init = WebDriverWait(self.driver, wait_timeout).until(
            lambda driver: driver.find_element(
                rendering_status_element.get("by"),
                rendering_status_element.get("value"),
            )
        )
        print("page init enabled", page_init.is_enabled())
        return page_init.is_enabled()

    def scroll_page(self, scroll_count=2, scroll_height=100):

        for i in range(scroll_count):  # Scroll twice
            self.driver.execute_script(
                f"window.scrollBy(0, {scroll_height});"
            )  # Scroll by specified height
            print(f"Scroll {i + 1} by {scroll_height} pixels")
            time.sleep(1)

    def wait_for_element(self, element_locator, timeout=20):

        print("waiting for element: ", element_locator.get("value"))
        return WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.find_element(
                element_locator.get("by"), element_locator.get("value")
            )
        )

    def is_element_visible(self, element_locator, timeout=20):

        locator = (element_locator.get("by"), element_locator.get("value"))
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False

    def is_element_invisible(self, element_locator, timeout=20):

        locator = (element_locator.get("by"), element_locator.get("value"))
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except:
            return False

    def take_screenshot_and_save_to_local_directory(self):

        sc_time = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        result_file = os.path.join(SCREENSHOT_PATH, f"screenshot_{sc_time}.png")
        os.makedirs(os.path.dirname(result_file), exist_ok=True)

        # Take the screenshot
        self.driver.save_screenshot(result_file)
        return result_file

    def get_viewport_bounds(self):

        return {
            "top": 0,
            "left": 0,
            "right": self.driver.execute_script("return window.innerWidth"),
            "bottom": self.driver.execute_script("return window.innerHeight"),
        }

    def get_element_bounds(self, element):

        bounds = self.driver.execute_script(
            """
            var rect = arguments[0].getBoundingClientRect();
            return {
                top: rect.top,
                left: rect.left,
                bottom: rect.bottom,
                right: rect.right,
                width: rect.width,
                height: rect.height
            };
        """,
            element,
        )
        return bounds

    def is_element_within_bounds(self, element):

        bounds_to_check = self.get_viewport_bounds()
        element_bounds = self.get_element_bounds(element)

        # Check if the element is within the specified bounds
        within_bounds = (
            element_bounds["top"] >= bounds_to_check["top"]
            and element_bounds["left"] >= bounds_to_check["left"]
            and element_bounds["right"] <= bounds_to_check["right"]
            and element_bounds["bottom"] <= bounds_to_check["bottom"]
        )

        return within_bounds
