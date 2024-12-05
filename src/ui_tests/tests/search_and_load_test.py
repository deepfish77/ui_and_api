import pytest
import random
from src.ui_tests.utils.driver_utils import driver_wrapper
from src.ui_tests.pages.main_index_page import TwitchMainPage



@pytest.mark.parametrize("search_term", ["StarCraft II"])
@driver_wrapper(driver_name="android")
def test_search_a_term_and_validate_test(search_term, driver=None):
    main_page = TwitchMainPage(driver)
    main_page.open()
    print("attempting to open the search page...")
    search_page = main_page.open_search()
    print(f"search opened successfully, executing search...{search_term}")
    search_page.execute_search(search_term=search_term)

    # The intitial page is opening at the 'Top' tab content
    # switching to the 'Videos' tab to enable the scrolling
    # operation and to select a video
    search_page.switch_to_videos()

    # Controllable scroll pace, scroll_count= number of scrolls,scroll_height=height of scroll
    search_page.scroll_page(scroll_count=2, scroll_height=200)

    # Getting all the videos in the page , and filtering out the ones
    # that are not in the current viewport
    videos, count_vids_viewport = search_page.get_videos_in_page_in_viewport()
    assert (
        count_vids_viewport > 0
    ), "There are no videos returned on viewport, check possible bug"

    # Clicking randomally on a video and checking it started playing
    random_int = random.randint(1, count_vids_viewport - 1)
    selected_video = videos[random_int]
    video_page = search_page.click_on_video_and_go_to_page(selected_video)

    # if the content is for SUBSCRIBED USERS?
    subscribed_present = video_page.check_subscribed_present()
    if subscribed_present is True:
        print("The video cannot be played without subscription")
        video_page.take_screenshot_and_save_to_local_directory()
    else:
        #  a MODAL before video playing ?
        video_page.check_modal_user_present_and_continue()
        # ASSERT if the video started playing
        video_page.assert_video_started_playing()

        # taking a screenshot
        video_page.take_screenshot_and_save_to_local_directory()

