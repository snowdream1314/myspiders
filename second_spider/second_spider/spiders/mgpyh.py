#-*-coding:utf-8-*-
#-------------------------------------
# Name: 
# Purpose: try to write a spider
# Author:
# Date: 2015-10-28
#-------------------------------------

from bs4 import BeautifulSoup
import httplib2
from scrapy.spiders import Spider

from second_spider.conf.config import first_mongodb
from second_spider.items.item import Item
from second_spider.utils.net_util import loadHtmlSelector


# from second_spider.items import mgpyhItem
class mgpyh_Spider(Spider):
    '''
    classdocs
     
    '''
     
    print "mgpyh_spider"
     
    name = "mgpyh"
#     allow_domains = ['baidu.com']
    start_urls = ['http://www.mgpyh.com/']
    
    database = "mgpyh"
#     item_collection_name = "mgpyh_category"
    item_collection_name = None
#     mongodbitemlist = None 
    
    def __init__(self, **kwargs):
        pass
#         super(mgpyh_Spider, self)._init_(**kwargs)
        
#         self.mongodbitemlist = first_mongodb[self.database][self.item_collection_name]
        
    def parse(self,response):
        print "parse"
#         self.mongodbitemlist.insert({"name":"jck", "age":25, "tall":"175", "weight":65})
#         print self.mongodbitemlist.find({"name":"jim"})
#         print self.mongodbitemlist.find().count()
#         print "OK"

        #清数据库数据
#         self.mongodbitemlist.remove()
#         print "remove over" 

#         self.parseCategory()
        
        self.parseItemList()

    def parseCategory(self):#OK
        
        print "parseCategory"
        
        item_collection_name = "mgpyh_category"
        mongodbitemlist = first_mongodb[self.database][item_collection_name]
        
        #清数据库数据
#         mongodbitemlist.remove()
#         print "remove over"
        
        url = "http://www.mgpyh.com/"
        
        while 1 :
            
            print url
            
#             http = httplib2.Http(timeout=0.2)  
#             response, content = http.request(url, method='GET', headers={})
#             selector = BeautifulSoup(content)
            selector = loadHtmlSelector(url, headers=None)
            
            reviews = selector.find("ul", {"class":"pull-left menu-left"}).findAll("li",  {"data-id":True})
#             print reviews
            
            id = 1
            for review in reviews :
                num = mongodbitemlist.find({"item_id":id}).count()
                if num == 0 :
                    name = review.find("a").get_text().strip()
                    href =  "http://www.mgpyh.com" + str(review.find("a").attrs['href'])
                    print id 
                    print name
                    print href
                    mongodbitemlist.insert({"item_id":id, "item_name":name, "href":href})
                    id += 1
                else :
                    print "exit"
                    return
                
    def parseItemList(self):
        
        print "parseItemList"
        
        item_collection_name = "mgpyh_category"
        mongodb = first_mongodb[self.database][item_collection_name]
        
        sources = mongodb.find()
        for source in sources :
            print source['item_name']
            print source['href']
            self.mgpyh(source)
            
            
    def mgpyh(self,source):
        
        print "mgpyh"
        
        item_collection_name = "mgpyh_item"
        mongodbitemlist = first_mongodb[self.database][item_collection_name]
        
        #清除数据
#         self.mongodbitemlist.remove()
#         print "remove over"

        source_url = source['href']
        source_name = source['item_name']
        print source_name
        print source_url 
        
        pagenum = 1
        
        while 1 :
#             
            print source_url 
              
            selector =  loadHtmlSelector(source_url, headers=None)
            if selector is None : return
            lists = selector.findAll("div", {"class":"content-item clearfix"})
            item_list = []
            
            for list in lists :
                
                item = Item()
                item.categoryid = source['id']
                
                #条目ID 
                item.itemid = int (list.find("a", {"class":"favorite"}).attrs['data-id'])
                print item.itemid
                
#                 #更新，直接跳到下一个分类
#                 num = self.mongodbitemlist.find({"itemid":item.itemid}).count()
#                 if num != 0 : return
                
                #时间
                item.updatetime = int (list.attrs['data-timestamp'])
                print item.updatetime
               
                #条目名称
                item.name = list.find("h3").find("a").get_text().strip()
                print item.name
                 
                #商品图片
                item.image = list.find("img", {"alt":True})
                if item.image :
                    item.image = item.image.attrs['src']
                    print item.image        
                else :
                    item.image = ""

                #商品价格
                prices = list.find("h3").findAll("em", {"class":"number"})
                if prices !=[] :
                    item.price = ''
                    for price in prices :
                        item.price += price.get_text()
                else :
                    item.price = ''
#                     continue    #过滤没有价格的条目
                print item.price        
                
                #购买链接 
                item.href = "http://www.mgpyh.com" + str (list.find("div", {"class":"item-right"}).find("a", {"class":"mp-btn-red"}).attrs['href'])
                print item.href     
        
                itemicon = list.find("ol", {"class":"item-icon"})
                firecount = itemicon.find("a", {"title":True}).find("span", {"class":"count"}).get_text()
                firecountnum = int(firecount)
                print "firecountnum is %d" %firecountnum
                
                #收藏数
                favcount = itemicon.find("a", {"class":"favorite"}).find("span", {"class":"count"}).get_text()
                favcountnum = int(favcount)
                print "favcountnum is %d" %favcountnum      
                
                #评论数
                commentcount = itemicon.find("li").find("a", {"class":None, "data-id":None}).find("span", {"class":"count"}).get_text()
                commentcountnum = int(commentcount)
                print "commentcountnum is %d" %commentcountnum      
                
                item_dict = item.createItemDic({"fire_count":firecountnum, "fav_count":favcountnum, "comment_count":commentcountnum})
                print item_dict 
                 
                #判断是否已经爬取
                num = mongodbitemlist.find({"itemid":item.itemid}).count()
                if num == 0 :
                    item_list.append(item_dict)
                 
#                     self.mongodbitemlist.insert(dict)
#                     print "insert sucessfully"
                else :
                    print ("item exits, num is %s"  % num)
#                     continue
                    return      #退出,跳到下一个分类，有更新功能
            
            #一次插入整页所有条目
            print item_list
            if len(item_list) != 0 :
                mongodbitemlist.insert(item_list) 
                print "insert sucessfully"  
            pagenum += 1  
            source_url = source['href'] + "?page=" + str(pagenum)
#             if next_page :
#                 source_url = next_page.find("a").attrs['href']
#             else :
#                 print "exit"
#                 break
                   
        pass
        