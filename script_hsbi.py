import requests
import hashlib
import os
import yagmail
from dotenv import load_dotenv
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


logging.basicConfig(filename='script_hsbi.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Example logging
logging.info('Script started.')


# Load environment variables
load_dotenv()
EMAIL = os.getenv('EMAIL')  # Email username
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Email password
LOGIN_USERNAME = os.getenv('LOGIN_USERNAME') 
LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD') 

# Configuration
WEBSITE_NAME = 'HSBI' # for user email, has no semantic value
LOGIN_URL = 'https://www.hsbi.de/qisserver/rds?state=wlogin&login=in&breadCrumbSource=portal'
XPATH_LOGIN_USERNAME = '//*[@id="asdf"]'
XPATH_LOGIN_PASSWORD = '//*[@id="fdsa"]'
XPATH_LOGIN_BUTTON = '//*[@id="loginForm:login"]'
XPATH_BUTTON_STEP_2 = '//*[@id="wrapper"]/div[5]/div/ul/li[1]/a'
XPATH_BUTTON_STEP_3 = '//*[@id="makronavigation"]/ul/li[2]/a'
XPATH_BUTTON_STEP_4 = '//*[@id="wrapper"]/div[5]/table/tbody/tr/td/div/div[2]/div/form/div/ul/li[3]/a'
XPATH_BUTTON_STEP_5 = '//*[@id="wrapper"]/div[5]/table/tbody/tr/td/div/div[2]/form/ul/li/a[2]'

HASH_FILE = 'website_hash_hsbi.txt'
TO_EMAIL = 'vika.vovchenkoo@gmail.com'


def get_website_content():
    # Initialize Selenium WebDriver
    driver = webdriver.Chrome()

    try:
        # Step 1: Open the login page
        driver.get(LOGIN_URL)
        time.sleep(2)

        # Step 2: Enter username
        username_field = driver.find_element(By.XPATH, XPATH_LOGIN_USERNAME)
        username_field.send_keys(LOGIN_USERNAME)

        # Step 3: Enter password
        password_field = driver.find_element(By.XPATH, XPATH_LOGIN_PASSWORD)
        password_field.send_keys(LOGIN_PASSWORD)

        # Step 4: Click the login button
        login_button = driver.find_element(By.XPATH, XPATH_LOGIN_BUTTON)
        login_button.click()
        
        button_step_2 = driver.find_element(By.XPATH, XPATH_BUTTON_STEP_2)
        button_step_2.click()

        button_step_3 = driver.find_element(By.XPATH, XPATH_BUTTON_STEP_3)
        button_step_3.click()

        button_step_4 = driver.find_element(By.XPATH, XPATH_BUTTON_STEP_4)
        button_step_4.click()

        button_step_5 = driver.find_element(By.XPATH, XPATH_BUTTON_STEP_5)
        button_step_5.click()

        # Step 5: Wait for the login process to complete
        time.sleep(5)  # Adjust based on website behavior

        # Step 7: Get website content
        page_content = driver.page_source
        return page_content

    finally:
        # Ensure the driver is closed
        driver.quit()

def calculate_hash(content):
    """Calculate hash of the website content."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def load_previous_hash():
    """Load the previously stored hash from file."""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_current_hash(current_hash):
    """Save the current hash to a file."""
    with open(HASH_FILE, 'w') as f:
        f.write(current_hash)

def send_email(subject, body):
    """Send an email notification."""
    yag = yagmail.SMTP(EMAIL, EMAIL_PASSWORD)
    yag.send(to=TO_EMAIL, subject=subject, contents=body)

def main():
    try:
        # Fetch the website content and calculate its hash
        content = get_website_content()
        current_hash = calculate_hash(content)

        # Compare with the previous hash
        previous_hash = load_previous_hash()
        if previous_hash != current_hash:
            # Content has changed
            send_email("Website Updated", f"The website {WEBSITE_NAME} has been updated.")
            print("Website updated. Email sent.")
            save_current_hash(current_hash)
            logging.warning('Website content changed! Email notification sent.')
        else:
            print("No changes detected.")
            logging.info('Hash comparison successful. No change detected.')

    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error('An error occurred:', exc_info=True)

if __name__ == "__main__":
    main()
