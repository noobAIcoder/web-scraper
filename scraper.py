from PyQt5.QtCore import QObject, pyqtSignal
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from config import Config
from database import Database
from logger import Logger
import time


class BaseScraper(QObject):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.add_argument("--start-maximized")

        config = Config()
        settings = config.read_config()

        if settings:
            user_agent = settings.get("browser", "user_agent", fallback=None)
            if user_agent:
                options.add_argument(f"user-agent={user_agent}")

        options.add_argument("user-data-dir=C:\\path\\to\\chrome\\profile")  # Add this line

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def quit_driver(self):
        if self.driver:
            self.driver.quit()

class Scraper(BaseScraper):
    login_status = pyqtSignal(str)
    search_status = pyqtSignal(str)
    scraping_progress = pyqtSignal(int)
    scraping_finished = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    message_logged = pyqtSignal(str)

    def __init__(self, url, login_credentials):
        super().__init__()
        self.url = url
        self.login_credentials = login_credentials
        self.db = Database()
        self.logger = Logger("scraper.log")
        self.stop_flag = False
        self.cancel_flag = False

    def login(self):
        try:
            self.driver.get(self.url)
            self.logger.log("Navigating to website: {}".format(self.url))

            field1_identifier = self.login_credentials["field1"]["identifier"]
            field1_value = self.login_credentials["field1"]["value"]
            field2_identifier = self.login_credentials["field2"]["identifier"]
            field2_value = self.login_credentials["field2"]["value"]
            field3_identifier = self.login_credentials["field3"]["identifier"]
            field3_value = self.login_credentials["field3"]["value"]
            button_selector = self.login_credentials["button_selector"]
            mode_button_selector = self.login_credentials["mode_button_selector"]

            field1_element = self.driver.find_element(By.CSS_SELECTOR, field1_identifier)
            field1_element.send_keys(field1_value)

            if field2_identifier and field2_value:
                field2_element = self.driver.find_element(By.CSS_SELECTOR, field2_identifier)
                field2_element.send_keys(field2_value)

            if field3_identifier and field3_value:
                field3_element = self.driver.find_element(By.CSS_SELECTOR, field3_identifier)
                field3_element.send_keys(field3_value)

            login_button = self.driver.find_element(By.CSS_SELECTOR, button_selector)
            login_button.click()
            self.logger.log("Logged in successfully")

            try:
                mode_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, mode_button_selector))
                )
                mode_button.click()
                self.logger.log("Switched to website mode")
                self.login_status.emit("Logged in successfully")
            except TimeoutException:
                self.logger.log("Mode button not found. Continuing without switching mode.")
                self.login_status.emit("Logged in successfully (mode button not found)")
        except Exception as e:
            self.logger.log("Login failed: {}".format(str(e)), level="error")
            self.error_occurred.emit("Login failed: {}".format(str(e)))

    def search(self, search_query):
        try:
            search_input_identifier = self.login_credentials["search_input_identifier"]
            search_button_identifier = self.login_credentials["search_button_identifier"]

            search_input = self.driver.find_element(By.CSS_SELECTOR, search_input_identifier)
            search_input.clear()
            search_input.send_keys(search_query)
            self.logger.log("Entered search query: {}".format(search_query))

            search_button = self.driver.find_element(By.CSS_SELECTOR, search_button_identifier)
            search_button.click()
            self.logger.log("Clicked search button")

            self.search_status.emit("Search completed successfully")
        except Exception as e:
            self.logger.log("Search failed: {}".format(str(e)), level="error")
            self.error_occurred.emit("Search failed: {}".format(str(e)))

    def scrape_data(self, data_div_selector, next_button_selector):
        try:
            page = 1
            total_items = 0

            config = Config()
            settings = config.read_config()

            if settings:
                encoding = settings.get("scraping", "encoding", fallback="utf-8")
            else:
                encoding = "utf-8"

            while not self.stop_flag and not self.cancel_flag:
                self.logger.log("Scraping page {}".format(page))

                try:
                    data_divs = self.driver.find_elements(By.CSS_SELECTOR, data_div_selector)
                    self.logger.log("Found {} data divs on page {}".format(len(data_divs), page))

                    for data_div in data_divs:
                        if self.stop_flag or self.cancel_flag:
                            break

                        data = data_div.get_attribute("innerText")
                        data = data.encode(encoding).decode(encoding)
                        url = self.driver.current_url

                        self.db.insert_data(url, data)
                        total_items += 1
                        self.logger.log("Scraped item {} from page {}".format(total_items, page))
                except NoSuchElementException:
                    self.logger.log("No data divs found on page {}".format(page))

                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, next_button_selector)
                    next_button.click()
                    self.logger.log("Clicked next button on page {}".format(page))
                    page += 1
                    time.sleep(2)  # Wait for page load
                except NoSuchElementException:
                    self.logger.log("No more pages found")
                    break

            if self.cancel_flag:
                self.logger.log("Scraping canceled")
                self.scraping_finished.emit("Scraping canceled")
            else:
                self.logger.log("Scraping completed")
                self.scraping_finished.emit("Scraping completed")
        except Exception as e:
            self.logger.log("Scraping failed: {}".format(str(e)), level="error")
            self.error_occurred.emit("Scraping failed: {}".format(str(e)))

    def stop_scraping(self):
        self.stop_flag = True
        self.logger.log("Scraping stopped")

    def cancel_scraping(self):
        self.cancel_flag = True
        self.logger.log("Scraping canceled")

    def __del__(self):
        self.quit_driver()
        self.db.close_connection()
