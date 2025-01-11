import requests
import hashlib
import os
import yagmail
from dotenv import load_dotenv
import logging

logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Example logging
logging.info('Script started.')


# Load environment variables
load_dotenv()
EMAIL = os.getenv('EMAIL')  # Email username
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Email password

# Configuration
WEBSITE_URL = 'https://coinmarketcap.com/'
HASH_FILE = 'website_hash.txt'
TO_EMAIL = 'vika.vovchenkoo@gmail.com'

def get_website_content(url):
    """Fetch website content."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch website content. Status code: {response.status_code}")

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
        content = get_website_content(WEBSITE_URL)
        current_hash = calculate_hash(content)

        # Compare with the previous hash
        previous_hash = load_previous_hash()
        if previous_hash != current_hash:
            # Content has changed
            send_email("Website Updated", f"The website {WEBSITE_URL} has been updated.")
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
