# Import modules
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd
from flask import Flask, render_template
import pymongo
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_dict = {}

    # PART 1 - Scrape the news
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(2) # add delay to let the page fully load

    # Get the content title
    mars_dict["title"] = browser.find_by_css("div.content_title a").text
    mars_dict["body"] = browser.find_by_css("div.article_teaser_body").text
    
    
    # PART 2 - Scrape the image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(4) # add delay to let the page fully load
    
    full_image_btn = browser.find_by_id("full_image")
    full_image_btn.click()
    time.sleep(4) # add delay to let the page fully load
    
    more_btn = browser.links.find_by_partial_text('more info')
    more_btn.click()
    time.sleep(4) # add delay to let the page fully load
    
    more_info_html = browser.html
    img_soup = BeautifulSoup(more_info_html, 'html.parser')
    
    src_link = img_soup.select_one('figure.lede a img').get("src")
    featured_image_url = (f'https://www.jpl.nasa.gov{src_link}')
    
    # Get the content title
    mars_dict["url"] = featured_image_url
    
    
    # PART 3 - Current weather on Mars
    #mars_url = 'https://twitter.com/marswxreport?lang=en'
    browser.quit()
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit('https://twitter.com/marswxreport?lang=en')
    #html = browser.html
    #weather_soup = BeautifulSoup(html, 'html.parser')
    time.sleep(5)
    #results = weather_soup.find_all("div", { "data-testid" : "tweet" })
    #results = browser.find_by_css('div[data-testid="tweet"]') 
    mars_weather = browser.find_by_css('#react-root > div > div > div.css-1dbjc4n.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-1tlfku8.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div > div > div > div:nth-child(3) > section > div > div > div > div:nth-child(1) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > div:nth-child(2) > div:nth-child(1) > div > span')
    
    mars_weather = mars_weather[0].text
    print(f"+++++{mars_weather}")

    time.sleep(5)
    print("IRINA _ SLEEP")

    #spans = results.findAll('span') #, class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    time.sleep(5)
    print("spans found")

    # tweets_list = []
    # for span in spans:
        
    # # mars_weather = span.find('p').text
    #     if "InSight" in span.text: 
    #         tweets_list.append(span.text)
    #         break
    #     else:
    #         pass
    # mars_dict["weather"] = tweets_list
    # mars_dict["weather"] = results
    # mars_dict["weather"] = weather_soup.find_all('p',class_="tweet-text")[2].text
    mars_dict["weather"] = mars_weather
    browser.quit()

    
    # # PART 4 - Mars facts

    # facts_url = 'https://space-facts.com/mars/'
    # browser.visit(facts_url)
    # # html = browser.html
    # # soup = BeautifulSoup(html, 'html.parser')
    # df = pd.read_html(facts_url)
    # mars_table_df = df[1]
    # mars_table_df.columns = ['description', 'value']
    # mars_table_df = mars_table_df.to_frame()
    # html_table = mars_table_df.to_html(header = True, index = False)
    # # mars_dict['Description', 'Value'] = html_table
    # # mars_dict['table'] = html_table
    
    
    return mars_dict

