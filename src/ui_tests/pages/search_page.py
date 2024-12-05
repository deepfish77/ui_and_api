from selenium.webdriver.common.by import By as By
from selenium.webdriver.common.keys import Keys
from  src.ui_tests.pages.base_page import BasePage
from  src.ui_tests.pages.video_page import VideoPageMobile


class MobileSearchPage(BasePage):

    # Page Init
    def __init__(self, web_driver):
        super().__init__(web_driver)
        self.url = "directory"

    # Which element should be rendered in order for us to be satisfied that all the page is loaded
    # We should choose the last element that is loaded and check it.. that is the reason for rendering_status_element
    # Page Elements
    search_box_by_expression = {
        "by": By.XPATH,
        "value": "//input[@placeholder='Search']",
    }
    videos_tab = {"by": By.XPATH, "value": "//a//div[text()='Videos']"}

    # This was the identifier that seemed as the most change prone from others
    get_all_videos_xpath = "//a[contains(@class, 'ScCoreLink-sc')]"

    # Page Methods

    def execute_search(self, search_term):
        search_box_field = self.wait_for_element(self.search_box_by_expression)
        search_box_field.clear()
        search_box_field.send_keys(search_term)
        search_box_field.send_keys(Keys.RETURN)

    def switch_to_videos(self):
        videos_tab = self.wait_for_element(self.videos_tab)
        videos_tab.click()

    def get_videos_in_page_in_viewport(self):

        # Get all videos from page
        all_videos = self.driver.find_elements(By.XPATH, self.get_all_videos_xpath)

        # Filter the videos that are in the viewport
        vids_lst = []
        for _, video in enumerate(all_videos):
            element_bound_status = self.is_element_within_bounds(element=video)
            if element_bound_status:
                vids_lst.append(video)
        vids_count = len(vids_lst)
        return vids_lst, vids_count

    def click_on_video_and_go_to_page(self, web_object):
        web_object.click()
        return VideoPageMobile(self.driver)
