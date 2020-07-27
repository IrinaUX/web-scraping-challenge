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
    time.sleep(2) # add delay to let the page fully load
    
    full_image_btn = browser.find_by_id("full_image")
    full_image_btn.click()
    time.sleep(2) # add delay to let the page fully load
    
    more_btn = browser.links.find_by_partial_text('more info')
    more_btn.click()
    time.sleep(2) # add delay to let the page fully load
    
    more_info_html = browser.html
    img_soup = BeautifulSoup(more_info_html, 'html.parser')
    
    src_link = img_soup.select_one('figure.lede a img').get("src")
    featured_image_url = (f'https://www.jpl.nasa.gov{src_link}')
    
    # Get the content title
    mars_dict["url"] = featured_image_url
    
    
    # # PART 3 - Current weather on Mars
    # mars_url = 'https://twitter.com/marswxreport?lang=en'
    # browser.visit(mars_url)
    # html = browser.html
    # time.sleep(5)
    # soup = BeautifulSoup(html, 'html.parser')
    # tweets = soup.find_all('span') #, class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    # time.sleep(5)

    # tweets_list = []
    # for tweet in tweets:
    #     mars_weather = tweet.find('p').text
    #     if "InSight" in tweet.text: 
    #         # tweets_list.append(tweet.text)
    #         break
    #     else:
    #         pass
    # mars_dict["weather"] = tweets_list[0]
    
    
    return mars_dict

