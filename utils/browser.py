from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep

ROOT_DIR = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver'
CHROMERIVER_PATH: str = str(ROOT_DIR / 'bin' / CHROMEDRIVER_NAME)


def make_chrome_browser(*options) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(executable_path=CHROMERIVER_PATH)
    browser = webdriver.Chrome(
        service=chrome_service,
        options=chrome_options
    )
    return browser


if __name__ == "__main__":
    browser = make_chrome_browser()
    browser.get('https://www.google.com.br/')
    sleep(10)
    browser.quit()
