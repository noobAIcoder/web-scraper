from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class ScraperCore:
    def __init__(self, driver, db, logger):
        self.driver = driver
        self.db = db
        self.logger = logger

    def scrape_data(self, data_div_selector, table_selector, tbody_selector, next_button_selector, timeout, stop_flag, cancel_flag):
        page = 1
        total_items = 0

        while not stop_flag and not cancel_flag:
            self.logger.log(f"Scraping page {page}")

            # Wait for data rows to stabilize
            if not self.wait_for_data_rows_to_stabilize(data_div_selector, table_selector, tbody_selector, timeout):
                self.logger.log("Timeout waiting for data rows to stabilize")
                break

            # Scrape data from the div
            data_div = self.driver.find_element(By.CSS_SELECTOR, data_div_selector)
            grid_content = data_div.find_element(By.CSS_SELECTOR, table_selector)
            table = grid_content.find_element(By.TAG_NAME, "table")
            tbody = table.find_element(By.TAG_NAME, tbody_selector)
            scraped_data = self.scrape_data_from_tbody(tbody)
            # Validate and cleanse the scraped data
            validated_data = self.validate_and_cleanse_data(scraped_data)
            # Store the validated data in the database
            self.store_data_in_database(validated_data)
            total_items += len(validated_data)
            self.logger.log(f"Scraped {len(validated_data)} items from page {page}")

            # Find the next button
            next_button = self.find_next_button(next_button_selector)

            if next_button and next_button.is_enabled():
                self.logger.log(f"Clicking next button on page {page}")
                next_button.click()
                # Wait for the page to load new content after clicking the next button
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, data_div_selector))
                )
                self.logger.log("New page loaded successfully")
                page += 1
            else:
                self.logger.log("No more pages found or next button not enabled")
                break

        if cancel_flag:
            self.logger.log("Scraping canceled")
        else:
            self.logger.log("Scraping completed")

        return total_items

    def wait_for_data_rows_to_stabilize(self, data_div_selector, table_selector, tbody_selector, timeout):
        start_time = time.time()
        previous_count = 0
        stable_time = 0

        while time.time() - start_time < timeout:
            try:
                data_div = self.driver.find_element(By.CSS_SELECTOR, data_div_selector)
                grid_content = data_div.find_element(By.CSS_SELECTOR, table_selector)
                table = grid_content.find_element(By.TAG_NAME, "table")
                tbody = table.find_element(By.TAG_NAME, tbody_selector)
                rows = tbody.find_elements(By.TAG_NAME, "tr")
                current_count = len(rows)
                self.logger.log(f"Current row count: {current_count}, Previous row count: {previous_count}, Stable time: {stable_time}")

                if current_count == previous_count:
                    stable_time += 0.1  # Increase stable time if count hasn't changed
                else:
                    stable_time = 0  # Reset stable time if count changes

                previous_count = current_count

                if stable_time >= 1:  # Stable for 1 second
                    self.logger.log("Data rows have stabilized")
                    return True

            except NoSuchElementException:
                self.logger.log("No data rows found")
                pass
            except Exception as e:
                self.handle_scraping_error(e)

            time.sleep(0.1)  # Polling interval

        self.logger.log("Timeout waiting for data rows to stabilize")
        return False

    def scrape_data_from_tbody(self, tbody):
        scraped_data = []
        encoding = self.get_encoding()

        try:
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                data = row.text
                data = data.encode(encoding).decode(encoding)
                scraped_data.append(data)
        except Exception as e:
            self.handle_scraping_error(e)

        return scraped_data

    def get_encoding(self):
        return "utf-8"

    def validate_and_cleanse_data(self, scraped_data):
        # Implement data validation and cleansing logic here
        return scraped_data

    def store_data_in_database(self, validated_data):
        # Implement data storage logic here
        pass

    def find_next_button(self, next_button_selector):
        return self.driver.find_element(By.CSS_SELECTOR, next_button_selector)

    def handle_scraping_error(self, error):
        self.logger.log(f"Scraping error: {str(error)}", level="error")
