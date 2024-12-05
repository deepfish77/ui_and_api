import time
from  src.ui_tests.pages.base_page import BasePage
from selenium.webdriver.common.by import By as By


class VideoPageMobile(BasePage):

    # Page Init
    def __init__(self, web_driver):
        super().__init__(web_driver)
        self.url = "videos"

    # Page Elements
    start_watching_button = {
        "by": By.XPATH,
        "value": '//button[@data-a-target="content-classification-gate-overlay-start-watching-button"]',
    }

    subscribe_button = {
        "by": By.XPATH,
        "value": '//button[.//div[text()="Subscribe"]]',
    }
    video_duration_view = {
        "by": By.XPATH,
        "value": '//p[@data-a-target="player-seekbar-current-time"]',
    }

    def check_subscribed_present(self):
        return self.is_element_visible(self.subscribe_button, timeout=10)

    def check_modal_user_present_and_continue(self):
        is_visible = self.is_element_visible(self.start_watching_button, timeout=3)
        if is_visible:
            print("found the user modal, clicking on continue")
            continue_button = self.find_element(self.start_watching_button)
            continue_button.click()
            return True
        else:
            return False

    def validate_time_increasing(self, time_list):
        # Check if the list has at least one valid time
        if not time_list:
            print("The time list is empty.")
            return False

        # Convert the time strings to seconds for comparison
        def time_to_seconds(time_str):
            h, m, s = map(int, time_str.split(":"))
            return h * 3600 + m * 60 + s

        # Validate increasing time
        times_in_seconds = [time_to_seconds(time) for time in time_list]
        is_increasing = all(
            x < y for x, y in zip(times_in_seconds, times_in_seconds[1:])
        )

        if is_increasing:
            print("The time is increasing.")
        else:
            print("The time is not strictly increasing.")

        return is_increasing

    def assert_video_started_playing(self):

        self.wait_for_element(self.video_duration_view)
        current_elm_value = []
        for _ in range(3):
            video_element = self.find_element(self.video_duration_view)
            inner_text = video_element.get_attribute("innerText")
            time.sleep(2)
            current_elm_value.append(inner_text)
        print("video playing time: ", current_elm_value)
        assert self.validate_time_increasing(
            current_elm_value
        ), "The Video is not playing... check issue"
