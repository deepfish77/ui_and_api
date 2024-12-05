from selenium import webdriver

PATH_TO_DRIVER = "C:\\AutoCourse\\practiceback\\drivers\\chromedriver.exe"


def _get_mobile_emulation_options(device_name="iPhone X"):

    chrome_options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": device_name}
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    return chrome_options


def _get_driver_options(driver_name):

    driver_options = {
        "chrome": webdriver.ChromeOptions(),
        "firefox": webdriver.FirefoxOptions(),
        "iphone": _get_mobile_emulation_options(device_name="iPhone X"),
        "android": _get_mobile_emulation_options(device_name="Nexus 5"),
    }.get(driver_name)

    if not driver_options:
        raise ValueError(f"Unsupported driver name: {driver_name}")

    return driver_options


def get_driver(driver_options):

    driver_opts = _get_driver_options(driver_options)
    return webdriver.Chrome(
        executable_path=PATH_TO_DRIVER,
        options=driver_opts,
    )