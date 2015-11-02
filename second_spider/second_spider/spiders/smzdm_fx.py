# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose: a spider grab information from "http://faxian.smzdm.com/"
# Author:
# Date: 2015-11-2
#-------------------------------------
import datetime
import re
import time

from scrapy.spiders import Spider

from second_spider.conf.config import first_mongodb
from second_spider.items.item import Item
from second_spider.utils.net_util import loadHtmlSelector


class smzdm_fx_Spider(Spider):
    '''
    classdocs
     
    '''
     
    print "smzdm_fx_Spider"
     
    name = "smzdmfx"
    start_urls = ['http://faxian.smzdm.com/']
    
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
        
        item_collection_name = "smzdm_fx_category"
        mongodbCategoryList = first_mongodb[self.database][item_collection_name]
        
        #清除数据库数据
#         mongodbCategoryList.remove()
#         print "remove over"
        
        url = "http://faxian.smzdm.com/"
        
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
        
        item_collection_name = "smzdm_fx_category"
        mongodbItemList = first_mongodb[self.database][item_collection_name]
        
        sources = mongodbItemList.find()
        for source in sources :
            print source['item_name']
            print source['href']
            self.smzdm_fx(source) 
            
            
    def smzdm_fx(self,source):
        
        print "smzdm_fx"
        
        item_collection_name = "smzdm_fx_item"
        mongodbItem = first_mongodb[self.database][item_collection_name]
        
        #清除数据库数据
#         mongodbItem.remove()
#         print "remove over"

        source_url = source['href']
        source_name = source['item_name']
        print source_name
        print source_url 
        
        while 1 :
            
            print source_url
            
            selector =  loadHtmlSelector(source_url, headers=None)
            if selector is None : return
            lists = selector.findAll("li", {"class":"list"})
#             print divs
            item_list = []
            for list in lists :
                
                item = Item()
                item.categoryid = source['item_id']      #分类ID  
                
                #条目ID
                item.itemid = int (list.attrs['articleid'].split("_")[-1])
                print item.itemid
                
                #更新，直接跳到下一个分类
                num = mongodbItem.find({"itemid":item.itemid}).count()
#                 if num != 0 : return    
                if num != 0 : continue  #暂停，继续爬取
                
                #时间  
                item.updatetime = int (list.attrs['timesort'])
                updatetime = time.asctime(time.localtime(item.updatetime))
                article_time = datetime.datetime.strptime(updatetime,"%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%d %H:%M:%S %A")
                print item.updatetime
                print article_time
                
                #条目名称  
                item.name = list.find("h2", {"class":"itemName"}).find("span", {"class":"black"}).get_text().strip()
                print item.name
                  
                if "优惠券".decode('utf-8') in item.name : continue    #过滤非商品条目
                if "活动".decode('utf-8') in item.name : continue
                if "专享".decode('utf-8') in item.name : continue
                  
                #商品图片  
                item.image = list.find("img", alt=True)     
                if item.image :
                    item.image = item.image.attrs['src']
                    print item.image
                else :
                    item.image = ""
                
                    continue
                #价格  
                item.price = list.find("h2", {"class":"itemName"}).find("span", {"class":"red"}).get_text()     
#                 if item.price == '' : continue 
                if "促销".decode('utf-8') in item.price : continue
                if "红包".decode('utf-8') in item.price : continue    #过滤非商品条目
                if  item.price != '' and not re.search(r'\d', item.price) : continue        #过滤价格中没有数字的条目
#                 print item.price
                
                #购买链接  
                item.href = list.find("div", {"class":"item_buy_mall"}).find("a", {"class":"directLink"}).attrs['href']     
                print item.href
                
                #推荐数  
                goodcount = list.find("div", {"class":"zan_fav_com"}).find("a", {"class":"zan"}).find("em").get_text()      #“值”数
                goodcountnum = int(goodcount)
                print "goodcountnum is %d" %goodcountnum        
                
                #评论数  
                commentcount = list.find("div", {"class":"zan_fav_com"}).find("a", {"class":"comment"}).get_text()      
                commentcountnum = int(commentcount)
                print "commentcountnum is %d" %commentcountnum
                
                #文章链接
                article_url =  list.find("h2", {"class":"itemName"}).find("a").attrs['href']  
                print article_url
                
                article_selector = loadHtmlSelector(article_url, headers=None)
                
                #商城
                originmall = article_selector.find("div", {"class":"article-meta-box"}).find("a", {"onclick":None})
                if originmall :
                    originmall = originmall.get_text()
                else :
                    originmall = ""
                print originmall
                
                #优惠力度
                youhui_content = article_selector.find("div", {"class":"item-box item-preferential"}).find("div", {"class":"inner-block"})
                if youhui_content :
                    youhui_content = youhui_content.find("p").get_text().replace("\t","").replace("\n", "").replace("\r", "").strip()
                else :
                    youhui_content = ""
#                 print youhui_content
                
                #爆料原文
                baoliao_content = article_selector.find("div", {"class":"item-box item-preferential"}).find("div", {"class":"baoliao-block"})
                if baoliao_content :
                    baoliao_content = baoliao_content.find("p").get_text().replace("\t","").replace("\n", "").replace("\r", "").strip()
                else :
                    baoliao_content = ""
#                 print baoliao_content
                
                #商品介绍
                item_description = ""
                item_descriptions = article_selector.findAll("div", {"class":"item-box"})
                if item_descriptions :
                    description_count = 1
                    for description in item_descriptions :
                        if description_count == 2 :
                            item_description = description.find("div", {"class":"inner-block"})
                            if item_description :
                                item_description = item_description.find("p")
                                if item_description :
                                    item_description = item_description.get_text().replace("\t","").replace("\n", "").replace("\r", "").strip()
                                else :
                                    item_description = ""
                            else :
                                    item_description = ""
                        description_count += 1
#                 print item_description
                
                #不推荐数
                badcount = article_selector.find("div", {"class":"score_rate"}).find("span", {"id":"rating_unworthy_num"}).get_text().strip()
                badcountnum = int(badcount)
                print "badcountnum is %d" %badcountnum
                
                #收藏数
                favcount = article_selector.find("div", {"class":"operate_box"}).find("div", {"class":"operate_icon"}).find("a", {"class":"fav"}).find("em").get_text()
                favcountnum = int(favcount)
                print favcountnum 
                  
                item_dict = item.createItemdic({"originmall":originmall, "baoliao_content":baoliao_content, "youhui_content":youhui_content, "item_description":item_description, "bad_count":badcountnum, "fav_count":favcountnum, "article_url":article_url, "article_time":article_time, "good_count":goodcountnum, "comment_count":commentcountnum})
                print item_dict 
                
                #判断是否已经爬取  
                num = mongodbItem.find({"itemid":item.itemid}).count()
                if num == 0 :
#                     item_list.append(item_dict)
                    mongodbItem.insert(item_dict)    #一次插入一个条目
                    print "insert successfully"
                else :
#                     mongodbItem.update({"itemid":item.itemid}, item_dict)
#                     print "update over"
                    print ("item exits, num is %s"  % num)
                    continue
            
            #一次插入一页所有条目      
#             print item_list
#             if len(item_list) != 0 :
#                 self.mongodbitemlist.insert(item_list) 
#                 print "insert successfully"  
              
            next_page = selector.find("ul", {"class":"pagination"}).find("li", {"class":"pagedown"})
            if next_page :
                source_url = next_page.find("a").attrs['href']
            else :
                print "exit"
                break