# Headless Talk To

A Python script for automated interaction with Google AI Studio using Selenium in headless mode.

## Prerequisites

- Python 3.x
- Google Chrome
- Chrome WebDriver
- A Google account with access to AI Studio

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/headlesstalkto.git
cd headlesstalkto
```

2. Install required Python packages:
```bash
pip install selenium python-dotenv
```

3. Install Google Chrome (if not already installed):
   - For Ubuntu/Debian:
     ```bash
     wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
     sudo dpkg -i google-chrome-stable_current_amd64.deb
     sudo apt-get install -f
     ```
   - For other operating systems, download from [Google Chrome website](https://www.google.com/chrome/)

4. Download ChromeDriver:
   - Download the ChromeDriver version that matches your Chrome version from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
   - Extract the chromedriver executable to `/usr/local/bin/chromedriver`
   - Make it executable:
     ```bash
     sudo chmod +x /usr/local/bin/chromedriver
     ```

## Configuration

1. Export your cookies from Google AI Studio:
   - Log into [AI Studio](https://aistudio.google.com/)
   - Use a browser extension like "Cookie-Editor" to export cookies
   - Save the exported cookies as `cookies.txt` in the project directory

2. Create a `.env` file (optional, as chromedriver path is now hardcoded):
```bash
CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
```

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Launch a headless Chrome browser
2. Navigate to AI Studio
3. Load cookies for authentication
4. Verify successful login
5. Close the browser

## Notes

- The script runs Chrome in headless mode, so no browser window will be visible
- Make sure your cookies are up to date if authentication fails
- The chromedriver path is hardcoded to `/usr/local/bin/chromedriver`

## Files

- `main.py`: Main script file
- `cookies.txt`: Your exported cookies (not included, must be added)
- `.env`: Environment variables (optional)
