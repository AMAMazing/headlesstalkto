from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
import pickle

# ✅ Load environment variables
load_dotenv()
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

# ✅ Function to take a screenshot
def take_screenshot(driver, step_name="step"):
    filename = f"{step_name}.png"
    driver.save_screenshot(filename)
    print(f"📸 Screenshot saved: {filename}")

# ✅ Function to load valid cookies
def load_valid_cookies(driver, cookie_file="cookies.pkl"):
    """Load only valid (non-expired) cookies."""
    try:
        with open(cookie_file, "rb") as f:
            cookies = pickle.load(f)
            current_time = int(time.time())  # Get current Unix timestamp
            
            valid_cookies = []
            for cookie in cookies:
                if 'expiry' in cookie and cookie['expiry'] < current_time:
                    print(f"❌ Skipping expired cookie: {cookie['name']}")
                else:
                    valid_cookies.append(cookie)
                    driver.add_cookie(cookie)

            print(f"✅ Loaded {len(valid_cookies)} valid cookies!")
    except FileNotFoundError:
        print("❌ No cookies found! Please log in manually first.")

# ✅ Setup Selenium with Headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ Start ChromeDriver
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # ✅ Open AI Studio
    print("🔵 Opening AI Studio...")
    driver.get("https://aistudio.google.com/prompts/new_chat")
    time.sleep(3)
    take_screenshot(driver, "1_open_ai_studio")

    # ✅ Load cookies
    load_valid_cookies(driver)

    # ✅ Refresh the page to apply cookies
    print("🔄 Refreshing page to apply cookies...")
    driver.get("https://aistudio.google.com/prompts/new_chat")
    time.sleep(3)
    take_screenshot(driver, "2_after_cookie_load")

    # ✅ Test if login was successful
    page_title = driver.title
    if "AI Studio" in page_title:
        print("✅ Login successful, page title:", page_title)
    else:
        print("❌ Login failed, cookies might be expired.")

    take_screenshot(driver, "3_final_check")

    # ✅ Step 1: Click "New Chat" Button
    try:
        new_chat_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'New chat')]"))
        )
        new_chat_button.click()
        print("✅ Clicked 'New Chat' button!")
        take_screenshot(driver, "4_clicked_new_chat")

    except Exception as e:
        print(f"❌ Error clicking 'New Chat': {e}")

    # ✅ Step 2: Find Chat Input Box
    try:
        chat_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@class='textarea']"))
        )
        print("✅ Found chat input box!")
        take_screenshot(driver, "5_chat_box_found")

        # ✅ Step 3: Type and Send a Message
        chat_input.send_keys("Hello AI")
        chat_input.send_keys(Keys.RETURN)
        print("✅ Test message sent!")
        take_screenshot(driver, "6_message_sent")

    except Exception as e:
        print(f"❌ Error interacting with chat input: {e}")

finally:
    # ✅ Close browser
    driver.quit()
    print("🛑 Browser session closed.")
