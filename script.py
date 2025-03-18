import os
import yagmail
import dns.resolver
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from guara.transaction import Application, AbstractTransaction
from guara import it, setup
import time

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
LOGIN_USERNAME = os.getenv("LOGIN_USERNAME")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")

# Configuration
LOGIN_URL = "https://www.hsbi.de/qisserver/rds?state=wlogin&login=in&breadCrumbSource=portal"
XPATHS = {
    "username": '//*[@id="asdf"]',
    "password": '//*[@id="fdsa"]',
    "login_button": '//*[@id="loginForm:login"]',
    "step_2": '//*[@id="wrapper"]/div[5]/div/ul/li[1]/a',
    "step_3": '//*[@id="makronavigation"]/ul/li[2]/a',
    "step_4": '//*[@id="wrapper"]/div[5]/table/tbody/tr/td/div/div[2]/div/form/div/ul/li[3]/a',
    "step_5": '//*[@id="wrapper"]/div[5]/table/tbody/tr/td/div/div[2]/form/ul/li/a[2]',
    "track_area": '//*[@id="wrapper"]/div[5]/table/tbody/tr/td/div/div[2]/form/table[2]/tbody',
}

CONTENT_FILE = "content_file.txt"
SMTP_PROVIDERS = {
    "gmail.com": {"host": "smtp.gmail.com", "port": 587, "use_ssl": False, "use_tls": True},
    "outlook.com": {"host": "smtp.office365.com", "port": 587, "use_ssl": False, "use_tls": True},
    "yahoo.com": {"host": "smtp.mail.yahoo.com", "port": 465, "use_ssl": True, "use_tls": False},
}


class LoginTransaction(AbstractTransaction):
    def do(self, **kwargs):
        self._driver.get(LOGIN_URL)
        time.sleep(1)
        self._driver.find_element(By.XPATH, XPATHS["username"]).send_keys(LOGIN_USERNAME)
        self._driver.find_element(By.XPATH, XPATHS["password"]).send_keys(LOGIN_PASSWORD)
        self._driver.find_element(By.XPATH, XPATHS["login_button"]).click()
        time.sleep(1)


class NavigateTransaction(AbstractTransaction):
    def do(self, **kwargs):
        for step in ["step_2", "step_3", "step_4", "step_5"]:
            self._driver.find_element(By.XPATH, XPATHS[step]).click()
            time.sleep(1)
        return self._driver.find_element(By.XPATH, XPATHS["track_area"]).get_attribute("outerHTML")


class SMTPSettingsTransaction(AbstractTransaction):
    def do(self, email):
        domain = email.split("@")[1]
        return SMTP_PROVIDERS.get(domain, SMTP_PROVIDERS["gmail.com"])


class LoadPreviousContentTransaction(AbstractTransaction):
    def do(self, **kwargs):
        if os.path.exists(CONTENT_FILE):
            with open(CONTENT_FILE, "r") as f:
                return f.read().strip()
        return None


class SaveCurrentContentTransaction(AbstractTransaction):
    def do(self, content):
        with open(CONTENT_FILE, "w") as f:
            f.write(content)


class SendEmailTransaction(AbstractTransaction):
    def do(self, subject, body):
        smtp_settings = SMTP_PROVIDERS.get(EMAIL.split("@")[1], SMTP_PROVIDERS["gmail.com"])
        yag = yagmail.SMTP(
            user=EMAIL,
            password=EMAIL_PASSWORD,
            host=smtp_settings["host"],
            port=smtp_settings["port"],
            smtp_ssl=smtp_settings["use_ssl"],
            smtp_starttls=smtp_settings["use_tls"],
        )
        yag.send(to=EMAIL, subject=subject, contents=body)


# Test case using Page Transactions
def main():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    app = Application(driver)
    app.at(LoginTransaction)
    content = app.at(NavigateTransaction).result
    previous_content = app.at(LoadPreviousContentTransaction).result

    if previous_content != content:
        app.at(SendEmailTransaction("Website Updated", "The tracked content has changed."))
        print("Website updated. Email sent.")
    else:
        print("No changes detected.")

    app.at(SaveCurrentContentTransaction(content))
    app.at(setup.CloseApp)

    return content


if __name__ == "__main__":
    main()
