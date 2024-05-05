from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
# Other options you might need...

# Setup WebDriver (WebDriver Manager will handle binary path)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate and interact with the page
try:
    driver.get('https://www.example.com')
    input("Press Enter to continue...")  # Keep the window open until you press Enter
except Exception as e:
    print(e)
finally:
    driver.quit()
