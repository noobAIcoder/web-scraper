# web-scraper

Project Summary: Web Scraping Tool with GUI

Objective:
The objective of this project is to develop a web scraping tool with a graphical user interface (GUI) that allows users to extract data from websites that require login and have a search functionality. The tool will automate the process of logging in, performing a search, and scraping desired data from the website. The scraped data will be stored in a SQLite database for further analysis and processing.

Key Features:
1. GUI Interface: The tool will provide a GUI built with PyQt5, allowing users to input website URL, login credentials, search query, and CSS selectors for data extraction and navigation.

2. Login Automation: The tool will automate the login process by filling in the login form with user-provided credentials and checking for successful login based on the presence of a specific element on the page.

3. Search Functionality: After successful login, the tool will allow users to enter a search query and perform a search on the website. The search results will be loaded and ready for data extraction.

4. Data Extraction: Users will provide CSS selectors to identify the desired data elements on the page. The tool will extract the specified data from the search results and store it in a raw format in an SQLite database. 

5. Pagination Handling: If the search results are paginated, the tool will automatically navigate through the pages by clicking on the "next" button until all pages are processed.

6. Progress Tracking: The GUI will display the progress of the scraping process, including the current page being scraped, the number of items extracted, and any errors encountered.

7. Database Storage: The scraped data will be stored in a SQLite database for persistent storage and future analysis. The database will be created and managed by the tool. Columns should be following: URL, date, div contents

8. Error Handling: The tool will incorporate robust error handling mechanisms to gracefully handle and report errors related to login, search, data extraction, and database operations.

9. Logging: Detailed logging will be implemented to capture important events, errors, and debug information during the scraping process. Logs will be stored in a file for later review and troubleshooting.

10. Configuration Management: The tool will store user-provided settings such as website URL, login credentials, and CSS selectors in a configuration file. These settings will be loaded automatically when the tool is launched, allowing users to quickly resume their scraping tasks.

11. Multithreading: The scraping process will be executed in a separate thread to ensure a responsive GUI and prevent blocking of user interactions.

12. Modularity and Reusability: The codebase will be organized into modular components, separating the GUI, scraping, database, and utility functions. This modular architecture will enhance code reusability and maintainability.

Technologies and Libraries:
- Python: The primary programming language for the project.
- PyQt5: The library used for building the GUI.
- Selenium: A web automation library used for interacting with web pages, handling login, and performing search.
- BeautifulSoup: A library for parsing HTML and extracting desired data from web pages.
- SQLite: A lightweight and embedded database engine for storing scraped data.
- Requests: A library for making HTTP requests to web pages.
- ChromeDriver: A web driver used by Selenium to automate Google Chrome browser.

Project Structure:
The project will be organized into the following files and directories:
- `main.py`: The entry point of the application, responsible for creating the GUI and starting the application.
- `main_window.py`: Defines the main window of the GUI and handles user interactions.
- `scraper.py`: Defines the core scraping functionality, including login, search, and data extraction.
- `database.py`: Defines the database operations for storing scraped data.
- `config.py`: Handles configuration management for storing and loading user settings.
- `logger.py`: Implements logging functionality for capturing important events and errors.
- `config.ini`: A configuration file for storing user-provided settings.
- `requirements.txt`: A file listing the project dependencies.
- `README.md`: A readme file providing an overview of the project and installation instructions.


-----------------------------------------------------------------------------
