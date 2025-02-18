📂 Recommended Folder Structure for Your Project

Breaking the project into separate scripts will make debugging way easier and help keep track of progress. Here's what I recommend:

/headlesstalkto
│── cookies/
│   ├── cookies.txt           # Netscape format cookies (exported from Firefox)
│   ├── cookies.pkl           # Converted cookies (for Selenium)
│   ├── cookie_expiration.txt # Expiration log
│
│── scripts/
│   ├── convert_cookies.py    # Convert Netscape cookies to Selenium format
│   ├── save_cookies.py       # Logs in manually and saves new cookies
│   ├── check_cookies.py      # Checks if login cookies are still valid
│   ├── ai_navigate.py        # Handles AI Studio navigation (chat input, button clicks)
│
│── main.py                   # The main script to run everything
│── requirements.txt           # Dependencies (Selenium, dotenv, etc.)
│── README.md                  # Guide on how to use everything


---

🚀 1️⃣ convert_cookies.py → Convert Netscape cookies to Selenium format

🔹 Purpose: Converts cookies.txt (Firefox format) into cookies.pkl (Selenium-compatible).
💡 Run this once after exporting cookies from Firefox.

import pickle

def convert_firefox_cookies(firefox_cookies_txt, output_file="cookies/cookies.pkl"):
    """Convert Firefox cookies.txt (Netscape format) to a Selenium-friendly format."""
    cookies = []
    with open(firefox_cookies_txt, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("#") or line.strip() == "":
                continue  # Skip comments and blank lines
            parts = line.strip().split("\t")
            if len(parts) < 7:
                continue  # Ignore malformed lines

            # Convert to Selenium format
            cookie = {
                "domain": parts[0],
                "path": parts[2],
                "secure": parts[3].lower() == "true",
                "expiry": int(parts[4]),
                "name": parts[5],
                "value": parts[6]
            }
            cookies.append(cookie)

    # Save as a pickle file for Selenium
    with open(output_file, "wb") as f:
        pickle.dump(cookies, f)
    
    print(f"✅ Converted {len(cookies)} cookies to Selenium format!")

# Run conversion
convert_firefox_cookies("cookies/cookies.txt")

📌 Run this whenever you get new cookies from Firefox.


---

🚀 2️⃣ save_cookies.py → Save Fresh Cookies from Manual Login

🔹 Purpose: Allows manual login and saves fresh cookies to cookies.pkl.
💡 Run this once to refresh cookies when they expire.

import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ✅ Setup Chrome
chrome_options = Options()
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ Open AI Studio
driver.get("https://aistudio.google.com/prompts/new_chat")
time.sleep(3)

# ❌ Turn OFF headless mode so you can log in manually
input("🔵 Log in manually, then press Enter...")

# ✅ Save Cookies
with open("cookies/cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)
print("✅ Fresh cookies saved to cookies.pkl!")

# ✅ Close Browser
driver.quit()

📌 Run this when cookie_expiration.txt says cookies are expired.


---

🚀 3️⃣ check_cookies.py → Detect Expired Login Cookies

🔹 Purpose: Checks if login cookies are still valid and logs expiration times.
💡 Run this daily or before launching your bot.

import pickle
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ✅ Setup Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ Open AI Studio
driver.get("https://aistudio.google.com/prompts/new_chat")
time.sleep(3)

# ✅ Load Cookies
cookies_file = "cookies/cookies.pkl"
login_cookies = ["SID", "_Secure-1PSID", "_Secure-3PSID", "SSID", "SAPISID"]  # Important login cookies

if os.path.exists(cookies_file):
    with open(cookies_file, "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    print("✅ Loaded cookies!")

# ✅ Refresh Page & Check Login
driver.get("https://aistudio.google.com/prompts/new_chat")
time.sleep(3)

# ✅ If Login Failed, Log It
if "Sign in" in driver.page_source:
    print("❌ Login failed! Authentication cookies might be expired.")

# ✅ Log Expiration Dates
with open("cookies/cookie_expiration.txt", "w") as log_file:
    for cookie in cookies:
        if cookie["name"] in login_cookies and "expiry" in cookie:
            expiry_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(cookie["expiry"]))
            log_file.write(f"{cookie['name']} expires on: {expiry_time}\n")
            print(f"📝 Logged {cookie['name']} - Expires: {expiry_time}")

# ✅ Close Browser
driver.quit()
print("📜 Expiration times saved in cookie_expiration.txt")

📌 Run this before launching the bot to make sure cookies are valid.


---

🚀 4️⃣ ai_navigate.py → Automate AI Studio (Typing & Clicking)

🔹 Purpose: Automates clicking, typing, and sending messages in AI Studio.
💡 Use this in main.py once cookies are valid.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def send_message(driver, message="Hello AI!"):
    """Finds the AI Studio input box and sends a message."""
    try:
        chat_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@class='textarea']"))
        )
        print("✅ Found chat input box!")

        chat_input.send_keys(message)
        chat_input.send_keys(Keys.RETURN)
        print(f"✅ Sent message: {message}")

    except Exception as e:
        print(f"❌ Error sending message: {e}")

📌 Use this function inside main.py to interact with AI Studio.


---

🚀 5️⃣ main.py → Run Everything

🔹 Purpose: This script brings everything together.

import check_cookies
import ai_navigate

# ✅ Check if cookies are still valid
check_cookies.run()

# ✅ If cookies are good, start automation
driver = start_driver()  # Start Selenium instance
ai_navigate.send_message(driver, "Hello AI!")

📌 Run main.py to check cookies & send messages.


---

📌 Summary: What Goes in the Folder


---

🚀 Final Step

✔ Build each script separately first, then combine into main.py.
✔ Test cookies before automating navigation (use check_cookies.py).
✔ Once login is stable, add clicking & typing.

📌 Try this structure and let me know if you get stuck! 🚀🔥
