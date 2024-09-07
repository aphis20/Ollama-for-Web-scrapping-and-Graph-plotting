AI Web Scraper
This project demonstrates a web scraping solution leveraging artificial intelligence, using a combination of Ollama Moondream, Selenium, and other Python tools. The scraper is designed to extract and process data from web pages efficiently.

Overview
The AI web scraper utilizes the following tools and libraries:

Ollama Moondream: A powerful AI language model integrated via langchain_ollama for natural language processing and data extraction.
Selenium: A browser automation tool that enables interaction with web pages. We use Remote and ChromeOptions from Selenium for browser control and ChromiumRemoteConnection for remote web driver connections.
BeautifulSoup: A library for parsing HTML and XML documents, used for extracting data from web pages.
python-dotenv: Manages environment variables, ensuring sensitive information like API keys are securely handled.
Setup
Install Dependencies

Ensure you have Python installed, then install the required libraries:

bash

pip install selenium beautifulsoup4 python-dotenv langchain_ollama
Environment Configuration

Create a .env file in the project root directory and set your environment variables. Example:

env

SBR_WEBDRIVER=wss://brd-customer-hl_66c4c249-zone-ai_scrapper:<enteer your own password>@brd.superproxy.io:9222
Use load_dotenv to load these variables into your script.

Usage
Initialize the Web Driver

Configure Selenium to connect to your remote web driver. Example:

python

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection

options = ChromeOptions()
options.add_argument('--headless')  # Run headless Chrome
driver = Remote(
    command_executor='http://<your-webdriver-url>',
    options=options
)
Create the AI Model

Set up the Ollama model for natural language processing:

python

from langchain_ollama import OllamaLLM

model = OllamaLLM()
Fetch and Parse Data

Use Selenium to navigate and fetch web page data:

python

driver.get('https://example.com')
page_source = driver.page_source
Parse the page using BeautifulSoup:

python

from bs4 import BeautifulSoup

soup = BeautifulSoup(page_source, 'html.parser')
Process Data with AI

Utilize the AI model to process and analyze the data:

python
Copy code
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate('Extract relevant information from the given HTML content.')
response = model.generate(prompt.format(page_source))
Clean Up

Close the web driver after the scraping process is complete:

python

driver.quit()
Example Code
Here is a complete example of the web scraper:

python

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
webdriver_url = os.getenv('SBR_WEBDRIVER')

options = ChromeOptions()
options.add_argument('--headless')
driver = Remote(
    command_executor=webdriver_url,
    options=options
)

driver.get('https://example.com')
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Processing with AI model can be added here

driver.quit()
