from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

# ✅ Set ChromeDriver Path in .env
from dotenv import load_dotenv
load_dotenv()
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

# ✅ Setup Selenium with Headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ Start ChromeDriver
service = Service("/usr/local/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ Open AI Studio
driver.get("https://aistudio.google.com/prompts/new_chat")
time.sleep(3)

# ✅ Load Cookies from cookies.txt
cookies_path = "cookies.txt"  # Assuming cookies.txt is in the same folder
try:
    with open(cookies_path, "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 7:  # Ensure the line has the correct format
                cookie_domain = parts[0]  # Extract domain from cookie file
                cookie = {
                    "domain": cookie_domain,
                    "name": parts[5],
                    "value": parts[6],
                    "path": parts[2],
                    "secure": parts[3].lower() == "true",
                }

                print(f"🔵 Attempting to add cookie for domain: {cookie_domain}")

                # ✅ Ensure cookie matches current domain before adding
                if cookie_domain in driver.current_url:
                    driver.add_cookie(cookie)
                else:
                    print(f"❌ Skipping cookie - Domain mismatch: {cookie_domain} ≠ {driver.current_url}")

    print("✅ Cookies loaded successfully!")

except FileNotFoundError:
    print("❌ cookies.txt not found! Please make sure it's in the same folder.")

# ✅ Refresh the page to apply cookies
driver.get("https://aistudio.google.com/prompts/new_chat")

# ✅ Test if login was successful
time.sleep(3)  # Wait for page load
page_title = driver.title

if "AI Studio" in page_title:
    print("✅ Login successful, page title:", page_title)
else:
    print("❌ Login failed, cookies might be expired.")

# ✅ Close browser
driver.quit()
