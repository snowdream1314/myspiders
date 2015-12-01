# from django.db import models

from second_spider.items.item import Item
from mongoengine import *
from mysite.settings import DBNAME


# from mongoengine import connect
# Create your models here.
connect(DBNAME, host='localhost', port=27017)

# class smzdm_fx(Document):
#     itemid = Item.itemid
#     categoryid = Item.categoryid
#     name = Item.name
#     image = Item.image
#     href = Item.href
#     brandname = Item.brandname
#     price = Item.price
#     originprice = Item.originprice
#     updatetime = Item.updatetime
#     bad_count = IntField()
#     
#     def createItemdic(self, dict2):
#         return Item.createItemdic(self, dict2)

class smzdm_fx(Document):
    itemid = IntField()
    categoryid = IntField()
    name = StringField()
    image = StringField()
    href = StringField()
    brandname = StringField()
    price = StringField()
    originprice = StringField()
    updatetime = IntField()
    bad_count = IntField()
    originmall = StringField()
    originmallurl = StringField()
    comment_count = IntField()
    good_count = IntField()
    fav_count = IntField()
    
    def createItemdic(self, dict2):
        return Item.createItemdic(self, dict2)


