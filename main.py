import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# ✅ Setup Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ Open AI Studio
driver.get("https://aistudio.google.com/prompts/new_chat")
time.sleep(3)

# ✅ Load Converted Cookies
try:
    with open("cookies.pkl", "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    print("✅ Loaded cookies!")
except FileNotFoundError:
    print("❌ No cookies found. Please log in manually first.")

# ✅ Refresh Page & Check Login
driver.get("https://aistudio.google.com/prompts/new_chat")
time.sleep(3)
driver.save_screenshot("login_test.png")

# ✅ Close Browser
driver.quit()
print("📸 Screenshot saved as login_test.png")
