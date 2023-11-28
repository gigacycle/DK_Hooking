import os
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


# Function to extract item information
def extract_item_info(html_content):
    soup_ = BeautifulSoup(html_content, 'html.parser')

    # Extract item link
    item_link = 'https://digikala.com' + (soup_.find('a', {'class': 'block'})['href'] if soup_.find('a', {'class': 'block'}) else '/No_link')

    # Extract image tag
    img_tag = soup_.find('img')
    if img_tag:
        # Extract image source
        image_src = urljoin(item_link, img_tag['src'])
        # Extract title from the alt property of img tag
        item_title = img_tag.get('alt', 'No title')
    else:
        item_title = 'No title'
        image_src = 'No image'

    return item_link, image_src, item_title


# Set up Selenium options
chrome_options = Options()
chrome_options.headless = True

# Provide the path to your ChromeDriver executable
chrome_path = "D:/Projects/Python Projects/chromedriver-win64/chromedriver.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\chrome.exe"
driver = webdriver.Chrome(service=ChromeService(executable_path=chrome_path), options=chrome_options)

# Example usage
url = "https://www.digikala.com/search/category-mobile-phone/product-list/?price%5Bmax%5D=747000000&price%5Bmin%5D=350000000"
driver.get(url)

# Wait for the page to load (you might need to adjust the sleep time)
time.sleep(30)

# Get the fully rendered HTML after JavaScript execution
page_content = driver.page_source

# Continue with your existing code to extract information
soup = BeautifulSoup(page_content, 'html.parser')
items = soup.find_all('div', class_='product-list_ProductList__item__LiiNI')

if os.path.exists('output.html'):
    os.remove('output.html')

# Create a new HTML file
with open('output.html', 'w', encoding='utf-8') as file:
    file.write("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Custom Digikala Product Viewer : </title>
        <style>body{margin:0;padding:0;font-family:Arial,sans-serif}header{background-color:#333;color:#fff;text-align:center;padding:10px}main{padding:20px}footer{background-color:#333;color:#fff;text-align:center;padding:10px;position:fixed;bottom:0;width:100%}.row{display:flex;margin-bottom:20px;border-bottom:1px solid #333}.row:last-child{border-bottom:none}.main-cell{margin-right:20px}.main-cell h4{max-width:300px;word-wrap:break-word}.main-cell img{border-radius:10px;max-width:300px;max-height:300px;display:block;margin:0 auto}.grid{display:grid;grid-template-columns:repeat(10,1fr);grid-gap:5px}.grid img{max-width:100px;max-height:100px;border:1px solid #ddd;border-radius:5px;display:block;margin:0 auto}</style>
    </head>
    <body>
        <header>
            <h1>Custom Digikala Product Viewer</h1>
        </header>
        <main>
    """)

    # Add item details to the HTML
    for item in items:
        item_link_, image_src, item_title = extract_item_info(str(item))
        images = []

        try:
            # Example usage
            driver.get(item_link_)
            # Wait for the page to load (you might need to adjust the sleep time)
            time.sleep(2)
            element = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, '[data-cro-id="pdp-album-open"]'))
            )
            # Click on the div
            element.click()
            time.sleep(2)
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')
            images = soup.find_all('img', class_='w-full bg-neutral-000 inline-block')
        except Exception as ex:
            print('Error while getting inner images : ' + ex.__str__())

        # Stream content to the HTML file
        file.write(f"""
        <div class="row">
            <div class="main-cell">
                <h4><a href='{item_link_}'>{item_title}</a></h2>
                <img alt='{item_title}' src='{image_src}'/>
            </div>
            <div class="grid">""")
        for img in images:
            file.write(f"""<div><a href='{img['src']}'>{img.__str__().replace('height="62"', 'height="100"').replace('width="62"', 'width="100"')}</a></div>""")
        file.write("""</div></div>""")

    # Close the HTML file
    file.write("""
    </main>
    <footer>
        <p>&copy; 2023 Gigacycle. All Rights Reserved.</p>
    </footer>
    </body>
    </html>
    """)

print("HTML file created: output.html")

# Close the WebDriver
driver.quit()
