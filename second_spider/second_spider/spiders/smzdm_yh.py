# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose: a spider grab information from "http://www.smzdm.com/youhui/"
# Author:
# Date: 2015-10-30
#-------------------------------------

import datetime
import time

from scrapy.spiders import Spider

from second_spider.conf.config import first_mongodb
from second_spider.items.item import Item
from second_spider.utils.color import Color
from second_spider.utils.net_util import loadHtmlSelector


class smzdm_yh_Spider(Spider):#OK
    '''
    classdocs
     
    '''
     
    print "smzdm_yh_Spider"
     
    name = "smzdmyh"
    start_urls = ['http://www.smzdm.com/youhui/']
    
    database = "smzdm"
    item_collection_name = None
    
    def __init__(self, **kwargs):
        pass
#         super(mgpyh_Spider, self)._init_(**kwargs)
        
#         self.mongodbitemlist = first_mongodb[self.database][self.item_collection_name]
        
    def parse(self,response):
        print "parse"
        
#         self.parseCategory()
        
        self.parseItemList()

    def parseCategory(self):
        
        print "parseCategory"
        
        item_collection_name = "smzdm_yh_category"
        mongodbCategoryList = first_mongodb[self.database][item_collection_name]
        
        #清除数据库数�?
#         mongodbCategoryList.remove()
#         print "remove over"
        
        url = "http://www.smzdm.com/youhui/"
        while 1 :
            
            selector = loadHtmlSelector(url, headers=None)
            if selector is None : return
            reviews = selector.findAll("div", {"class":"tab_info"})
            id = 1
            num = 1
            for review in reviews :
                if num == 2 :
                    categorys = review.findAll("a")
                    for category in categorys :
                        count = mongodbCategoryList.find({"item_id":id}).count()
                        if count == 0 :
                            name = category.get_text().strip()
                            href = category.attrs['href']
                            print id 
                            print name
                            print href
                            mongodbCategoryList.insert({"item_id":id, "item_name":name, "href":href})
                            id += 1
                        else :
                            print "exit"
                            return
                    num += 1
                else :
                    print num
                    num += 1
                    
    
    def parseItemList(self):
        
        print "parseItemList"
        
        item_collection_name = "smzdm_yh_category"
        mongodbItemList = first_mongodb[self.database][item_collection_name]
        
        sources = mongodbItemList.find()
        for source in sources :
#             if source['item_id'] < 2 :continue
            print source['item_name']
            print source['href']
            self.smzdm_yh(source) 
            
            
    def smzdm_yh(self, source):
        
        print "smzdm_yh"
        
        item_collection_name = "smzdm_yh_item"
        mongodbItem = first_mongodb[self.database][item_collection_name]
        
        clr = Color()   #CMD终端分颜色打�?
        
        #清除数据库数�?
#         mongodbItem.remove()
#         print "remove over"
        source_url = source['href']
#         if source['item_id'] == 13 :
#             source_url = "http://www.smzdm.com/youhui/fenlei/jiajujiazhuang/p17"
        source_name = source['item_name']
        clr.print_red_text(source_name)
        clr.print_red_text(source_url)
#         print source_name
#         print source_url 
        
        while 1 :
              
            print source_url 
                  
            selector = loadHtmlSelector(source_url, headers=None)
            if selector is None : return
            divs = selector.findAll("div", articleid=True)
            item_list = []
            for div in divs :
                
                item = Item()
                item.categoryid = source['item_id']
                   
                if div.find("div", {"class":"listTitle"}).find("span", {"class":"icon"}) : continue     #过滤过期条目
                          
                item.itemid = int (div.attrs['articleid'].split("_")[-1])
                print item.itemid
                
                #更新，直接跳到下�?个分�?
                item_num = mongodbItem.find({"itemid":item.itemid}).count()
                if item_num != 0 : 
                    clr.print_red_text("%s update over " %source_name)
#                     print "%s update over " %source_name
                    return
#                 if item_num != 0 : continue     #暂停，继续爬�?
                      
                item.updatetime = int (div.attrs['timesort'])
                updatetime = time.asctime(time.localtime(item.updatetime))
                article_time = datetime.datetime.strptime(updatetime,"%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%d %H:%M:%S %A")
                print item.updatetime
                print article_time
                      
                item.name = div.find("h2", {"class":"itemName"}).find("a").get_text().strip()
#                 print item.name
                    
#                 if "优惠�?".decode('utf-8') in item.name : continue 
#                 if "红包".decode('utf-8') in item.name : continue
#                 if "免费�?".decode('utf-8') in item.name : continue
#                 if "蚊子�?".decode('utf-8') in item.name : continue
#                 if "消费提示".decode('utf-8') in item.name : continue #过滤非商品条�?
#                 if "促销".decode('utf-8') in item.name : continue 
#                 if "活动".decode('utf-8') in item.name : continue
#                 if "�?么�?�得�?".decode('utf-8') in item.name : continue 
#                 if "公告".decode('utf-8') in item.name : continue 
#                 if "打车".decode('utf-8') in item.name : continue 
#                 if "公交".decode('utf-8') in item.name : continue 
#                 if "点券".decode('utf-8') in item.name : continue
#                 if "预告".decode('utf-8') in item.name : continue
#                 if "银行".decode('utf-8') in item.name : continue
#                 if "公益".decode('utf-8') in item.name : continue 
#                 if "专享".decode('utf-8') in item.name : continue
#                 if "晒物".decode('utf-8') in item.name : continue
#                 if "专题".decode('utf-8') in item.name : continue  
#                 if "白菜".decode('utf-8') in item.name : continue
#                 if "电信".decode('utf-8') in item.name : continue
#                 if "话费".decode('utf-8') in item.name : continue
#                 if "迅雷".decode('utf-8') in item.name : continue
#                 if "网友投稿".decode('utf-8') in item.name : continue
                        
                item.image = div.find("img", alt=True)      #商品图片
                if item.image :
                    item.image = item.image.attrs['src']
                    print item.image
                else :
                    item.image = ""
                    continue
                
                #商品价格      
                item.price = div.find("h2", {"class":"itemName"}).find("span", {"class":"red"}).get_text()      
#                 if item.price == '' : continue 
#                 if "红包".decode('utf-8') in item.price : continue
#                 if  item.price != '' and not re.search(r'\d', item.price) : continue        #过滤价格中没有数字的条目
#                 print item.price
                
                #购买链接      
                item.href = div.find("div", {"class":"buy"})    
                if item.href :
                    item.href =item.href.find("a", {"target":"_blank"}).attrs['href']
                    if "baoxian" in item.href : continue    #过滤保险类条�?
                    if "baidu" in item.href : continue
                    print item.href
                else :             
                    item.href = ""
                    continue  
                
                #商城
                originmallitem = div.find("div", {"class":"botPart"}).find("a", {"class":"mall"})
                if originmallitem :
                    originmall = originmallitem.get_text()   
                    originmallurl = originmallitem.attrs['href']
                    print originmall
                else : 
                    originmall = ""
                    originmallurl = ""
                
                #推荐�?      
                itemelse = div.find("div", {"class":"lrBot"})
                goodcount = itemelse.find("a", {"class":"good"}).find("span", {"class":"scoreTotal"}).attrs['value']
                goodcountnum = int(goodcount)   #�?
                print "goodcountnum is %d" %goodcountnum
                
                #不推荐数     
                badcount = itemelse.find("a", {"class":"bad"}).find("span", {"class":"scoreTotal"}).attrs['value']
                badcountnum = int(badcount)    #不�??
                print "badcountnum is %d" %badcountnum
                
                #收藏�?     
                favcount = itemelse.find("a", {"title":"收藏"}).find("em").get_text()
                favcountnum = int(favcount)     #收藏
                print "favcountnum is %d" %favcountnum
                
                #评论�?     
                commentcount = itemelse.find("a", {"class":"comment"}).get_text()
                commentcountnum = int(commentcount)     #评论
                print "commentcountnum is %d" %commentcountnum
                
                #文章链接
                article_url =  div.find("h2", {"class":"itemName"}).find("a").attrs['href']  
                print article_url
                  
                item_dict = item.createItemdic({"article_url":article_url, "article_time":article_time, "good_count":goodcountnum, "bad_count":badcountnum, "fav_count":favcountnum, "comment_count":commentcountnum, "originmall":originmall, "originmallurl":originmallurl})
                print item_dict 
                 
                #判断是否已经爬取     
                item_num = mongodbItem.find({"itemid":item.itemid}).count()
                if item_num == 0 :
#                     item_list.append(item_dict)
                    mongodbItem.insert(item_dict)
                    print "insert successfully"
                else :
#                     mongodbItem.update({"itemid":item.itemid}, item_dict)
#                     print "update over"
                    print ("item exits, num is %s"  % item_num)
                    continue
            
            #�?次插入整页所有条�?          
#             print item_list     
#             if len(item_list) != 0 :  
#                 mongodbItem.insert(item_list)  #�?次插入一页所有条�?
#                 print "insert successfully"
             
            #下一�?     
            next_page = selector.find("ul", {"class":"pagination"}).find("li", {"class":"pagedown"})
            if next_page :
                source_url = next_page.find("a").attrs['href']
            else :
                print "exit"
                break