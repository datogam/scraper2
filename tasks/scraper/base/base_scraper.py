from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os


SCRAPER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Scraper:
    def __init__(self, delay=5, log_path='logs/scraper.log', screenshot_path='logs/scraper_screenshot.png'):
        self.delay = delay
        opts = Options()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(executable_path=os.path.join(SCRAPER_PATH, 'geckodriver'), options=opts)
        self.logger = logging.getLogger('app')
        hdlr = logging.FileHandler(log_path)
        hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)
        self.screenshot_path = screenshot_path

    def login(self):
        try:
            self.driver.get(self.login_url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.username['by'])
            ).send_keys(self.username['text'])
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.password['by'])
            ).send_keys(self.password['text'])

            self.driver.find_element(*self.submit).click()
            time.sleep(self.delay)

            if self.driver.current_url.strip('/ ') == self.redirect_url.strip('/ '):
                self.logger.error('login failed')
                return True
        except Exception as e:
            self.logger.error('login failed')
            self.logger.error(str(e))

        self.driver.get_screenshot_as_file(self.screenshot_path)
        return False


class DataScraper(Scraper):
    def __init__(self, login_url, username, password, submit, redirect_url):
        self.login_url = login_url
        self.username = username
        self.password = password
        self.submit = submit
        self.redirect_url = redirect_url
        super(DataScraper, self).__init__()

    def get_data(self, url, elements):
        try:
            self.driver.get(url)
            data = {}
            for element in elements:
                value = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(element['by'])
                ).get_attribute('value')
                data[element['name']] = value
            return data
        except Exception as e:
            self.logger.error('login failed')
            self.logger.error(str(e))
            self.driver.get_screenshot_as_file(self.screenshot_path)
            return None

    def run(self, page_url, elements):
        if self.login():
            data = self.get_data(page_url, elements)
            return data


class FileScraper(Scraper):
    def __init__(self, login_url, username, password, submit, redirect_url):
        self.login_url = login_url
        self.username = username
        self.password = password
        self.submit = submit
        self.redirect_url = redirect_url
        super(FileScraper, self).__init__()

    def download_file(self, url, element):
        try:
            self.driver.get(url)
            file = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(element['by'])
            ).click()
            return file
        except Exception as e:
            self.logger.error('login failed')
            self.logger.error(str(e))
            self.driver.get_screenshot_as_file(self.screenshot_path)
            return None

    def run(self, page_url, elements):
        if self.login():
            data = self.download_file(page_url, elements)
            return data