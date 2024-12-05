from selenium.webdriver.common.by import By as By
from src.ui_tests.pages.base_page import BasePage
from  src.ui_tests.pages.search_page import MobileSearchPage


class TwitchMainPage(BasePage):

    # Page Init
    def __init__(self, web_driver):
        super().__init__(web_driver)
        self.url = ""

    # Page Elements
    search_page_xpath = {
        "by": By.XPATH,
        "value": "//a[@href='/directory']//div[text()='Browse']",
    }
    search_page_css = {
        "by": By.CSS_SELECTOR,
        "value": "a.ScInteractableDefault-sc-ofisyf-1[href='/directory']",
    }

    # Page Methods

    def open_search(self):

        self.wait_for_element(self.search_page_xpath)
        search_box_field = self.find_element(self.search_page_xpath)
        print("search page ", search_box_field.tag_name)
        search_box_field.click()
        search_page = MobileSearchPage(self.driver)
        return search_page
