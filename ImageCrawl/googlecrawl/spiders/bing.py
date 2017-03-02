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

class Bing(scrapy.Spider):
    # pdb.set_trace()
    name = "bing"
    allowed_domains = ["https://www.bing.com"]
    start_urls = ["https://www.bing.com"]

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
        self.driver.get("https://www.bing.com")
        time.sleep(1)
        self.driver.find_element_by_id('scpl1').click()
        time.sleep(1)
        keyword = ["pas foto", "pas foto 3x4", "pas foto 4x6", "pas foto ktp"]
        for a in range(len(keyword)):
            self.driver.find_element_by_xpath('//div[@class="b_searchboxForm"]/input[1]').send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            self.driver.find_element_by_xpath('//div[@class="b_searchboxForm"]/input[1]').send_keys(Keys.BACKSPACE)
            time.sleep(1)
            image = self.driver.find_element_by_xpath('//div[@class="b_searchboxForm"]/input[1]')
            image.click()
            image.send_keys(keyword[a])
            time.sleep(1)
            image.send_keys(Keys.ENTER)
            time.sleep(1)
            self.driver.find_element_by_xpath('//span[@title="People filter"]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//a[@title="Just faces"]').click()
            time.sleep(1)
            count = 0
            for x in range(1, 20):
                for a in range(1, 20):
                    for i in range(1, 40):
                        count += 1
                        response = TextResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
                        try:
                            # import pdb;pdb.set_trace()
                            response = TextResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
                            link = response.xpath('//div[@id="dg_c"]/div[' + str(x) + ']/div[' + str(a) + ']/div[' + str(i) + ']/div[1]/a/@m').extract()
                            link = ''.join(link).encode('utf-8')
                            photo = link.split("imgurl")[1]
                            photo = photo.split(",")[0]
                            photo = photo.split('"')[1]
                            nama = str(keyword[a]).replace(' ', '_') + '_ke-' + str(count)
                            direktori = 'C:\Users\EB-NB19\Documents\pict\ ' + nama + '.jpg'
                            urllib.urlretrieve(photo, direktori)
                            time.sleep(1)
                            print "=========================="
                            print nama
                            print "=========================="
                            self.driver.find_element_by_xpath('/html/body').send_keys(Keys.END)
                            time.sleep(1)
                        except Exception, e:
                            print e
                    try:
                        more = response.xpath('//div[@class="mm_seemore"]/a/text()').extract()
                        more = ''.join(more).encode('utf-8')
                        if more == "See more images":
                            self.driver.find_element_by_xpath('//div[@class="mm_seemore"]/a').click()
                        else:
                            pass
                    except Exception, e:
                        print e