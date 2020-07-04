from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
from pprint import pprint

def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p = mars_news(browser)

    data = {
        'news_title': news_title
        ,'news_p': news_p
        ,'featured_image': mars_image(browser)
        ,'hemispheres': mars_hemispheres(browser)
        ,'weather': mars_weather(browser)
        ,'facts': mars_facts(browser)
    }

    browser.quit()
    return data

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    slide = soup.find('li', class_='slide')
    news_p = slide.find('div',class_='article_teaser_body').text
    news_title = slide.find('div', class_='content_title').text
        
    return news_title, news_p

def mars_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=mars&category=#submit'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    full_image = browser.find_by_id('full_image')
    full_image.click()

    browser.is_element_present_by_text('more info', wait_time=1)
    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_image = soup.find('figure', class_='lede').a.get("href")

    featured_image_url = 'https://www.jpl.nasa.gov' + mars_image

    return featured_image_url

def mars_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')

    weather_tweet = weather_soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')

    for element in weather_tweet:
        if 'InSight' in element.text:
            mars_weather = element.text
            break
        
    return mars_weather

def mars_facts(browser):
    facts_df=pd.read_html('https://space-facts.com/mars/')[0]
    facts_df.columns=['Attribute', 'Value']
    facts_df.set_index('Attribute', inplace=True)
    
    return facts_df.to_html(classes='table table-striped')


def mars_hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hem = soup.find_all('h3')

    hemisphere_image_urls=[]

    for i in range(len(hem)):
        hemisphere = {}
        browser.find_by_css('h3')[i].click()
        #retrieve hemisphere name
        hemisphere['title'] = browser.find_by_css('h2').text
        #retrieve image url
        hem_url = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = hem_url['href']
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    return hemisphere_image_urls
if __name__ == "__main__":

    pprint(scrape_all())