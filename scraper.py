from PyQt5.QtCore import QObject, pyqtSignal
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from logger import Logger
from database import Database
from config import Config
from scraper_core import ScraperCore

class Scraper(QObject):
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
        self.driver = self.setup_driver()
        self.db = Database()
        self.logger = Logger("scraper.log")
        self.stop_flag = False
        self.cancel_flag = False
        self.scraper_core = ScraperCore(self.driver, self.db, self.logger)

    def setup_driver(self):
        options = Options()
        options.add_argument("--start-maximized")

        config = Config()
        settings = config.read_config()

        if settings:
            user_agent = settings.get("browser", "user_agent", fallback=None)
            if user_agent:
                options.add_argument(f"user-agent={user_agent}")

        options.add_argument("user-data-dir=C:\\path\\to\\chrome\\profile")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        return driver

    def login(self):
        try:
            self.driver.get(self.url)
            self.logger.log(f"Navigating to website: {self.url}")

            field1_identifier = self.login_credentials["field1"]["identifier"]
            field1_value = self.login_credentials["field1"]["value"]
            field2_identifier = self.login_credentials["field2"]["identifier"]
            field2_value = self.login_credentials["field2"]["value"]
            field3_identifier = self.login_credentials["field3"]["identifier"]
            field3_value = self.login_credentials["field3"]["value"]
            button_selector = self.login_credentials["button_selector"]
            mode_button_selector = self.login_credentials["mode_button_selector"]

            field1_element = self.driver.find_element(By.CSS_SELECTOR, field1_identifier)
            field1_element.clear()
            field1_element.send_keys(field1_value)

            if field2_identifier and field2_value:
                field2_element = self.driver.find_element(By.CSS_SELECTOR, field2_identifier)
                field2_element.clear()
                field2_element.send_keys(field2_value)

            if field3_identifier and field3_value:
                field3_element = self.driver.find_element(By.CSS_SELECTOR, field3_identifier)
                field3_element.clear()
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
            self.logger.log(f"Login failed: {str(e)}", level="error")
            self.error_occurred.emit(f"Login failed: {str(e)}")

    def search(self, search_query):
        try:
            search_input_identifier = self.login_credentials["search_input_identifier"]
            search_button_identifier = self.login_credentials["search_button_identifier"]

            search_input = self.driver.find_element(By.CSS_SELECTOR, search_input_identifier)
            search_input.clear()
            search_input.send_keys(search_query)
            self.logger.log(f"Entered search query: {search_query}")

            search_button = self.driver.find_element(By.CSS_SELECTOR, search_button_identifier)
            search_button.click()
            self.logger.log("Clicked search button")

            self.search_status.emit("Search completed successfully")
        except Exception as e:
            self.logger.log(f"Search failed: {str(e)}", level="error")
            self.error_occurred.emit(f"Search failed: {str(e)}")

    def start_scraping(self, data_div_selector, table_selector, tbody_selector, next_button_selector, timeout):
        total_items = self.scraper_core.scrape_data(data_div_selector, table_selector, tbody_selector, next_button_selector, timeout, self.stop_flag, self.cancel_flag)
        if self.cancel_flag:
            self.logger.log("Scraping canceled")
            self.scraping_finished.emit("Scraping canceled")
        else:
            self.logger.log("Scraping completed")
            self.scraping_finished.emit("Scraping completed")
        return total_items

    def stop_scraping(self):
        self.stop_flag = True
        self.logger.log("Scraping stopped")

    def cancel_scraping(self):
        self.cancel_flag = True
        self.logger.log("Scraping canceled")

    def __del__(self):
        self.driver.quit()
        self.db.close_connection()
