# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy.spiders import Spider

from utils import load_content


class gzh_newrank_spider(Spider):
    name = "gzh_new"
    
    
    def __init__(self):
        self.allowed_domains = "baidu.com"
        self.start_urls = ["http://www.baidu.com/"]
    
    
    def parse(self, response):
        print "parse"
        
        self.parse_category()
        
        
    def parse_category(self):
        print "parse_category"
        
        url = "http://newrank.cn/public/info/list.html?type=data&period=day"
        selector = load_content(url, method='GET')
        if selector is None: return
        
        category_zixuns = selector.find("div", {"class":"zixun"}).findAll("li")
        for item in category_zixuns:
            print item.find("a").attrs['data']
        
        
        
        