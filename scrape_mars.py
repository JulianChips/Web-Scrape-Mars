from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

#Browser Setup
def browser_init():
    executable_path = {'executable_path': 'C:\\Users\\julia\\Desktop\\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = browser_init()
    #visit url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(0.5)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    news_title = soup.find("div", class_="content_title").find('a').text
    news_p = soup.find("div",class_="article_teaser_body").text
    print(news_title+": "+news_p)
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html,'lxml')
    featured_image_url = soup.find('img',class_="fancybox-image")['src']
    featured_image_url = "https://www.jpl.nasa.gov"+featured_image_url
    print(featured_image_url)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'lxml')
    mars_weather = soup.find('p',class_='TweetTextSize').text
    print(mars_weather)
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    mars_df = table[0]
    mars_df.columns = ['Fact Name','Fact']
    html_mars_table = mars_df.to_html(border=3, index=False)
    print(html_mars_table)
    hemisphere_image_urls = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemispheres = ["Cerberus","Schiaparelli","Syrtis","Valles"]
    for hemisphere in hemispheres:
        time.sleep(0.3)
        browser.click_link_by_partial_text(hemisphere)
        html = browser.html
        soup = BeautifulSoup(html,'lxml')
        image_url = soup.find('div',class_='downloads').find_all('li')[0].find('a')['href']
        hemisphere_title = soup.find('h2',class_='title').text
        hemisphere_image_urls.append({"title":hemisphere_title,"img_url":image_url})
        browser.back()
    print(hemisphere_image_urls)
    results = {
        "News_Title":news_title,
        "News_P":news_p,
        "Featured_Image": featured_image_url,
        "Weather": mars_weather,
        "Facts_Table":html_mars_table,
        "Hemisphere_Images":hemisphere_image_urls
    }
    browser.quit()
    return results