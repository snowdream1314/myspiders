# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose: define database server
# Author:
# Date: 2015-10-28
#-------------------------------------

import pymongo

first_mongodb_domain = "localhost"
first_mongodb_port = 27017
first_mongodb = pymongo.MongoClient(first_mongodb_domain, first_mongodb_port)
