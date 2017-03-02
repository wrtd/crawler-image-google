import json
import scrapy
import MySQLdb
import time
import datetime
import urllib

from array import *
from kafka import KafkaProducer, KafkaConsumer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.http import TextResponse
from pyvirtualdisplay import Display

class Yahoo(scrapy.Spider):
    # pdb.set_trace()
    name = "yahoo"
    allowed_domains = ["https://www.yahoo.com"]
    start_urls = ["https://www.yahoo.com"]

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
        self.driver.get("https://www.yahoo.com")
        time.sleep(1)
        keyword = ["pas foto", "pas foto 3x4", "pas foto 4x6", "pas foto ktp"]
        for a in range(len(keyword)):
            try:
                image = self.driver.find_element_by_xpath('//input[@id="UHSearchBox"]')
            except:
                try:
                    image = self.driver.find_element_by_xpath('//div[@id="sbq-wrap"]/input')
                except Exception, e:
                    print e
            image.click()
            time.sleep(1)
            image.send_keys(keyword[a])
            time.sleep(1)
            image.send_keys(Keys.ENTER)
            time.sleep(3)
            self.driver.find_element_by_xpath('//div[@class="compList mt-5"]/ul/li[2]/a').click()
            time.sleep(2)
            self.driver.find_element_by_xpath('//ul[@id="filt-tabs-v2"]/li[3]/ul/li[5]/a').click()
            time.sleep(2)
            count = 0
            for i in range(1, 10000):
                count += 1
                # import pdb;pdb.set_trace()
                try:
                    self.driver.find_element_by_xpath('/html/body').send_keys(Keys.END)
                    time.sleep(3)
                    response = TextResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
                    end = response.xpath('//section[@id="results"]/button/text()').extract()
                    link = response.xpath('//section[@id="results"]/div/ul/li[' + str(i) + ']/a/img/@src').extract()
                    link = ''.join(link).encode('utf-8')
                    link = link +'.jpg'
                    end = ''.join(end).encode('utf-8')
                    nama = str(keyword[a]).replace(' ', '_') + '_ke-' + str(count)
                    direktori = 'C:\Users\EB-NB19\Documents\pict\ ' + nama + '.jpg'
                    urllib.urlretrieve(link, direktori)
                    time.sleep(1)
                    print "=========================="
                    print nama
                    print "=========================="
                    if end == "Tampilkan Lebih Banyak Gambar":
                        self.driver.find_element_by_xpath('//section[@id="results"]/button').click()
                    else:
                        pass
                except Exception, e:
                    print e