'''

Scraper that parse quotes from this website: https://quotes.toscrape.com (with logging function)

'''

# For Website scraping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests

# Other libs
import json
import time

def main():
    logging('Mistix', '12345678') # Loging function with username and password

    get_data() # Start scraping with bs4

def get_data():
       
    data = {'Information': []} # For storing data


    for num in range(1, 11): # Bypass website pagination
        url = f'https://quotes.toscrape.com/page/{num}/' 
        content = requests.get(url)
        
        # For each URL, get content
        soup = BeautifulSoup(content.text, 'html.parser')

        # Get main card with inner information
        cards = soup.find_all('div', class_='quote')

        # Check each card for inner tags
        for card in cards:
            text = card.find('span', class_='text').text.strip() # Quote
            author = card.find('small', class_='author').text.strip() # Author
            tags = card.find('meta', class_='keywords')['content'] # Tag
            bio_url = card.find_all('span') # Author biography

            # Pack all information into separate data list
            quote_data = {'Quote': text, 
                          'Author': author, 
                          'Bio URL': f"https://quotes.toscrape.com{bio_url[1].a['href']}", 
                          'Tags': tags}
            
            data['Information'].append(quote_data)

    # After scraping, pack data list into JSON file
            
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

        print("Information parsed") # Just for debug

def logging(username, password):
    url = 'https://quotes.toscrape.com/login' # Login URL
    
    # Using selenium, open Chrome driver and get all URL
    driver = webdriver.Chrome() 
    driver.get(url)

    # Get all fields to fill
    username_field = driver.find_element(By.CSS_SELECTOR, 'input[type="text"].form-control')
    password_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"].form-control')

    # Get button to submit information
    login_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"].btn.btn-primary')

    # Put username and password into each field
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Then click submit button
    login_button.click()

    # Wait
    time.sleep(1)

    # Just for debug
    print("Logged in")

    driver.quit()

if __name__ == "__main__":
    main()