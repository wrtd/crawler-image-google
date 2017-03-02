import json
import scrapy
import MySQLdb
import time
import datetime
import urllib
import os

from array import *
from kafka import KafkaProducer, KafkaConsumer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.http import TextResponse
from pyvirtualdisplay import Display

class Mark(scrapy.Spider):
    name = "ez"
    allowed_domains = ["https://www.google.com"]
    start_urls = ["https://www.google.com"]

    def __init__(self):
        # self.connect = self.conn
        # path_to_chromedriver = 'D://chromedriver'
        path = 'C://Program Files//Mozilla Firefox//firefox'
        # path_to_chromedriver='/usr/local/bin/chromedriver'
        # driver = webdriver.Chrome(executable_path=path_to_chromedriver)
        # display = Display(visible=0, size=(800, 600))
        # display.start()

        # driver = webdriver.Chrome(executable_path=path_to_chromedriver)
        self.driver = webdriver.Firefox(executable_path=path)
        self.driver.set_window_size(1280,720)
        # driver = webdriver.PhantomJS()

    def start_requests(self):
        self.driver.get("https://www.google.com")
        time.sleep(3)

        self.driver.find_element_by_xpath('//div[@id="gbw"]/div/div/div/div[2]/a').click()
        time.sleep(3)
        keyword = ["pas foto", "pas foto 3x4", "pas foto 4x6", "pas foto ktp"]
        now = datetime.datetime.now()
        folder = now.strftime("%d-%m-%Y")
        direktori = 'C:\Users\EB-NB19\Documents\pict\picture_google_' + str(folder)
        os.makedirs(direktori)
        for a in range(len(keyword)):
            image = self.driver.find_element_by_xpath('//div[@id="gs_lc0")]/input')
            image.click()
            image.send_keys(keyword[a])
            time.sleep(3)
            image.send_keys(Keys.ENTER)
            count = 0
            for i in range(1, 10000):
                count += 1
                try:
                    self.driver.find_element_by_xpath('//*[contains(@id, "rg_s")]/div[' + str(i) + ']/a').click()
                    time.sleep(3)
                    response = TextResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8')

                    # import pdb;pdb.set_trace()
                    try:
                        if i % 3 == 1:
                            link = response.xpath('//*[contains(@class, "irc_bg irc_land")]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/a/img/@src').extract()
                        elif i % 3 == 2:
                            link = response.xpath('//*[contains(@class, "irc_bg irc_land")]/div[2]/div[1]/div[3]/div[1]/div[2]/div[2]/a/img/@src').extract()
                        else:
                            link = response.xpath('//*[contains(@class, "irc_bg irc_land")]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/a/img/@src').extract()
                    except:
                        link = response.xpath('//*[contains(@class, "irc_bg irc_land")]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/a/img/@src').extract()

                    link = ''.join(link).encode('utf-8')
                    photo = str(keyword[a]).replace(' ', '_') + '_ke-' + str(count)
                    direktori_photo = direktori + photo + '.jpg'
                    urllib.urlretrieve(link, direktori_photo)
                    self.driver.find_element_by_xpath('//*[contains(@id, "irc_bg")]/div[2]/a').click()
                    time.sleep(3)
                    print "=========================="
                    print photo
                    print "=========================="
                except Exception, e:
                    print e