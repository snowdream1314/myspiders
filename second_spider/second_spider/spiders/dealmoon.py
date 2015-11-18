# -*- coding: UTF-8 -*- 
'''
Created on 2015-10-13

@author: mushua
'''
import datetime
import json
import random
import re
from string import lower
import sys
import time
import urllib
import urlparse

import pymongo
from scrapy.spiders import Spider

from second_spider.conf.config import first_mongodb
from second_spider.items.item import Item
from second_spider.utils.color import Color
from second_spider.utils.net_util import loadHtmlSelector


# from pygments.lexers._postgres_builtins import SOURCE_URL
class dealmoon_Spider(Spider):
    '''
    classdocs
    '''
    name = "dealmoon"
    allowed_domains = ['baidu.com']
    start_urls = ["http://www.baidu.com/"]
    
    database = "dealmoon"
#     item_collection_name = "dealmoon_item_list"
#     mall_code = "dealmoon"
    
    mongodbitemlist = None
    
    def __init__(self, **kwargs):
#         self.mysqlDatabaseName = 'app_yunjiekou_ebusiness'
        super(dealmoon_Spider, self).__init__(**kwargs)
        
#         self.mongodbitemlist = ebusiness_mongodb[self.database][self.item_collection_name]
        
#         self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        
    def __str__(self):
        return "targetGrabSpider"
    
    def parse(self, response):
        
#         self.parseCategory()
        
        self.parseItemList()
        pass 


    def parseCategory(self):
        
        print "parseCategory"
        
        item_collection_name = "dealmoon_category"
        mongodbCategoryList = first_mongodb[self.database][item_collection_name]
        
        #清除数据库数据
#         mongodbCategoryList.remove()
#         print "remove over"

        url = "http://cn.dealmoon.com/"
        
        while 1 :
            
#             headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
            selector = loadHtmlSelector(url, headers=None)
            if selector is None : return
            reviews = selector.find("ul", {"class":"top_list"}).findAll("a", {"class":"more_arrow"})
            reviewhides = selector.find("ul", {"class":"top_list"}).find("div", {"class":"droplist wid_menu"}).findAll("span", {"class":None})
            id = 1
            
            for review in reviews :
                count = mongodbCategoryList.find({"item_id":id}).count() 
                if count == 0 :
                    name = review.find("s").get_text().strip()
                    href = review.attrs['href']
                    print id 
                    print name
                    print href
                    mongodbCategoryList.insert({"item_id":id, "item_name":name, "href":href})
                    id += 1
                else :
                    print "exit"
                    return
                
            for reviewhide in reviewhides :
                count = mongodbCategoryList.find({"item_id":id}).count()
                if count == 0 :
                    if id > 17 : return     #过滤不需要的分类
                    name = reviewhide.find("a", {"class":"wid105"}).get_text().strip()
                    href = reviewhide.find("a", {"class":"wid105"}).attrs['href']
                    print id 
                    print name
                    print href
                    mongodbCategoryList.insert({"item_id":id, "item_name":name, "href":href})
                    id += 1
                else :
                    print "exit"
                    return
            
        pass
    
    def parseItemList(self):
        
        print "parseItemList"
        
        item_collection_name = "dealmoon_category"
        mongodbItemList = first_mongodb[self.database][item_collection_name]
        sources = mongodbItemList.find()
        print "query ok"
        for source in sources :
#             if source['id'] < 15 : continue  #暂停，继续爬取
#             print source
            print source['item_name']
            print source['href']
            self.dealmoon(source)
                
        pass
    
    
    def dealmoon(self,source):#OK
        
        print "dealmoon"
        
        item_collection_name = "dealmoon_item"
        mongodbItem = first_mongodb[self.database][item_collection_name]
        
        #清除数据
#         mongodbItem.remove()
#         print "remove over" 

        clr = Color()   #CMD终端分颜色打印
        
        source_url = source['href']
        source_name = source['item_name']
        clr.print_red_text(source_url)
        clr.print_red_text(source_name)
        if source['item_id'] == 1 :
            source_url = "http://cn.dealmoon.com/Clothing-Jewelry-Bags/5"
#         print source_name
#         print source_url 
        
#         item = ShopItem()
#         item.categoryid = source['id']
        
        while 1 :
            
#             print source_url 
            clr.print_red_text(source_url)
            
            selector =  loadHtmlSelector(source_url, headers=None)
            if selector is None : return
            lists = selector.findAll("div", {"class":"mlist"})
            item_list = []
            
            for list in lists :
                
                item = Item()
                item.categoryid = source['item_id']
                
                #条目ID
                item.itemid = int (list.attrs['data-id'])
                print item.itemid
                
                #更新，直接跳到下一个分类
                item_num = mongodbItem.find({"itemid":item.itemid}).count()
#                 if item_num != 0 : return
                if item_num != 0 : continue     #暂停，继续爬取
                
                #条目标题
                if list.find("h2") :
                    item.name = list.find("h2").find("span", {"class":None}).get_text().strip()
                else :
                    item.name = list.find("h1").find("span", {"class":None}).get_text().strip()
#                 print item.name
                 
                #商品图片
                item.image = list.find("div", {"class":"mpic"}).find("img", {"alt":True}).attrs['src']       
                print item.image
                 
                #时间
                if not list.find("div", {"class":"date"}) : continue
                updatetimeitem = list.find("div", {"class":"date"}).get_text().strip()
                if "分钟".decode('utf-8') in updatetimeitem :     #时间格式为几分钟前
                    updatetime =  datetime.datetime.now() - datetime.timedelta(minutes= int (filter(lambda x:x.isdigit(),updatetimeitem)))
                    item.updatetime = time.mktime(updatetime.timetuple())
                elif "小时".decode('utf-8') in updatetimeitem :   #时间格式为几小时前
                    updatetime =  datetime.datetime.now() - datetime.timedelta(hours= int (filter(lambda x:x.isdigit(),updatetimeitem)))
                    item.updatetime = time.mktime(updatetime.timetuple())
                else :   #时间格式为几天前
                    updatetime = datetime.datetime.today() - datetime.timedelta(days= int (filter(lambda x:x.isdigit(),updatetimeitem)))
                    item.updatetime = time.mktime(updatetime.timetuple())
                print item.updatetime
                 
                #价格
                if list.find("h2") :
                    item.price = list.find("h2").find("a").find("span", {"class":"notice_item"}).get_text().strip()
                else :
                    item.price = list.find("h1").find("a").find("span", {"class":"notice_item"}).get_text().strip()       
#                 print item.price
                 
                #商城
                if list.find("h2") :
                    articleurl = list.find("h2").find("a").attrs['href']
                else :
                    articleurl = list.find("h1").find("a").attrs['href']
                    
                status = urllib.urlopen(articleurl).code
                if status == 404 :  #有个别链接失效
                    clr.print_red_text("return 404 error")
#                     print "return 404 error"
                    continue
                
                articleselector = loadHtmlSelector(articleurl, headers=None)
                originmall_text = articleselector.find("div", {"class":"gn_line"})
                if originmall_text :
                    originmall_text = originmall_text.find("a", {"style":"color:#003399;", "trk":None})
                    if originmall_text : 
#                 originmall = originmall_text[4:len(originmall_text)-6]      #提取商城名字
                        originmall = originmall_text.get_text().strip().replace("来自".decode('utf-8'),"").replace("的折扣".decode('utf-8'),"") #提取商城名字
                        originmallurl = originmall_text.attrs['href']
                    else :
                        originmall = ''
                        originmallurl = ''
                else :
                    originmall = ''
                    originmallurl = ''
                print originmall
                  
                #购买链接
                href = articleselector.find("div", {"class":"mpic"})
                if href :
                    item.href = "http://cn.dealmoon.com" + str (href.find("div", {"class":"buy"}).find("a", {"trk":True}).attrs['href'])
#                 if href :
#                     item.href = "http://cn.dealmoon.com" + str (href.attrs['href'])
                else :
                    item.href = ""
                    continue        #过滤没有购买链接的条目
                print item.href
                
                #推荐数
                goodcount = list.find("div", {"class":"minfo"}).find("span", {"class":"like_btn"})
                if goodcount :
                    goodcount = goodcount.find("em").get_text()
                    goodcountnum = int (filter(lambda x : x.isdigit(),goodcount))
                else :
                    goodcountnum = 0
                print "goodcountnum is %d" %goodcountnum        
                  
                #评论数 
                commentcount = list.attrs['cmtcn']
                commentcountnum = int (commentcount)
                print "commentcountnum is %d" %commentcountnum 
                
                #收藏数
                favcount = list.find("div", {"class":"minfo"}).find("span", {"class":"fav_btn"}).find("em").attrs['num']
                favcountnum = int (favcount)
                print "favcountnum is %d" %favcountnum
                
                dict = item.createItemdic({"articleurl":articleurl, "good_count":goodcountnum, "comment_count":commentcountnum, "fav_conut":favcountnum, "originmall":originmall, "originmallurl":originmallurl})
                print dict 
                
                #判断是否已经爬取
                num = mongodbItem.find({"itemid":item.itemid}).count()
                if num == 0 :
#                     item_list.append(dict)
                    mongodbItem.insert(dict)    #一次插入一条
                    clr.print_red_text("insert sucessfully")
#                     print "insert sucessfully"
                else :
                    clr.print_red_text("item exits, num is %s"  % num)
#                     print ("item exits, num is %s"  % num)
                    continue
             
            #一次插入整页所有条目
#             print item_list
#             if len(item_list) != 0 :  
#                 self.mongodbitemlist.insert(item_list)  
#                 print "insert successfully"   
             
            #下一页
            next_page = selector.find("div", {"class":"pages"}).find("a", {"class":"next_link"})
            if next_page :
                source_url = next_page.attrs['href']
            else :
                clr.print_red_text("exit")
#                 print "exit"
                break
                   
        pass
    
    
