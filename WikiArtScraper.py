from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
#from fake_useragent import UserAgent
import time
from random import randrange
#import functions
import random
import os
import sqlite3
from tqdm import tqdm
import pandas as pd
import shutil
import requests

from bs4 import BeautifulSoup
import re
import urllib


class WikiArtScraper:

    def __init__(self):
        self.browser = None
        self.xpath_num = None
        self.urls = []

        self.genres = ['https://www.wikiart.org//en/paintings-by-genre/abstract?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/advertisement?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/allegorical-painting?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/animal-painting?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/animation',
                     'https://www.wikiart.org//en/paintings-by-genre/architecture?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/artists-book',
                     'https://www.wikiart.org//en/paintings-by-genre/battle-painting?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/bijinga',
                     'https://www.wikiart.org//en/paintings-by-genre/bird-and-flower-painting?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/calligraphy?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/capriccio?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/caricature?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/cityscape?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/cloudscape?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/design?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/digital',
                     'https://www.wikiart.org//en/paintings-by-genre/figurative?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/flower-painting?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/furniture',
                     'https://www.wikiart.org//en/paintings-by-genre/genre-painting?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/graffiti?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/history-painting?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/icon?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/illustration?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/installation?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/interior?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/jewelry',
                     'https://www.wikiart.org//en/paintings-by-genre/landscape?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/literary-painting?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/manga',
                     'https://www.wikiart.org//en/paintings-by-genre/marina?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/miniature?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/mobile',
                     #'https://www.wikiart.org//en/paintings-by-genre/mosaic',
                     'https://www.wikiart.org//en/paintings-by-genre/mural',
                     'https://www.wikiart.org//en/paintings-by-genre/mythological-painting?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/nude-painting-nu?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/ornament',
                     #'https://www.wikiart.org//en/paintings-by-genre/panorama',
                     'https://www.wikiart.org//en/paintings-by-genre/pastorale',
                     'https://www.wikiart.org//en/paintings-by-genre/performance?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/photo?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/pin-up',
                     'https://www.wikiart.org//en/paintings-by-genre/portrait?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/poster?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/quadratura',
                     'https://www.wikiart.org//en/paintings-by-genre/religious-painting?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/sculpture?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/self-portrait?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/shan-shui',
                     'https://www.wikiart.org//en/paintings-by-genre/sketch-and-study?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/stabile',
                     'https://www.wikiart.org//en/paintings-by-genre/still-life?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/symbolic-painting?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/tapestry',
                     'https://www.wikiart.org//en/paintings-by-genre/tessellation?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/trompe-loeil',
                     'https://www.wikiart.org//en/paintings-by-genre/tronie?select=featured',
                     'https://www.wikiart.org//en/paintings-by-genre/utensil?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/vanitas',
                     'https://www.wikiart.org//en/paintings-by-genre/veduta?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/video-art',
                     'https://www.wikiart.org//en/paintings-by-genre/wildlife-painting?select=featured',
                     #'https://www.wikiart.org//en/paintings-by-genre/urushi-e',
                     #'https://www.wikiart.org//en/paintings-by-genre/augmented-reality',
                     #'https://www.wikiart.org//en/paintings-by-genre/object',
                     'https://www.wikiart.org//en/paintings-by-genre/yakusha-e?select=featured']

        return

    def run(self):
        for genre_url in self.genres:
            genre = genre_url.split('paintings-by-genre/')[1].replace('?select=featured', '')
            print(genre)
            self.get_genre_url(genre, genre_url)

        self.save_urls(filename='genres.csv')
        self.download_images('genres.csv')


    def download_images(self, filename, offset=0, limit=None):
        def soup_creator(url):
            # Downloads the WikiArt page for processing
            res = requests.get(url)
            # Raises an exception error if there's an error downloading the website
            res.raise_for_status()
            # Creates a BeautifulSoup object for HTML parsing
            return BeautifulSoup(res.text, 'lxml')

        def request_download_image(url, path):
            name = url.split('/')[-1]
            response = requests.get(url, stream=True)
            with open(path+'/'+name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

        df = pd.read_csv(filename)
        if limit == None: df = df[offset:]
        else: df = df[offset:limit]

        for i in tqdm(range(len(df.values))):
            genre, img_url = df.iloc[i]
            os.makedirs('./images/{}'.format(genre), exist_ok=True)
            soup = soup_creator(img_url)
            item = soup.findAll(attrs = {'itemprop': 'image'})[0]
            request_download_image(item['src'], './images/{}'.format(genre))


    def open_Chrome(self):
        optionsChrome = Options()
        # ua = UserAgent()
        # userAgent = ua.random
        # print(userAgent)
        # optionsChrome.add_argument(f'user-agent={userAgent}')
        optionsChrome.add_argument("--window-size=1920,1080");
        optionsChrome.add_argument("--start-maximized");
        optionsChrome.add_argument('--headless')
        optionsChrome.add_argument('--disable-gpu')  # Last I checked this was necessary.
        #optionsChrome = functions.get_Chrome_proxy(optionsChrome, proxy)
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=optionsChrome)
        print('browser opened')
        self.browser = browser
        return browser

    def get_xpath_num(self):
        for i in range(1, 50):
            try:
                load_more_button_path = "/html/body/div[2]/div[1]/section/main/div[{}]/div/div/div[1]/div/ul/li[2]/div[2]/a[1]".format(i)
                load_more_button = self.browser.find_element_by_xpath(load_more_button_path)
                break
            except:
                continue
        self.xpath_num = i
        return

    def get_genre_url(self, genre, genre_url):

        def scroll_to_bottom():
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        def get_n_images():
            n_images_path = "/html/body/div[2]/div[1]/section/main/div[{}]/div/div/div[2]/a/span[1]".format(self.xpath_num)
            n_images = self.browser.find_element_by_xpath(n_images_path).text

            print(n_images)

            try:
                n_images_loaded = int(n_images.split('-')[1].split(' ')[0].strip())
                max_images = int(n_images.split('of ')[1].strip())
            except:
                n_images_loaded = 10
                max_images = 10
            #print(n_images)
            print(n_images_loaded, max_images)
            return n_images_loaded, max_images

        def load_more_images():
            load_more_button_path = "/html/body/div[2]/div[1]/section/main/div[{}]/div/div/div[2]/a".format(self.xpath_num)
            load_more_button = self.browser.find_element_by_xpath(load_more_button_path)

            load_more_button.click()
            time.sleep(1)
            scroll_to_bottom()
            time.sleep(1)

        self.browser.get(genre_url)
        time.sleep(3)

        self.get_xpath_num()

        n_images_loaded = 0
        max_images = 100

        while n_images_loaded < max_images-60:
            n_images_loaded, max_images = get_n_images()
            try:
                load_more_images()
            except:
                pass

        for i in tqdm(range(1, max_images)):
            xpath_test = "/html/body/div[2]/div[1]/section/main/div[{}]/div/div/div[1]/div/ul/li[{}]/div[2]/a[1]".format(self.xpath_num, i)
            x = self.browser.find_element_by_xpath(xpath_test).get_attribute("href")
            self.urls.append((genre, x))

        #self.urls = urls
        return

    def show_urls(self):
        print(self.urls)
        return

    def save_urls(self, filename='test.csv'):
        df = pd.DataFrame(self.urls)
        df.to_csv(filename, index=False)
        return
