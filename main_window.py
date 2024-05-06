from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal
from scraper import Scraper
from config import Config
from logger import Logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Scraping Tool")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.setup_login_settings()
        self.setup_scraping_settings()
        self.setup_status_widgets()
        self.setup_browser_settings()  # Add this line

        self.load_settings()

        self.scraper = None

    def setup_login_settings(self):
        login_layout = QVBoxLayout()

        self.url_label = QLabel("Website URL:")
        self.url_input = QLineEdit()
        login_layout.addWidget(self.url_label)
        login_layout.addWidget(self.url_input)

        self.login_field1_label = QLabel("Login Field 1 Identifier:")
        self.login_field1_input = QLineEdit()
        self.login_field1_value_label = QLabel("Login Field 1 Value:")
        self.login_field1_value_input = QLineEdit()
        login_layout.addWidget(self.login_field1_label)
        login_layout.addWidget(self.login_field1_input)
        login_layout.addWidget(self.login_field1_value_label)
        login_layout.addWidget(self.login_field1_value_input)

        self.login_field2_label = QLabel("Login Field 2 Identifier:")
        self.login_field2_input = QLineEdit()
        self.login_field2_value_label = QLabel("Login Field 2 Value:")
        self.login_field2_value_input = QLineEdit()
        login_layout.addWidget(self.login_field2_label)
        login_layout.addWidget(self.login_field2_input)
        login_layout.addWidget(self.login_field2_value_label)
        login_layout.addWidget(self.login_field2_value_input)

        self.login_field3_label = QLabel("Login Field 3 Identifier:")
        self.login_field3_input = QLineEdit()
        self.login_field3_value_label = QLabel("Login Field 3 Value:")
        self.login_field3_value_input = QLineEdit()
        login_layout.addWidget(self.login_field3_label)
        login_layout.addWidget(self.login_field3_input)
        login_layout.addWidget(self.login_field3_value_label)
        login_layout.addWidget(self.login_field3_value_input)

        self.login_button_selector_label = QLabel("Login Button Selector:")
        self.login_button_selector_input = QLineEdit()
        login_layout.addWidget(self.login_button_selector_label)
        login_layout.addWidget(self.login_button_selector_input)

        self.mode_button_selector_label = QLabel("Website Mode Button Selector:")
        self.mode_button_selector_input = QLineEdit()
        login_layout.addWidget(self.mode_button_selector_label)
        login_layout.addWidget(self.mode_button_selector_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login_clicked)
        login_layout.addWidget(self.login_button)

        self.layout.addLayout(login_layout)

    def setup_scraping_settings(self):
        scraping_layout = QVBoxLayout()

        self.search_query_label = QLabel("Search Query:")
        self.search_query_input = QLineEdit()
        scraping_layout.addWidget(self.search_query_label)
        scraping_layout.addWidget(self.search_query_input)

        self.search_input_label = QLabel("Search Input Field Identifier:")
        self.search_input_input = QLineEdit()
        scraping_layout.addWidget(self.search_input_label)
        scraping_layout.addWidget(self.search_input_input)

        self.search_button_label = QLabel("Search Button Identifier:")
        self.search_button_input = QLineEdit()
        scraping_layout.addWidget(self.search_button_label)
        scraping_layout.addWidget(self.search_button_input)

        wait_layout = QHBoxLayout()

        self.wait_login_label = QLabel("Wait Time After Login:")
        self.wait_login_input = QLineEdit()
        self.wait_login_input.setFixedWidth(50)
        self.wait_login_increase_button = QPushButton("+")
        self.wait_login_increase_button.setFixedWidth(30)
        self.wait_login_increase_button.clicked.connect(self.increase_wait_login)
        self.wait_login_decrease_button = QPushButton("-")
        self.wait_login_decrease_button.setFixedWidth(30)
        self.wait_login_decrease_button.clicked.connect(self.decrease_wait_login)
        wait_layout.addWidget(self.wait_login_label)
        wait_layout.addWidget(self.wait_login_input)
        wait_layout.addWidget(self.wait_login_increase_button)
        wait_layout.addWidget(self.wait_login_decrease_button)

        self.wait_mode_label = QLabel("Wait Time After Switching Mode:")
        self.wait_mode_input = QLineEdit()
        self.wait_mode_input.setFixedWidth(50)
        self.wait_mode_increase_button = QPushButton("+")
        self.wait_mode_increase_button.setFixedWidth(30)
        self.wait_mode_increase_button.clicked.connect(self.increase_wait_mode)
        self.wait_mode_decrease_button = QPushButton("-")
        self.wait_mode_decrease_button.setFixedWidth(30)
        self.wait_mode_decrease_button.clicked.connect(self.decrease_wait_mode)
        wait_layout.addWidget(self.wait_mode_label)
        wait_layout.addWidget(self.wait_mode_input)
        wait_layout.addWidget(self.wait_mode_increase_button)
        wait_layout.addWidget(self.wait_mode_decrease_button)

        self.wait_search_label = QLabel("Wait Time After Search:")
        self.wait_search_input = QLineEdit()
        self.wait_search_input.setFixedWidth(50)
        self.wait_search_increase_button = QPushButton("+")
        self.wait_search_increase_button.setFixedWidth(30)
        self.wait_search_increase_button.clicked.connect(self.increase_wait_search)
        self.wait_search_decrease_button = QPushButton("-")
        self.wait_search_decrease_button.setFixedWidth(30)
        self.wait_search_decrease_button.clicked.connect(self.decrease_wait_search)
        wait_layout.addWidget(self.wait_search_label)
        wait_layout.addWidget(self.wait_search_input)
        wait_layout.addWidget(self.wait_search_increase_button)
        wait_layout.addWidget(self.wait_search_decrease_button)

        scraping_layout.addLayout(wait_layout)

        self.data_div_label = QLabel("Data Div Selector:")
        self.data_div_input = QLineEdit()
        scraping_layout.addWidget(self.data_div_label)
        scraping_layout.addWidget(self.data_div_input)

        self.next_button_label = QLabel("Next Button Selector:")
        self.next_button_input = QLineEdit()
        scraping_layout.addWidget(self.next_button_label)
        scraping_layout.addWidget(self.next_button_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_clicked)
        scraping_layout.addWidget(self.search_button)

        self.start_scraping_button = QPushButton("Start Scraping")
        self.start_scraping_button.clicked.connect(self.start_scraping_clicked)
        scraping_layout.addWidget(self.start_scraping_button)

        self.stop_scraping_button = QPushButton("Stop Scraping")
        self.stop_scraping_button.clicked.connect(self.stop_scraping_clicked)
        scraping_layout.addWidget(self.stop_scraping_button)

        self.cancel_scraping_button = QPushButton("Cancel Scraping")
        self.cancel_scraping_button.clicked.connect(self.cancel_scraping_clicked)
        scraping_layout.addWidget(self.cancel_scraping_button)

        self.layout.addLayout(scraping_layout)

    def setup_status_widgets(self):
        self.status_label = QLabel("Status: Ready")
        self.layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.layout.addWidget(self.log_text_edit)

    def setup_browser_settings(self):
        browser_layout = QVBoxLayout()

        self.user_agent_label = QLabel("User Agent:")
        self.user_agent_input = QLineEdit()
        browser_layout.addWidget(self.user_agent_label)
        browser_layout.addWidget(self.user_agent_input)

        self.layout.addLayout(browser_layout)

    def load_settings(self):
        config = Config()
        settings = config.read_config()

        if settings:
            self.url_input.setText(settings.get("website", "url", fallback=""))
            self.login_field1_input.setText(settings.get("login", "field1_identifier", fallback=""))
            self.login_field1_value_input.setText(settings.get("login", "field1_value", fallback=""))
            self.login_field2_input.setText(settings.get("login", "field2_identifier", fallback=""))
            self.login_field2_value_input.setText(settings.get("login", "field2_value", fallback=""))
            self.login_field3_input.setText(settings.get("login", "field3_identifier", fallback=""))
            self.login_field3_value_input.setText(settings.get("login", "field3_value", fallback=""))
            self.login_button_selector_input.setText(settings.get("login", "button_selector", fallback=""))
            self.mode_button_selector_input.setText(settings.get("login", "mode_button_selector", fallback=""))
            self.search_query_input.setText(settings.get("scraping", "search_query", fallback=""))
            self.search_input_input.setText(settings.get("scraping", "search_input_identifier", fallback=""))
            self.search_button_input.setText(settings.get("scraping", "search_button_identifier", fallback=""))
            self.wait_login_input.setText(settings.get("scraping", "wait_login", fallback="5"))
            self.wait_mode_input.setText(settings.get("scraping", "wait_mode", fallback="3"))
            self.wait_search_input.setText(settings.get("scraping", "wait_search", fallback="2"))
            self.data_div_input.setText(settings.get("scraping", "data_div_selector", fallback=""))
            self.next_button_input.setText(settings.get("scraping", "next_button_selector", fallback=""))
            user_agent = settings.get("browser", "user_agent", fallback="")
            if user_agent:
                self.user_agent_input.setText(user_agent)

    def save_settings(self):
        config = Config()
        settings = {
            "website": {
                "url": self.url_input.text()
            },
            "login": {
                "field1_identifier": self.login_field1_input.text(),
                "field1_value": self.login_field1_value_input.text(),
                "field2_identifier": self.login_field2_input.text(),
                "field2_value": self.login_field2_value_input.text(),
                "field3_identifier": self.login_field3_input.text(),
                "field3_value": self.login_field3_value_input.text(),
                "button_selector": self.login_button_selector_input.text(),
                "mode_button_selector": self.mode_button_selector_input.text()
            },
            "scraping": {
                "search_query": self.search_query_input.text(),
                "search_input_identifier": self.search_input_input.text(),
                "search_button_identifier": self.search_button_input.text(),
                "wait_login": self.wait_login_input.text(),
                "wait_mode": self.wait_mode_input.text(),
                "wait_search": self.wait_search_input.text(),
                "data_div_selector": self.data_div_input.text(),
                "next_button_selector": self.next_button_input.text()
            },
            "browser": {
                "user_agent": self.user_agent_input.text()
            }
        }

        print("Settings to be saved:")
        print(settings)

        config.write_config(settings)

    def login_clicked(self):
        url = self.url_input.text()
        login_credentials = {
            "field1": {
                "identifier": self.login_field1_input.text(),
                "value": self.login_field1_value_input.text()
            },
            "field2": {
                "identifier": self.login_field2_input.text(),
                "value": self.login_field2_value_input.text()
            },
            "field3": {
                "identifier": self.login_field3_input.text(),
                "value": self.login_field3_value_input.text()
            },
            "button_selector": self.login_button_selector_input.text(),
            "mode_button_selector": self.mode_button_selector_input.text(),
            "search_input_identifier": self.search_input_input.text(),
            "search_button_identifier": self.search_button_input.text()
        }

        if not url:
            QMessageBox.critical(self, "Error", "Please enter a website URL.")
            return

        if not login_credentials["field1"]["identifier"] or not login_credentials["field1"]["value"]:
            QMessageBox.critical(self, "Error", "Please enter values for Login Field 1.")
            return

        self.scraper = Scraper(url, login_credentials)
        self.scraper.login_status.connect(self.update_status)
        self.scraper.search_status.connect(self.update_status)
        self.scraper.scraping_progress.connect(self.update_progress)
        self.scraper.scraping_finished.connect(self.update_status)
        self.scraper.error_occurred.connect(self.handle_error)
        self.scraper.message_logged.connect(self.log_message)

        self.scraper.login()

    def search_clicked(self):
        if not self.scraper:
            QMessageBox.critical(self, "Error", "Please log in before performing a search.")
            return

        search_query = self.search_query_input.text()
        if not search_query:
            QMessageBox.warning(self, "Warning", "Please enter a search query.")
            return

        self.scraper.search(search_query)

    def start_scraping_clicked(self):
        data_div_selector = self.data_div_input.text()
        next_button_selector = self.next_button_input.text()

        if not data_div_selector:
            QMessageBox.critical(self, "Error", "Please enter a data div selector.")
            return

        if not next_button_selector:
            QMessageBox.critical(self, "Error", "Please enter a next button selector.")
            return

        if not self.scraper:
            QMessageBox.critical(self, "Error", "Please log in and perform a search before starting scraping.")
            return

        self.scraper.scrape_data(data_div_selector, next_button_selector)

    def stop_scraping_clicked(self):
        if self.scraper:
            self.scraper.stop_scraping()

    def cancel_scraping_clicked(self):
        if self.scraper:
            self.scraper.cancel_scraping()

    def update_status(self, status):
        self.status_label.setText(f"Status: {status}")
    
    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def handle_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)

    def log_message(self, message):
        self.log_text_edit.append(message)

    def increase_wait_login(self):
        current_value = int(self.wait_login_input.text())
        self.wait_login_input.setText(str(current_value + 1))

    def decrease_wait_login(self):
        current_value = int(self.wait_login_input.text())
        if current_value > 0:
            self.wait_login_input.setText(str(current_value - 1))

    def increase_wait_mode(self):
        current_value = int(self.wait_mode_input.text())
        self.wait_mode_input.setText(str(current_value + 1))

    def decrease_wait_mode(self):
        current_value = int(self.wait_mode_input.text())
        if current_value > 0:
            self.wait_mode_input.setText(str(current_value - 1))

    def increase_wait_search(self):
        current_value = int(self.wait_search_input.text())
        self.wait_search_input.setText(str(current_value + 1))

    def decrease_wait_search(self):
        current_value = int(self.wait_search_input.text())
        if current_value > 0:
            self.wait_search_input.setText(str(current_value - 1))

    def closeEvent(self, event):
        self.save_settings()
        event.accept()
