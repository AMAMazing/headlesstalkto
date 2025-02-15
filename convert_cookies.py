import json
import pickle

def convert_firefox_cookies(firefox_cookies_txt, output_file="cookies.pkl"):
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

# Run the conversion
convert_firefox_cookies("cookies.txt")
