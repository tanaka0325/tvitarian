from selenium.webdriver import Chrome, ChromeOptions


def create_chrome_driver():
    options = ChromeOptions()
    # options.binary_location = '/app/.apt/usr/bin/google-chrome'
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    return Chrome(options=options)
