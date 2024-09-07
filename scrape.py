from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

# Scraper WebDriver connection URL
SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")
print(f"SBR_WEBDRIVER: {SBR_WEBDRIVER}")  # Check if this prints the correct URL

if SBR_WEBDRIVER is None:
    raise ValueError("SBR_WEBDRIVER is not set. Please check your .env file.")

def scrape_website(website):
    print("Connecting to Scraping Browser...")

    # User-Agent Spoofing to avoid simple blocks
    options = ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")

    with Remote(sbr_connection, options=options) as driver:
        try:
            driver.get(website)
            print("Waiting captcha to solve...")

            # Check if captcha solving is required
            try:
                solve_res = driver.execute(
                    "executeCdpCommand",
                    {
                        "cmd": "Captcha.waitForSolve",
                        "params": {"detectTimeout": 10000},
                    },
                )
                print("Captcha solve status:", solve_res["value"]["status"])
            except Exception as e:
                print("No captcha or unable to solve:", str(e))

            print("Navigated! Scraping page content...")
            html = driver.page_source

            time.sleep(3)  # Allow the page to load properly
            return html
        except Exception as e:
            raise RuntimeError(f"Error scraping website: {str(e)}")
        finally:
            driver.quit()


def extract_body_content(html_content):
    """Extract body content from the HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    """Clean the body content by removing scripts and styles."""
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    """Split DOM content into chunks to avoid overload."""
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
