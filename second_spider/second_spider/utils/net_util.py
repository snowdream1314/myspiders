#-*-coding:utf-8-*-
#-------------------------------------
# Name: 
# Purpose:  spider load net
# Author:
# Date: 2015-10-28
#-------------------------------------
from bs4 import BeautifulSoup
import httplib2


def loadHtmlSelector(url, method='GET', headers=None, contenttype='application/x-www-form-urlencoded', cookie=''):
    
    print "loadHtmlSelector"
    
    useragent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
    
#     if headers is  None :
#         headers = {"User-Agent":useragent, "content-type":contenttype, "Cookie":cookie}
    
    http = httplib2.Http(timeout=0.2)  
    response, content = http.request(url, method='GET', headers=headers)
    print str(response.status)
    return BeautifulSoup(content)