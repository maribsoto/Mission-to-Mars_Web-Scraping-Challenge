# This is the Python script that comes from the Jupyter Notebook: mission_to_mars.ipynb
# Some variables were renamed for simplicity

# Import necessary libraries
import pandas as pd
import time

from splinter import Browser
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt

# Creating a function to scrape all the scraping code and returning a dictionary that 
# contains all the scraped data

def scrape_all():
    browser = Browser('chrome', executable_path='chromedriver', headless=True)

    news_title, news_paragraph = mars_news(browser)
    hem = hemispheres()

    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'weather' : mars_weather(browser),
        'facts': mars_facts(),
        'hem': hem,
        'last_modified': dt.now()
    }

    browser.quit()

    return mars_data

# This is the summarized scraping code that was created in the Jupyter Notebook: mission_to_mars

# Scraping Mars News
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

    html = browser.html
    news_soup = bs(html, 'html.parser')
    # Retrieving the news title and paragraph
    news_title = news_soup.find('div', class_='bottom_gradient').find('h3').get_text()
    news_p = news_soup.find('div', class_='article_teaser_body').get_text()

    return news_title, news_p

# Scraping Mars Featured Image
def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Retrieving the full image url after browsing through the website
    full_image = browser.find_by_id('full_image')[0]
    full_image.click()
    browser.is_element_present_by_text('more info', wait_time=1)

    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()

    html = browser.html
    img_soup = bs(html, 'html.parser')

    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# Scraping Mars Weather Details
def mars_weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Using the xpath to locate the weather twits
    x_path = "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div[2]/section/div/div/div[1]/div/div/div/div/article/div/div[2]/div[2]/div[2]/div[1]/div/span"
       
    if browser.is_element_present_by_xpath(x_path, wait_time = 5):
        twit = browser.find_by_xpath(x_path).text
    
    return twit

# Scraping Mars Facts
def mars_facts():
    url = 'https://space-facts.com/mars/'
    df = pd.read_html(url)[0]
    df.columns = ['Parameters', 'Values']

    return df.to_html(classes="table table-striped")

# Scraping Mars Hemispheres
def hemispheres():
    try: 
        browser = Browser('chrome', executable_path='chromedriver', headless=True)
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        html = browser.html
        
        hem_soup = bs(html, 'html.parser')

        base_url = 'https://astrogeology.usgs.gov' 
        
        #Defining the list that will contain dictionaries:
        hem = []  

        # Loop through the items stored in hems
        for item in range (4):
            time.sleep(5)
            
            browser.find_by_tag('h3')[item].click()
            
            html = browser.html
            hem_soup = bs(html, 'html.parser')
            
            title = hem_soup.find('h2', class_='title').text
            
            src = hem_soup.find("img", class_="wide-image")["src"]
            
            img_url = base_url + src
                            
            # Appending the hemispheres title and img_url into a list of dictionaries 
            hem.append({"title" : title, "img_url" : img_url})
    
        return hem

    finally:

        browser.quit()    

if __name__ == '__main__':

    print(scrape_all())
