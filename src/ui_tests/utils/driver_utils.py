import functools
import src.ui_tests.utils.drivers as web_driver


def driver_wrapper(driver_name):
    """
    Decorator to manage WebDriver lifecycle for a specific driver type.
    :param driver_name: The name of the driver ('chrome', 'firefox', 'android').
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # Initialize WebDriver
            try:
                driver = web_driver.get_driver(driver_name)
                print(f"Initialized {driver_name} driver.")
                try:
                    # Pass the driver along with other arguments to the decorated function
                    func(*args, driver=driver, **kwargs)
                finally:
                    driver.quit()
                    print(f"{driver_name} driver quit.")
            except Exception as ex:
                print(f"Couldn't get driver '{driver_name}'. Error: {ex}")

        return wrapper

    return decorator
