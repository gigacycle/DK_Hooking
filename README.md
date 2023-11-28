# DK_Hooking

DK_Hooking is a tool designed to streamline the extraction of Digikala products from a specified search page link.

## Overview

The primary goal of this project is to simplify the process of gathering information about products listed on Digikala.

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

Download `Chrome01.rar`, `Chrome02.rar`, `Chrome03.rar` and `chromedriver-win64.zip`. 
Then extract extract the contents of `Chrome01.rar` to a location of your choice. 
Extract the contents of `chromedriver-win64.zip` to a separate location.

### Installation

1. Open `main.py` in a text editor of your choice.
2. Set the path to the Chrome binary by updating `chrome_options.binary_location`. For example:
   ```python
   chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\chrome.exe"
3. Set the path to the ChromeDriver binary by updating chrome_path. For example:
   ```python
   chrome_path = "C:\\chromedriver-win64\\chromedriver.exe"
4. Install project dependencies by running:
   ```bash
    pip install -r requirement.txt

### Usage

1. Set the `url` in `main.py` to the desired webpage. For example:
   ```python
   url = "https://www.digikala.com/search/"
2. Run the main script to start
   ```bash
   python main.py
3. You have 30 seconds to scroll down the entire page in order to load more products.
