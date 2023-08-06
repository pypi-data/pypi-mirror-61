# -*- coding: utf8 -*- 
import requests
import re # string resplit
from bs4 import BeautifulSoup # crawler main func
#from lxml import etree # crawler with xPath
import ast # string to dict
import pandas as pd # sort dict
import json, os # input, output json file # check file exist
import sys # stop as read last progress

# crawler with selenium through chrome
from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.chrome.options import Options # run without chrome show up
from selenium.webdriver.support.ui import WebDriverWait # run as complete loading
from selenium.webdriver.support import expected_conditions as EC # run as complete loading
from selenium.webdriver.common.by import By  # run as complete loading

# asyncio for asynchronous communication
#import aiohttp
#import asyncio

# avoid crawler error
from time import sleep # sleep as be block for over-visiting
#import httplib2 # html exist
#import urllib2 # html exist
from fake_useragent import UserAgent # random user agent
from random import choice # random choice
import socket

# shedule execute span
from datetime import datetime, date, timedelta
import time

# rss crawler
#import feedparser

TEST = False
PATH = '/Users/ritalliou/Desktop/IIS/News_Ideology/myCrawlerResult/politics/'
CHROME_PATH = '/Users/ritalliou/Desktop/IIS/News_Ideology/chromedriver'


class crawler(object):
    def __init__(self):
        self.output_file = None
        self.last_news_url = None
        self.proxies = []
        random_prox = self.get_random_proxies()
        self.proxy = {"http": random_prox, "https": random_prox, }
        requests.adapters.DEFAULT_RETRIES = 3   # reload times if fail
        self.session = requests.Session()  
        self.session.get('https://www.google.com.tw/', allow_redirects=False)
        #self.session.get('https://www.google.com.tw/', timeout=10, allow_redirects=False)   # load page to create cookie data and imitate browser

        # open a chrome browser for crawler
        opts = Options()
        opts.add_argument("--enable-javascript") # enable javascript        
        opts.add_argument("--incognito")  # non cookie browser
        opts.add_argument("user-agent="+str(UserAgent().random)) # random user agent
        opts.add_argument('--lang=zh-TW') # accepted language
        #opts.add_argument('--proxy-server=2.58.228.16:3128') # random proxy (ip_adress+port)
        #opts.add_argument('--no-sandbox') # bypass OS security model        
        #opts.add_argument("--headless") # no browser show up
        self.browser = webdriver.Chrome(CHROME_PATH, chrome_options=opts) # Optional argument, if not specified will search path.

        self.media_func = {"ltn": self.ltn_reader,    "appledaily": self.appledaily_reader,   "udn": self.udn_reader, "chinatimes": self.chinatimes_reader,   "tvbs": self.tvbs_reader,   "ettoday": self.ettoday_reader, "ttv": self.ttv_reader, "ctv": self.ctv_reader, "cts": self.cts_reader, "ftv": self.ftv_reader, "pts": self.pts_reader, "sten": self.sten_reader,   "ctitv": self.ctitv_reader, "era": self.era_reader, "ustv": self.ustv_reader,   "cna": self.cna_reader, "thenewslens": self.thenewslens_reader, "peoplenews": self.peoplenews_reader,   "upmedia": self.upmedia_reader, "epochtimes": self.epochtimes_reader,   "cmmedia": self.cmmedia_reader, "cnews": self.cnews_reader, "newtalk": self.newtalk_reader, "storm": self.storm_reader, "nownews": self.nownews_reader, "mirrormedia": self.mirrormedia_reader, "new7": self.new7_reader,   "taiwanhot": self.taiwanhot_reader, "rti": self.rti_reader, "worldjournal": self.worldjournal_reader,   "kairos": self.kairos_reader,   "mypeople": self.mypeople_reader,   "taronews": self.taronews_reader,   "yahoo": self.yahoo_reader, "pchome": self.pchome_reader}
        self.media_all_func = {}

    # crawler to get text by url and avoid https error
    def get_url_text(self, url):
        while 1:            
            try:
                self.session.keep_alive = False
                self.session.proxies = self.proxy
                self.session.headers = {'user-agent':str(UserAgent().random), 'accept-language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5'}
                res = self.session.get(url, allow_redirects=False)
                #res = self.session.get(url, timeout=10, allow_redirects=False)
                res.encoding = 'utf-8'
                return res.text            
            except Exception as e:
                print(e)
                random_prox = self.get_random_proxies()  # change proxy 
                print('Change proxy to '+random_prox)
                self.proxy = {"http": random_prox, "https": random_prox, }    
                continue

    # reopen chrome driver with new information
    def change_browser(self):
        self.browser.quit() # close existing browser
        opts = Options()
        opts.add_argument("--enable-javascript") # enable javascript        
        opts.add_argument("--incognito")  # non cookie browser
        opts.add_argument("user-agent="+str(UserAgent().random)) # random user agent
        opts.add_argument('--lang=zh-TW') # accepted language
        opts.add_argument('--proxy-server='+self.get_random_proxies()) # random proxy (ip_adress+port)
        self.browser = webdriver.Chrome(CHROME_PATH, chrome_options=opts) # open new browser


    # return random proxy (ip_address:port)
    def get_random_proxies(self):
        # get 20 proxy each time
        if self.proxies==[]:
            response = requests.get('https://free-proxy-list.net/')
            res = BeautifulSoup(response.text, features='lxml')
            ip_address_list = [element.text for element in res.select('td:nth-child(1)')[:20]]
            port_list = [element.text for element in res.select('td:nth-child(2)')[:20]]
            for ip, port in zip(ip_address_list, port_list): 
                self.proxies.extend([str(ip)+':'+str(port)])
        random_prox = choice(self.proxies)
        self.proxies.remove(random_prox)
        return random_prox


    # append news_dict to json file
    def append_2_json(self, list_of_dict):
        if len(list_of_dict)==0: return
        list_of_dict = sorted(list_of_dict, key=lambda k: k['time']) # sort time by acend
        #list_of_dict = [element for element in list_of_dict if date.today().strftime("%Y-%m-%d") in element['time']] # filter news today

        with open(self.output_file, 'ab+') as json_file:
            json_file.seek(0, os.SEEK_END) # Go to the end of file

            if json_file.tell() == 0: # file is empty
                json.dump(list_of_dict, json_file, indent=4, sort_keys=True)
            else:
                json_file.seek(-1, os.SEEK_END) # Move pointer 1 byte from the file end
                #json_file.seek(0, os.SEEK_SET) # Move pointer 1 byte from the file beginning
                json_file.truncate() # Remove the last character                
                for one_dict in list_of_dict:
                    json_file.write(',')
                    json.dump(one_dict, json_file, indent=4, sort_keys=True)
                json_file.write(']')


    #########################################################################
    ################################ 中國時報 ################################
    #########################################################################
    def chinatimes_all_reader(self):
        n = 1 # page in list
        while n < 15:
            print('================================ page: ' + str(n) + ' ================================')     
            url = 'https://www.chinatimes.com/politic/total?page='+str(n)+'&chdtv'
            drinks = []
            while drinks == []:
                text = self.get_url_text(url)
                soup = BeautifulSoup(text, "lxml")
                drinks = soup.select('{}'.format('.col'))

            all_news = []
            for drink in drinks: # .class # #id
                news_url = 'https://www.chinatimes.com' + drink.find('a').get('href') + '?chdtv'
                #print(news_url)
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.chinatimes_reader(news_url)
                    all_news.insert(0, news_dict)               
            n+=1
            self.append_2_json(all_news) # save as json file


    # read one chinatimes news, return dict {title, content, url, tag, time, related_news, recommend_news, media}
    def chinatimes_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')

        title = res.select('.article-title')[0].text.strip('\n')
        tag_list = [element.text for element in res.select('.article-hash-tag a')]
        author = [res.select('.author')[0].text.strip('\n').strip()] if res.select('.author a')==[] else [res.select('.author a')[0].text]

        context = ""
        for p in res.select('.article-body p'):
            if len(p.text) != 0 and p.text.find(u'(中時電子報)')==-1:
                #paragraph = (p.text.strip('\n').strip() + '\n')
                paragraph = (p.text.strip('\n').strip())
                #print(paragraph)
                context += paragraph
        
        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select('.meta-info-wrapper time')[0].get('datetime')
        date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]
        
        related_title = [element.text for element in res.select('.promote-word')] # 推廣連結 標題
        related_url = [element.get('href') for element in res.select('.promote-word a')] # 推廣連結 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        recommend_title = [element.text for element in res.select('.recommended-article ul h4')] # 推薦閱讀 標題
        recommend_url = [element.get('href') for element in res.select('.recommended-article ul h4 a')] # 推薦閱讀 url
        recommend_news = [dict([element]) for element in zip(recommend_title, recommend_url)]

        # video: {video_title:video_url}
        if res.find_all('figure', attrs={'data-media-type':'video'}) == []: video = []
        else:
            video_title = [element.find('div').get('data-href') for element in res.find_all('figure', attrs={'data-media-type':'video'})]
            video_url = [element.select('figcaption')[0].text for element in res.find_all('figure', attrs={'data-media-type':'video'})]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('.photo-container')==[]: img = [] # no img
        else:
            img_title = [element.find('img').get('alt') for element in res.select('.photo-container')]
            img_url = [element.find('img').get('src') for element in res.select('.photo-container')]
            img = [dict([element]) for element in zip(img_title, img_url)]          

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'中國時報'}
        print(title+' '+time)       
        return news_dict



    #########################################################################
    ################################ 自由時報 ################################
    #########################################################################
    def ltn_all_reader(self):
        n = 1 # page in list
        while n > 0:
            url = 'https://news.ltn.com.tw/ajax/breakingnews/politics/'+str(n)
            
            print('================================ page: ' + str(n) + ' ================================') 
            drinks = []
            while drinks == []:
                text = self.get_url_text(url)
                news_dict_data = json.loads(text) # turn dict in str to dict
                drinks = news_dict_data['data'] if n==1 else news_dict_data['data'].values()
            
            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink['url'].encode('utf-8')
                #print(news_url)
            
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    try:
                        news_dict = self.ltn_reader(news_url)
                        all_news.insert(0, news_dict)    
                    except Exception as e: print(e); continue           
            n+=1
            self.append_2_json(all_news) # save as json file
         


    def ltn_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')

        title = res.find('meta', attrs={'name':'og:title'})['content'].split(u' - ')[0]
        tag_list = res.find('meta', attrs={'name':'keywords'})['content'].split(u',')

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        if res.select('.whitecon .viewtime')!=[]:
            time_str = res.find('meta', attrs={'name':'pubdate'})['content'].strip('\n').strip()
            try:  date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ') # ex. 2019-09-20T05:30:00Z
            except Exception as e: date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S') # ex. 2019-09-20T05:30:00
        else:
            time_str = res.select('.time')[0].text.strip('\n').strip()
            try:  date_obj = datetime.strptime(time_str, '%Y/%m/%d %H:%M')
            except Exception as e: date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S') # ex. 2019-09-20T05:30:00
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        context = ""
        for p in res.select('.text p'):
            if len(p.text) !=0 and p.text.find(u'想看更多新聞嗎？現在用APP看新聞還可以抽獎')==-1 and p.text.find(u'／特稿')==-1:
                paragraph = (p.text.strip('\n').strip())
                context += paragraph
        if len(context.split(u'不用抽'))>1: context = context.split(u'不用抽 不用搶')[0]

        author = [context.split(u'〔')[1].split(u'／')[0]] if len(context.split(u'〔'))>1 else []

        related_title = [element.get_text() for element in res.select('.whitecon .related a') if element.get('href').find('http')==0] # 相關新聞 標題
        related_url = [element.get('href') for element in res.select('.whitecon .related a') if element.get('href').find('http')==0] # 相關新聞 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        recommend_news = []

        # video: {video_title:video_url}
        if res.select('#art_video') == []: video = []
        else:
            video_title = [element.get('alt') for element in res.select('#art_video')]
            video_url = ['https://youtu.be/'+element.get('data-ytid') for element in res.select('#art_video')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('.lightbox img, .articlebody .boxInput, .photo_bg img')==[]: img = [] # no img
        else:
            img_title = [element.get('alt') for element in res.select('.lightbox img, .articlebody .boxInput, .photo_bg img')]
            img_url = [element.get('src') for element in res.select('.lightbox img, .articlebody .boxInput, .photo_bg img')]
            img = [dict([element]) for element in zip(img_title, img_url)]          

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'自由時報'}
        print(title+' '+time)       
        return news_dict


    #########################################################################
    ############################ 聯合報 (2020大選) ############################
    #########################################################################
    def udn_all_reader_2020(self):
        url = 'https://udn.com/vote2020/president'
        text = self.get_url_text(url)
        soup = BeautifulSoup(text, "lxml")

        all_news = []
        # news that normal shows
        drinks = soup.select('#ptopic1 a, #ptopic2 a, #ptopic3 a')[1::2]
        for drink in drinks: # .class # #id
            news_url = drink.get('href')
            
            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                try:
                    news_dict = self.udn_reader_2020(news_url)
                    all_news.insert(0, news_dict)
                except Exception as e:
                    print(e); continue
        self.append_2_json(all_news)


    def udn_reader_2020(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')

        title = res.select(".article h1")[0].text        
        tag_list = res.find('meta', attrs={'name':'news_keywords'})['content'].split(u',')
        author = res.select('.article_info')[0].text
        author = author.split(u'記者')[1] if u'記者' in author else "".join(author.split(u' ')[3:])
        author = [author.split(u'╱')[0]] if u'╱' in author else [author.split(u'／')[0]]
        
        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'name':'date'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S') # ex. 2019-09-20 07:40:10
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        context = ""
        for p in res.select('p'):
            if len(p.text) != 0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph

        related_title = [element.text for element in res.select('#cate_1 h3')] # 相關新聞 標題
        related_url = [element.get('href') for element in res.select('#cate_1 a')[1::2]] ## 相關新聞 url # select odd elements to avoid repeat related urls
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        recommend_news = []

        # video: {video_title:video_url}
        if res.select('.video-container') == []: video = []
        else:
            video_title = [element.find('iframe').get('alt') for element in res.select('.video-container')]
            video_url = [element.find('iframe').get('src') for element in res.select('.video-container')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('.lazyloaded')==[]: img = [] # no img
        else:
            img_title = [element.get('alt') for element in res.select('.lazyloaded')]
            img_url = [element.get('src') for element in res.select('.lazyloaded')]
            img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'聯合報'}
        print(title+' '+time)       
        return news_dict



    #########################################################################
    ############################## 聯合報 (要聞) ##############################
    #########################################################################
    def udn_all_reader(self):
        self.browser.get('https://udn.com/news/breaknews/1/1#breaknews')   
        jsCode = "var q=document.documentElement.scrollTop=100000" # control distance of scroller on the right
        for x in range(0,15): 
            self.browser.execute_script(jsCode) # keep scrolling to the bottom
            sleep(2)
        text = self.browser.page_source
        soup = BeautifulSoup(text, "lxml")

        all_news = []
        drinks = soup.select('.area_body h2, .lazyload h2')
        for drink in drinks: # .class # #id
            news_url = 'https://udn.com' + drink.find('a').get('href').split('?from=udn-')[0]
            #print(news_url)        
            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                try:
                    news_dict = self.udn_reader(news_url)
                    all_news.insert(0, news_dict)
                except Exception as e:
                    print(e); continue 
        """
        # crawler with local html file
        import codecs
        f = codecs.open('/Users/ritalliou/Desktop/t_1.html', 'r', 'utf-8')
        f.encoding = 'utf-8'
        text = f.read()
        soup = BeautifulSoup(text, "lxml")
        drinks = soup.select('.listing a')
        n = 0; all_news = []
        for drink in drinks: # .class # #id
            news_url = 'https://udn.com' + drink.get('href')
            try:
                news_dict = self.udn_reader(news_url)
                all_news.insert(0, news_dict)
                n += 1
                if n%10==0:
                    self.append_2_json(all_news); print('output file')
                    all_news = []; n = 0
            except Exception as e:
                print(e); continue            
        self.append_2_json(all_news) # save as json file
        """
        
        
    def udn_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')

        title = res.select(".story_art_title")[0].contents[0].strip('\n')
        tag_list = res.find('meta', attrs={'name':'news_keywords'})['content'].split(u',')
        try:
            author = [res.select('.story_bady_info_author a')[0].text]
        except Exception as e:
            author = ['中央社']    # ex. 2019-11-21 14:23 中央社 台北21日電        

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'name':'date'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S') # ex. 2019-09-20 07:40:10
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        context = ""
        for p in res.select('#story_body_content p'):
            if len(p.text) != 0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph
        
        related_title = [element.text for element in res.select('.also_listing a[href*=relatednews] .also_title')] # 相關新聞 標題
        related_url = ['https://udn.com'+element.get('href') for element in res.select('.also_listing a[href*=relatednews]')] # 相關新聞 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        recommend_news = []

        # video: {video_title:video_url}
        if res.select('.video-container') == []: video = []
        else:
            video_title = [element.find('iframe').get('alt') for element in res.select('.video-container')]
            video_url = [element.find('iframe').get('src') for element in res.select('.video-container')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('.photo-story')==[]: img = [] # no img
        else:
            img_title = [element.find('figcaption').text for element in res.select('.photo-story')]
            img_url = [element.find('img').get('src') for element in res.select('.photo-story')]
            img = [dict([element]) for element in zip(img_title, img_url)]          

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'聯合報'}
        print(title+' '+time)       
        return news_dict

    #########################################################################
    ################################# TVBS ##################################
    #########################################################################
    def tvbs_all_reader(self):
        self.browser.get('https://news.tvbs.com.tw/politics')   
        jsCode = "var q=document.documentElement.scrollTop=100000" # control distance of scroller on the right
        for x in range(0,15): 
            self.browser.execute_script(jsCode) # keep scrolling to the bottom
            sleep(1)
        text = self.browser.page_source
        soup = BeautifulSoup(text, "lxml")
        
        all_news = []
        drinks = soup.select('.content_center_contxt_box_news ul li')
        for drink in drinks: # .class # #id
            news_url = 'https://news.tvbs.com.tw' + drink.find('a').get('href') 
            
            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                news_dict = self.tvbs_reader(news_url)
                all_news.insert(0, news_dict)
        self.append_2_json(all_news) # save as json file
        


    def tvbs_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  
        
        title = res.select('.title h1')[0].text.strip('\n')
        tag_list = [element.text for element in res.select('.adWords a')]
        author = [element.text for element in res.select('.leftBox1 a')]
        
        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'property':'article:published_time'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S+08:00') # ex. 2019-09-25T21:04:00+08:00
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        context = ""
        for p in res.select('#news_detail_div'):
            if len(p.text) != 0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph

        related_title = [element.text for element in res.select('.extended1 a')] # 延伸閱讀 標題
        related_url = ['https://news.tvbs.com.tw/politics/'+element.get('href') for element in res.select('.extended1 a')] # 延伸閱讀 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        recommend_news = []

        # video: {video_title:video_url}
        if res.select('#ytframe') == []: video = []
        else:
            video_title = [element.find('iframe').get('alt') for element in res.select('#ytframe')]
            video_url = [element.find('iframe').get('src') for element in res.select('#ytframe')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('#news_detail_div img')==[]: img = []
        else:
            img_title = [element.get('alt') for element in res.select('#news_detail_div img')]
            img_url = [element.get('data-src') for element in res.select('#news_detail_div img')]
            img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'TVBS'}
        print(title+' '+time)       
        return news_dict
        


    #########################################################################
    ############################ TVBS  (2020大選) ############################
    #########################################################################
    def tvbs_all_reader_2020(self):
        #https://news.tvbs.com.tw/eventsite/2020elections#golive
        n = 1
        while n < 6:
            url = 'https://news.tvbs.com.tw/pack/packdetail/424/'+str(n)
            print('================================ page: ' + str(n) + ' ================================')

            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            
            all_news = []
            drinks = soup.select('.pack_list_box')
            for drink in drinks: # .class # #id
                news_url = 'https://news.tvbs.com.tw' + drink.find('a').get('href')

                if news_url == self.last_news_url: # reach has read news
                        self.append_2_json(all_news)
                        raise SyntaxError("Read all news news")
                else:
                    news_dict = self.tvbs_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
        


    #########################################################################
    ################################ 蘋果日報 ################################
    #########################################################################
    def appledaily_all_reader(self):
        n = 1 # page in list
        while n < 6:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://tw.news.appledaily.com/politics/realtime/'+str(n)
            drinks = []
            while  drinks == []:
                res = requests.get(url)
                soup = BeautifulSoup(res.text, "lxml")
                drinks = soup.select('.abdominis ul li')
            
            all_news = []
            for drink in drinks: # .class # #id
                try:
                    news_url = 'https://tw.news.appledaily.com' + drink.find('a').get('href')
                    if news_url == self.last_news_url: # reach has read news
                        self.append_2_json(all_news)
                        raise SyntaxError("Read all news news")
                    else:
                        start_time = time.time()
                        print(news_url)
                        news_dict = self.appledaily_reader(news_url)
                        end_time = time.time(); print(end_time-start_time)
                        all_news.insert(0, news_dict)
                except Exception as e: print(news_url); continue                
            n+=1
            self.append_2_json(all_news) # save as json file
        
    # read one chinatimes news, return dict {title, content, url, tag, time, related_news, recommend_news, media}
    def appledaily_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml') 

        title = res.title.text.split(u' ｜ 蘋果新聞')[0]
        tag_list = [element.text for element in res.select('.ndgKeyword h3')]
        author = []

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = time = res.select(".ndArticle_creat")[0].text.replace(u"出版時間：","")
        date_obj = datetime.strptime(time_str, '%Y/%m/%d %H:%M')
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        context = ""
        for p in res.select('.ndArticle_contentBox .ndArticle_margin p'):
            if len(p) !=0 and p.text.find(u'allowTransparency')==-1 :
                paragraph = p.text.strip('\n').strip()
                context += paragraph        

        related_title = [element.text for element in res.select('.ndArticle_relateNews a')] # 相關新聞 標題
        related_url = [element.get('href') for element in res.select('.ndArticle_relateNews a')] # 相關新聞 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        recommend_news = []

        # video: {video_title:video_url}
        if res.select('#videobox') == []: video = []
        else:
            video_title = [None for element in res.select('#videobox')]
            video_url = [element.text.split(u'videoUrl = ')[1].split(u';')[0] for element in res.select('#videobox')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('.ndAritcle_headPic img, .ndArticle_margin img')==[]: img = []
        else:
            img_title = [element.get('alt') for element in res.select('.ndAritcle_headPic img, .ndArticle_margin img')]
            img_url = [element.get('src') for element in res.select('.ndAritcle_headPic img, .ndArticle_margin img')]
            img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'蘋果日報'}
        print(title+' '+time)       
        return news_dict

        


    #########################################################################
    ################################ ETtoday ################################
    #########################################################################
    def ettoday_all_reader(self):
        self.browser.get('https://www.ettoday.net/news/focus/%E6%94%BF%E6%B2%BB/')   
        jsCode = "var q=document.documentElement.scrollTop=100000" # control distance of scroller on the right
        for x in range(0,15): 
            self.browser.execute_script(jsCode) # keep scrolling to the bottom
            sleep(1)
        text = self.browser.page_source

        all_news = []
        res = BeautifulSoup(text, features='lxml')
        drinks = res.select('.block_content .part_pictxt_3 .piece')
        print(len(drinks))
        
        for drink in drinks: # .class # #id
            news_url = 'https://www.ettoday.net' + drink.find('a').get('href')
            
            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                try: news_dict = self.ettoday_reader(news_url)
                except Exception as e: # prevent link to ETtoday's other platform
                    print(news_url)
                    continue
                all_news.insert(0, news_dict)
        self.append_2_json(all_news) # save as json file
        

        
    def ettoday_reader(self, url):      
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  
        
        title = res.select('.subject_article h1')[0].text
        tag_list = res.find('meta', attrs={'name':'news_keywords'})['content'].split(u',')
        author = [json.loads(res.select('script')[0].text.replace('\r\n',"").replace(" ",""))['creator'][0].split(u'-')[1]] # turn dict in str to dict

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta',attrs={'property':'article:published_time'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:00+08:00') # ex. 2019-10-01T12:04:00+08:00
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        context = ""
        for p in res.select('.subject_article p'):
            if len(p) !=0 and p.text.find(u'【更多新聞】')==-1 and p.text.find(u'本文版權所有')==-1 and p.text.find(u'關鍵字')==-1:
                paragraph = p.text.strip('\n').strip()
                context += paragraph
            else: break        

        related_title = [element.text for element in res.select('.related-news h3')] # 相關新聞 標題
        related_url = ['https:'+element.get('href') for element in res.select('.related-news a')] # 相關新聞 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        recommend_title = [element.text for element in res.select('.part_list_3')[0].select('a')] # 推薦閱讀 標題
        recommend_url = ['https://www.ettoday.net'+element.get('href') for element in res.select('.part_list_3')[0].select('a')] # 推薦閱讀 url
        recommend_news = [dict([element]) for element in zip(recommend_title, recommend_url)]

        # video: {video_title:video_url}
        if res.select('.story iframe') == []: video = []
        else:
            video_title = [element.get('alt') for element in res.select('.story iframe')]
            video_url = [element.get('src') for element in res.select('.story iframe')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('.story img')==[]: img = []
        else:
            img_title = [element.get('alt') for element in res.select('.story img')]
            img_url = [element.get('src') for element in res.select('.story img')]
            img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'ETtoday'}
        print(title+' '+time)       
        return news_dict

        


    #########################################################################
    ################################ 台視 ################################
    #########################################################################
    def ttv_all_reader(self):
        n = 1 # page in list
        news_queue = []; news_titles = []
        while n < 14:
            #print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.ttv.com.tw/news/catlist.asp?page='+str(n)+'&Cat=A&NewsDay='
            drinks=[]
            while drinks==[]:
                text = self.get_url_text(url)
                soup = BeautifulSoup(text, "lxml")
                drinks = soup.select('.panel-body ul li')

            for drink in drinks: # .class # #id
                if drink.find('a').text not in news_titles:
                    news_titles.append(drink.find('a').text)
                    a = drink.find('a').get('href')
                    news_url = 'https://www.ttv.com.tw/news/view/'+a.split('=')[1].split('&')[0]+'/'+a.split('=')[2]
                    if news_url == self.last_news_url: # reach has read news
                        break
                    else:
                        news_queue.append(news_url) # store url in each page
            n+=1
        all_news = []
        for news_url in  list(set(news_queue)):
            try:
                news_dict = self.ttv_reader(news_url)
                all_news.insert(0, news_dict)
                if len(all_news)%10==0: 
                    self.append_2_json(all_news)
                    print('output to file')
                    all_news = []
            except Exception as e:
                print(e); continue
            finally:
                self.append_2_json(all_news) # save as json file
            
            
        
    def ttv_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')

        title = res.title.text.split(u' - 台視新聞')[0]
        tag_list = res.find('meta', attrs={'name':'keywords'})['content'].split(u',')
        author = []
            
        context = ""
        for p in res.select('.panel-body .content .br'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'http-equiv':'last-modified'})['content']
        date_obj = datetime.strptime(time_str, '%a, %d %b %Y %H:%M:%S UTC') # ex. "Mon, 29 Jul 2019 07:45:51 UTC"
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        related_title = [element.text for element in res.select('.panel-body .br2x p')] # 相關新聞 標題
        related_url = [element.get('href') for element in res.select('.panel-body .br2x a')] # 相關新聞 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        recommend_news = []

        # video: {video_title:video_url}
        if res.select('.embed-responsive-item') == []: video = []
        else:
            video_title = [element.get('alt') for element in res.select('.embed-responsive-item')]
            video_url = [element.get('src').split(u'?rel=')[0] for element in res.select('.embed-responsive-item')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('.p100')==[]: img = []
        else:
            img_title = [element.get('alt') for element in res.select('.p100')]
            img_url = [element.get('src') for element in res.select('.p100')]
            img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'台視'}
        print(title+' '+time)       
        return news_dict
    
        

    #########################################################################
    ################################ 中視 ################################
    #########################################################################
    def ctv_all_reader(self):
        n = 1 # page in list
        while n > 0:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'http://new.ctv.com.tw/Category/%E6%94%BF%E6%B2%BB?PageIndex='+str(n)
            drinks = []
            while drinks == []:
                res = requests.get(url)
                soup = BeautifulSoup(res.text, "lxml")
                drinks = soup.select('.threeColumn .list a')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = 'http://new.ctv.com.tw'+drink.get('href')    

                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    try:
                        news_dict = self.ctv_reader(news_url)
                        all_news.insert(0, news_dict)
                    except Exception as e:
                        print(e); continue                    
            n+=1
            self.append_2_json(all_news) # save as json file
         

        
    def ctv_reader(self, url):  
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')        
        
        title = res.title.text.split(u'│中視新聞')[0]
        tag_list = [element.text for element in res.select('.tag')]
        author = [res.select('.author')[0].text.split(u' | ')[0]]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select('.new .author')[0].text.split(u'中視新聞 | ')[1].replace("-", "/") 
        date_obj = datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S') # ex. "2019/07/29"
        time = date_obj.strftime("%Y/%m/%d")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        context = ""
        for p in res.select('.new .editor'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph

        related_news = []
        recommend_news = []

        # video: {video_title:video_url}
        if res.select('.new iframe') == []: video = []
        else:
            video_title = [element.get('alt') for element in res.select('.new iframe')]
            video_url = [element.get('src') for element in res.select('.new iframe')]
            video = [dict([element]) for element in zip(video_title, video_url)]

        # img: {img_title:img_url}
        img_title = [None]
        img_url = [res.find('meta', attrs={'property':'og:image:url'})['content']]
        img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'中視'}
        print(title+' '+time)       
        return news_dict

        


    #########################################################################
    ################################ 華視 ################################
    #########################################################################
    def cts_all_reader(self):
        url = 'https://news.cts.com.tw/politics/index.html'
        text = self.get_url_text(url)
        soup = BeautifulSoup(text, "lxml")
        drinks = soup.select('.left-container .newslist-container a')
            
        all_news = []
        for drink in drinks: # .class # #id
            news_url = drink.get('href')

            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                try:
                    news_dict = self.cts_reader(news_url)
                    all_news.insert(0, news_dict)
                except Exception as e:
                    print(e); continue                
        self.append_2_json(all_news) # save as json file
        
        
        
    def cts_reader(self, url):      
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')        
        
        tag_list = [element.text for element in res.artical.select('.news-tag a')]
        title = res.title.text.split(u' - 華視新聞網')[0]
       
        author =  None
        author_text = res.select('.artical-content p')[0].text.split(u'  / ')[0]
        if u'綜合報導' in author_text and len(author_text.split(u'綜合報導'))>1: author = author_text.split(u'綜合報導')[0].split(u' ')[:-1] # ex. 林仙怡 綜合報導 or 林仙怡 施幼偉 綜合報導
        elif u'華視新聞 ' in author_text: author =  filter(None, author_text.split(u'華視新聞')[1].split(u' ')[:-1])    # ex. 華視新聞 林仙怡 施幼偉 台北報導
        else: author = [author_text]  # ex. 綜合報導
        
        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str =  res.artical.select('.artical-time')[0].text
        date_obj = datetime.strptime(time_str, '%Y/%m/%d %H:%M') # ex. "2019/09/30 10:00"
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        context = ""
        for p in res.artical.select('.artical-content p'):
            if len(p) !=0 and p.text.find(u'新聞來源：')==-1:
                paragraph = p.text.strip('\n').strip()
                context += paragraph

        related_title = [element.text for element in res.artical.select('.newsingle-rel p')] # 延伸閱讀 標題
        related_url = [element.get('href') for element in res.artical.select('.newsingle-rel a')] # 延伸閱讀 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        recommend_news = []

        # video: {video_title:video_url}
        if res.select('.artical-content iframe') == []: video = []
        else:
            video_title = [element.get('alt') for element in res.select('.artical-content iframe')]
            video_url = [element.get('src') for element in res.select('.artical-content iframe')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('.artical-img') == []:    # no img in article, default cover img
            img_title = [None]
            img_url = [res.find('meta', attrs={'property':'og:image'})['content']]
        else: 
            img_title = [element.find('img').get('alt').split(u' | 華視新聞')[0] for element in res.select('.artical-img')]
            img_url = [element.find('img').get('src') for element in res.select('.artical-img')]
        img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'華視'}
        print(title+' '+time)       
        return news_dict

        


    #########################################################################
    ############################ 華視 (2020大選)  #############################
    #########################################################################
    def cts_all_reader_2020(self):
        url = 'https://news.cts.com.tw/topic/1227/'
        text = self.get_url_text(url)
        soup = BeautifulSoup(text, "lxml")
        drinks = soup.select('.newslist-container a')
            
        all_news = []
        for drink in drinks: # .class # #id
            news_url = drink.get('href')
            
            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                news_dict = self.cts_reader(news_url)
                all_news.insert(0, news_dict)
        self.append_2_json(all_news) # save as json file

        


    #########################################################################
    ################################## 民視 ##################################
    #########################################################################
    def ftv_all_reader(self):       
        n = 1 # page in list
        while n < 40:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://ftvapi.azurewebsites.net/api/FtvGetNews?Cate=POL&Page='+str(n)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('body')[0].text
            news_dict_data = json.loads(drinks.replace("<p>","").replace("</p>","")) # turn dict in str to dict
            drinks = news_dict_data["ITEM"]
            
            all_news = []
            for drink in drinks: # .class # #id
                news_url = 'https://www.ftvnews.com.tw/news/detail/'+drink["ID"]
                print(news_url)
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.ftv_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
            
        


        
        
    def ftv_reader(self, url):      
        self.browser.get(url)
        text = self.browser.page_source
        res = BeautifulSoup(text, features='lxml')
        
        title = res.find('meta', attrs={'property':'og:title'})['content'].split(u'-民視新聞')[0]
        tag_list = [element.text for element in res.select('.tag a')]

        author = []
        paragraph = res.article.select('p'); paragraph.reverse()
        for p in paragraph:
            if u'報導）' in p.text or u'報導)' in p.text: author = p.text.split(u'（')[1]; break
        if author != []:
            if u'／' not in author:
                if u'、' in author: author = author.split(u' ')[0].split(u'、') # ex. （劉忻怡、陳柏安 台北報導）
                elif u'民視新聞' not in author: author = [author.split(u' ')[0]] # ex. （劉忻怡 台北報導）
                else: author = [author.split(u'民視新聞')[1].split(u'）')[0]]    # ex. （民視新聞綜合報導）
            else: 
                author = author.split(u'／')[1]
                if u'、' in author: author = author.split(u' ')[0].split(u'、')   # ex. （民視新聞／周寧、陳威余、李志銳 台北報導）
                elif u' ' in author: author = [author.split(u' ')[0]]   # ex. （民視新聞／洪明生 屏東報導）
                else: author = [author.split(u'）')[0]]  # ex. （民視新聞／綜合報導）

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select('.date')[0].text.strip('\n').strip()
        date_obj = datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S')     # ex. 2019/09/04 17:28:53
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        context = ""        
        for p in res.select('article p')[:-1]:
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph         

        # related article: {related_title:related_url}
        related_title = [element.text for element in res.select('.exread-list .title')]
        related_url = [element.get('href') for element in res.select('.exread-list a')]
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_title = [element.text for element in res.select('.col-sm-8 .col-xs-6 .title')]
        recommend_url = ['https://www.ftvnews.com.tw'+element.get('href') for element in res.select('.col-sm-8 .col-xs-6 a')]
        recommend_news = [dict([element]) for element in zip(recommend_title, recommend_url)]
        
        # video: {video_title:video_url}
        if res.select('.news-article .fluid-width-video-wrapper') == []: video = []
        else:
            video_title = [element.find('iframe').get('alt') for element in res.select('.news-article .fluid-width-video-wrapper')]
            video_url = [element.find('iframe').get('src') for element in res.select('.news-article .fluid-width-video-wrapper')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        img_title = [None] # cover ing
        img_url = [res.find('meta', attrs={'property':'og:image'})['content']]
        if res.article.select('figure') != []: # article img
            for element in  res.article.select('figure'):
                img_title.extend([element.find('figcaption').text if element.find('figcaption')!=None else None])
            img_url.extend([element.get('src') for element in  res.article.select('figure img')])
        img = [dict([element]) for element in zip(img_title, img_url)]  

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'民視'}
        print(title+' '+time)   
        return news_dict
    
        


    #########################################################################
    ################################## 公視 ##################################
    #########################################################################
    def pts_all_reader(self):
        self.browser.get('https://news.pts.org.tw/subcategory/9') # 政經 總覽

        for x in range(0,15): 
            self.browser.find_element_by_class_name("category_more").click()
            sleep(1)
        text = self.browser.page_source
        
        res = BeautifulSoup(text, features='lxml')
        drinks = res.select('.sec01 .text-title')

        all_news = []
        for drink in drinks: # .class # #id
            news_url = drink.find('a').get('href')
            
            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                news_dict = self.pts_reader(news_url)
                all_news.insert(0, news_dict)
        self.append_2_json(all_news) # save as json file
        
        
        
        
    def pts_reader(self, url):      
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  
        
        title = res.title.text.split(u' | 公視新聞網')[0]
        tag_list = []

        author = None
        author_text = res.select('.subtype-sort')[0].text
        if author_text!=u'綜合報導': author = author_text.split(u' ')[:-1]  # ex. 陳佳鑫 王德心 張國樑   台北報導
        else: author = [author_text]
        
        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select('.sec01 .maintype-wapper h2')[0].text.replace(u"年","/").replace(u"月","/").replace(u"日","")    # ex. 2019年9月27日
        date_obj = datetime.strptime(time_str, '%Y/%m/%d')
        time = date_obj.strftime("%Y/%m/%d")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':None}]

        context = ""
        for p in res.select('.article_content'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph

        related_news = []
        recommend_news = []

        # video: {video_title:video_url}
        if res.select('.article-video') == []: video = []
        else:
            video_title = [element.find('iframe').get('alt') for element in res.select('.article-video')]
            video_url = [element.find('iframe').get('src') for element in res.select('.article-video')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('.img-responsive')==[]: img = []
        else:
            img_title = [element.get('alt') for element in res.select('.img-responsive')]
            img_url = [element.get('src') for element in res.select('.img-responsive')]
            img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'公視'}
        print(title+' '+time)   
        return news_dict
    
        


    #########################################################################
    ########################### 公視 (2020大選)   ############################
    #########################################################################
    def pts_all_reader_2020(self):
        self.browser.get('https://news.pts.org.tw/subcategory/167') # 政經 總覽

        for x in range(0,40): 
            self.browser.find_element_by_class_name("category_more").click()
            sleep(1)
        text = self.browser.page_source
        
        res = BeautifulSoup(text, features='lxml')
        drinks = res.select('.pd-l-r-10 a, .pd-l-r-1 a')

        all_news = []
        for drink in drinks: # .class # #id
            news_url = drink.get('href')
            
            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                news_dict = self.pts_reader(news_url)
                all_news.insert(0, news_dict)
        self.append_2_json(all_news) # save as json file
        

    #########################################################################
    ################################ 三立 ################################
    #########################################################################
    def sten_all_reader(self):
        n = 1 # page in list
        while n < 80:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.setn.com/ViewAll.aspx?PageGroupID=6&p='+str(n)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('.col-sm-12 .view-li-title')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = 'https://www.setn.com'+drink.find('a').get('href')   
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    try:
                        news_dict = self.sten_reader(news_url)
                        all_news.insert(0, news_dict)
                    except Exception as e:
                        print(e); continue                    
            n+=1
            self.append_2_json(all_news) # save as json file
            
            

        
    def sten_reader(self, url): 
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')
        
        title = res.title.text.strip('\n').strip().split(u' | ')[0]
        tag_list = [element.text for element in res.select('.keyword a')]
        author = [res.find('meta', attrs={'name':'author'})['content']]

        context = ""
        for p in res.select('article p')[1:]:
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph        
        
        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'property':'article:published_time'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:00') # ex. "2019-10-02T12:31:00"
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        related_title = [element.text for element in res.select('.row .col-sm-6')[0].select('a')] # 相關新聞 標題
        related_url = ['https://www.setn.com'+element.get('href') for element in res.select('.row .col-sm-6')[0].select('a')] # 相關新聞 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        recommend_title = [element.text for element in res.select('.extend ul li a')] # 延伸閱讀 標題
        recommend_url = ['https://www.setn.com'+element.get('href') for element in res.select('.extend ul li a')] # 延伸閱讀 url
        recommend_news = [dict([element]) for element in zip(recommend_title, recommend_url)]

        # video: {video_title:video_url}
        if res.select('#vodIframe') == []: video = []
        else:
            video_title = [element.get('alt') for element in res.select('#vodIframe')]
            video_url = ['https://www.setn.com/'+element.get('src') for element in res.select('#vodIframe')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('#Content1 img')==[]: img = []
        else:
            img_title = [element.text.split(u'▲')[1] for element in res.find_all('p', attrs={'style':'text-align: center;'}) if u'▲'in element.text]
            img_url = [element.get('src') for element in res.select('#Content1 img')]
            img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'三立新聞'}
        print(title+' '+time)   
        return news_dict


        

    #########################################################################
    ################################ 中天新聞 ################################
    #########################################################################
    def ctitv_all_reader(self): 
        n = 1 # page in list
        while n > 0:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'http://gotv.ctitv.com.tw/category/politics-news/page/'+str(n)        
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('.column article')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.find('a').get('href')  
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    try:
                        news_dict = self.ctitv_reader(news_url)
                        all_news.insert(0, news_dict)
                    except Exception as e:
                        print(e); continue                    
            n+=1
            self.append_2_json(all_news) # save as json file
        
            
            

        
    def ctitv_reader(self, url):    
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')      
        
        title = res.title.text.strip('\n').strip()
        author = [res.article.select('.reviewer')[0].text]
        tag_list = [element.text for element in res.select('article .tagcloud a')]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        date_obj = datetime.strptime(res.article.select('.posted-on time')[0].get('datetime'), '%Y-%m-%dT%H:%M:%S+08:00')
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]
        
        # article content
        content = ""
        for p in res.select('article p')[1:]:
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                content += paragraph

        # article resources: {source_name, source_url}
        try: 
            source_name = res.select('.article-source a')[0].text
            source_url = res.select('.article-source a')[0].get('href')
            source = [{'source_name':source_name, 'source_url':source_url}]
        except Exception as e: # no from other source
            source = [{'source_name':None, 'source_url':None}]      
        
        # related article: {related_title , related_url}
        related_title = [element.text for element in res.article.select('.section-head')[0].select('a')]# 相關新聞 標題
        related_url = [element.get('href') for element in res.article.select('.section-head')[0].select('a')] # 相關新聞 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]
        
        # recommend article: (recommend_title, recommend_url)
        recommend_news = []

        news_dict = {'title':title, 'author':author, 'context':content, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source':source, 'media':'中天新聞'}
        print(title+' '+time)
        return news_dict
        


        
    #########################################################################
    ################################ 年代新聞 ################################
    #########################################################################
    def era_all_reader(self):
        n = 1 # page in list
        while n < 21:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'http://www.eracom.com.tw/EraNews/Home/political/?pp='+str((n-1)*10)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('.tib-title a')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.era_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
            
            
            

        
    def era_reader(self, url):
        self.browser.get(url)
        text = self.browser.page_source
        res = BeautifulSoup(text, features='lxml')  
        
        title = res.select('.articletitle')[0].text
        author = [res.select('.author')[0].text] if res.select('.author')!=[] else []
        tag_list = res.find('meta', attrs={'name':'keywords'})['content'].split(u',')

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select('.time')[0].text
        date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        content = ""
        for p in res.select('.article-main')[0].select('p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                content += paragraph
        
        # related article: {related_title , related_url}
        related_title = [element.get('title') for element in res.select('.m2o-type-news-')] # 相關新聞 標題
        related_url = [element.get('href') for element in res.select('.m2o-type-news-')] # 相關新聞 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]
        
        # recommend article: (recommend_title, recommend_url)
        recommend_news = []

        news_dict = {'title':title, 'author':author, 'context':content, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'media':'年代新聞'}
        print(title+' '+time)
        return news_dict
        


        

    #########################################################################
    ################################ 非凡新聞 ################################
    #########################################################################
    def ustv_all_reader(self):
        n = 1 # page in list
        while n < 10:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.ustv.com.tw/UstvMedia/news/107?page='+str(n)        
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('.subject ')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.find('a').get('href').replace("\n", "")
        
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    try:
                        news_dict = self.ustv_reader(news_url)
                        all_news.insert(0, news_dict)
                    except Exception as e:
                        print(e); continue                   
            n+=1
            self.append_2_json(all_news) # save as json file
        
            
            

        
    def ustv_reader(self, url): 
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')      
        
        # news detail dict
        news_text = res.select('#news_detail .module script')[0].text
        news_dict_data = json.loads(news_text.replace("'", "\"")) # turn dict in str to dict
        
        title = news_dict_data['headline'].replace(u'&quot;',"")        
        author = [news_dict_data['author']['name']]
        tag_list = []

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time = news_dict_data['dateModified']
        date_obj = datetime.strptime(time, '%Y/%m/%d %H:%M')
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        content = ""
        for p in res.select('#primarytext'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                content += paragraph

        # article resources: {source_name, source_url}
        source = [{'source_name':None, 'source_url':None}]      
        
        # video url
        try: video_url = res.select('.video-play')[0].find('iframe').get('src')
        except Exception as e: video_url = None # no from other source      

        # related article: {related_title , related_url}
        related_news = []
        
        # recommend article: (recommend_title, recommend_url)
        recommend_news = []

        news_dict = {'title':title, 'author':author, 'context':content, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source':source, 'video_url':video_url, 'media':'非凡新聞'}
        print(title+' '+time)
        return news_dict
        

        

    #########################################################################
    ################################ 中央通訊社 ################################
    #########################################################################
    def cna_all_reader(self):
        for n in range(1,6): # click num of button "more"
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.cna.com.tw/cna2018api/api/simplelist/categorycode/aipl/pageidx/'+str(n)
            res = requests.get(url) 
            page_dict_text = json.loads(res.content.replace("'", "\"")) # read as API xml response
            all_news = []
            for news in page_dict_text['result']['SimpleItems']: # .class # #id
                news_url = news['PageUrl']              

                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    try:
                        news_dict = self.cna_reader(news_url)
                        all_news.insert(0, news_dict)
                    except Exception as e:
                        print(e); continue                    
            n+=1
            self.append_2_json(all_news) # save as json file
        
        
        
    def cna_reader(self, url):      
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  
            
        title = res.article.get('data-title')   
        tag_list = []

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time = res.find('meta', attrs={'itemprop':'datePublished'})['content']
        date_obj = datetime.strptime(time, '%Y/%m/%d %H:%M')
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]
        
        # article content
        content = ""
        for p in res.select('.paragraph p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                content += paragraph
        
        if content.find(u'（編輯：') != -1: 
            author = [content.split(u'（編輯：')[1].split(u'）')[0]] # article last example: ...（編輯：XXX）1080804
            content = content.split(u'（編輯：')[0]
        else:
            try: author = [content.split(u'記者')[1].split(u'台北')[0]] # article first example: （中央社記者XXX台北4日電）...
            except Exception as e: author = [res.find('meta', attrs={'itemprop':'author'})['content']] # article first example: （中央社台北2日電）...
            finally: content = content.split(u'日電）')[1].split(str(int(date_obj.strftime("%Y"))-1911)+date_obj.strftime("%m%d"))[0]
        
        # video url
        video = [] # no from other source 

        # img: {img_url, img_alt}
        img_url = []
        try:
            for element in res.select('.floatImg .wrap img'):
                img_url.extend(element.get('src') if element.get('src')!=None else element.get('data-src'))
            img_title = [element.get('alt') for element in res.select('.floatImg .wrap img')]
            img = [dict([element]) for element in zip(img_title, img_url)]          
        except Exception as e: # no img in news
            img = []

        # related article: {related_title , related_url}
        related_title = [element.text for element in res.select('.moreArticle-link span')] # 延伸閱讀 標題
        related_url = [element.get('href') for element in res.select('.moreArticle-link')] # 延伸閱讀 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]
        
        # recommend article: (recommend_title, recommend_url)
        recommend_news = []

        news_dict = {'title':title, 'author':author, 'context':content, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'中央通訊社'}
        print(title+' '+time)
        return news_dict
        

        


    #########################################################################
    ################################ 關鍵評論網 ################################
    #########################################################################
    def thenewslens_all_reader(self):       
        n = 1
        while n > 0:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.thenewslens.com/category/politics?page='+str(n)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('.share-box')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.find('a').get('data-url')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.thenewslens_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
        
            

        
    def thenewslens_reader(self, url):      
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  
        
        title = res.select('#title-bar')[0].text
        tag_list = [element.text for element in res.select('.tags a')]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'property':'article:published_time'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S+08:00') # ex. 2019-08-05T16:00:35+08:00
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]
        
        # article content
        content = ""
        for p in res.select('.article-content p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                content += paragraph
        content = content.split(u'責任編輯')[0] 
        
        author = [res.find('meta', attrs={'name':'author'})['content']]
        
        # article resources: {source_name, source_url}
        try: 
            source_name = [element.text for element in res.select('.article-content p a')]
            source_url = [element.get('href') for element in res.select('.article-content p a')]
            source = [dict([element]) for element in zip(source_name, source_url)]
        except Exception as e: # no from other source
            source = [{'source_name':None, 'source_url':None}]  
        
        # video url
        video_url = None # no from other source 

        # img: {img_url, img_alt}
        img_url = []
        try:                
            img_title = [element.get('alt') for element in res.find('figure')]
            img_url = [element.get('src') for element in res.find('figure')]
            img = [dict([element]) for element in zip(img_title, img_url)]          
        except Exception as e: # no img in news
            img = []

        # related article: {related_title , related_url}
        try: 
            related_source_title = [element.text for element in res.select('.article-content ul li a')] # 延伸閱讀+新聞來源 標題
            related_source_url = [element.get('href') for element in res.select('.article-content ul li a')] # 延伸閱讀+新聞來源 url
            related_title = list(set(related_source_title)-set(source_title)) # 延伸閱讀 標題
            related_url = list(set(related_source_url)-set(source_url)) # 延伸閱讀 url
            related_news = [dict([element]) for element in zip(related_title, related_url)]
        except Exception as e: # no from other source
            related_news = []   
        
        # recommend article: (recommend_title, recommend_url)
        recommend_news = []

        news_dict = {'title':title, 'author':author, 'context':content, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source':source, 'video_url':video_url, 'img':img, 'media':'關鍵評論網'}
        print(title+' '+time)
        return news_dict
        

        


    #########################################################################
    ################################ 民報 ################################
    #########################################################################
    def peoplenews_all_reader(self):    
        n = 1
        while n > 0:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.peoplenews.tw/list/%E6%94%BF%E6%B2%BB#page-'+str(n)
            self.browser.get(url)    
            soup = BeautifulSoup(self.browser.page_source,features="lxml")
            drinks = soup.select('#area_list a')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = 'https://www.peoplenews.tw'+drink.get('href')
                print(news_url)
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.peoplenews_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file



        
    def peoplenews_reader(self, url):   
        self.browser.get(url)
        res = BeautifulSoup(self.browser.page_source, features='lxml')

        title = res.select('.news_title')[0].text
        tag_list = []

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select("#news_author .date")[0].text
        date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M') # ex. 2019-08-05 16:02
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]
            
        # article content
        content = ""
        for p in res.select('#newscontent p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                content += paragraph 
        
        author = [res.select('.author')[0].text ]     
        
        # video: {video_title:video_url}
        if res.find('iframe')==None: source = [] # no from video source 
        else:
            video_url = [element.get('src') for element in res.select('iframe')]
            video_title = [element.text for element in res.select('iframe')]
            video = [dict([element]) for element in zip(video_title, video_url)]

        # img: {img_title:img_url}
        if res.find('#newsphoto')==None: img = [] # no from img source  
        else:           
            img_title = [element.find('img').get('alt') for element in res.select('#newsphoto')]
            img_url = [element.find('img').get('src') for element in res.select('#newsphoto')]
            img = [dict([element]) for element in zip(img_title, img_url)]          
            

        # related article: {related_title:related_url}
        related_title = [element.select('.title')[0].text for element in res.select('#area_related a')] # 相關新聞 標題
        related_url = ['https://www.peoplenews.tw'+element.get('href') for element in res.select('#area_related a')] # 相關新聞 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]
        
        # recommend article: (recommend_title:recommend_url)
        recommend_ad_url = res.select('#dablewidget_6XgLG0oN iframe')[0].get('src') # recommend news uses other api to make 
        recommend_res = BeautifulSoup(self.get_url_text(recommend_ad_url), features='lxml')
        recommend_title = [element.select('.name')[0].text for element in recommend_res.select('td') if element['data-item_id']!='undefined']
        recommend_url = ['https://www.peoplenews.tw/news/'+element.get('data-item_id') for element in recommend_res.select('td') if element['data-item_id']!='undefined']
        recommend_news = [dict([element]) for element in zip(recommend_title, recommend_url)]

        news_dict = {'title':title, 'author':author, 'context':content, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'民報'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ################################ 上報 ################################
    #########################################################################
    def upmedia_all_reader(self, in_col_type):
        col_type = 1 if in_col_type=='調查' else 24 # in_col_type={調查(1), 焦點(24)}
        n = 1
        while n < 14 :
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.upmedia.mg/news_list.php?currentPage='+str(n)+'&Type='+str(col_type)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('dl dt')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = 'https://www.upmedia.mg/'+drink.find('a').get('href')

                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.upmedia_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
            
        


    def upmedia_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')          
        
        title = res.select('#ArticleTitle')[0].text
        tag_list = [element.text for element in res.select('.label a')]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'itemprop':'datePublished'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S') # ex. 2019-08-05T16:00:35
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        content = ""        
        for p in res.find_all('p', attrs={'style':'text-align: justify;'}):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                content += paragraph 
        
        author = [res.select('.author a')[0].text]
        
        # video: {video_title:video_url}
        if res.find('iframe')==None: video = [] # no from video source  
        else:
            video_url = [element.get('src') for element in res.select('iframe')]
            video_title = [element.text for element in res.select('iframe')]
            video = [dict([element]) for element in zip(video_title, video_url)]

        # img: {img_title:img_url}
        if res.find('p+ div img') == None: img = [] # no from img source    
        else:           
            img_title = res.find('meta', attrs={'property':'og:image'})['content'] # cover img title
            img_title.extend([element.get('alt') for element in res.select('p+ div img')]) # cover img url

            img_url = res.find('meta', attrs={'property':'og:image:alt'})['content']
            img_url.extend([element.get('src') for element in res.select('p+ div img')])

            img = [dict([element]) for element in zip(img_title, img_url)]          
            
        # related article: {related_title:related_url}
        related_title = [element.text for element in res.select('.rss_close a')] # 延伸閱讀 標題
        related_url = [element.get('href') for element in res.select('.rss_close a')] # 延伸閱讀 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]
        
        # recommend article: (recommend_title:recommend_url)
        recommend_title = [element.text for element in res.select('.related a')] # 編輯部推薦 標題
        recommend_url = ['https://www.upmedia.mg/'+element.get('href') for element in res.select('.related a')] # 編輯部推薦 url
        recommend_news = [dict([element]) for element in zip(recommend_title, recommend_url)]

        news_dict = {'title':title, 'author':author, 'context':content, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'上報'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ################################# 信傳媒 #################################
    #########################################################################
    def cmmedia_all_reader(self):       
        n = 1
        while n > 0:                   
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.cmmedia.com.tw/api/articles?num=12&page='+str(n)+'&category=politics' 
            res = requests.get(url)
            page_dict_text = json.loads(res.content.replace("'", "\"")) # read as API xml response
            
            all_news = []
            for news in page_dict_text:
                news_url = 'https://www.cmmedia.com.tw/home/articles/'+str(news['id'])              
                print(news_url)
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    try:
                        news_dict = self.cmmedia_reader(news_url)
                        all_news.insert(0, news_dict)
                    except Exception as e:
                        print(e); continue                    
            n+=1
            self.append_2_json(all_news) # save as json file
        
        
        
        
        
    def cmmedia_reader(self, url):      
        self.browser.get(url)
        res = BeautifulSoup(self.browser.page_source, features='lxml')   

        title = res.find('meta', attrs={'property':'og:title'})['content']
        tag_list = res.find('meta', attrs={'name':'keywords'})['content'].split(',')
        author = [res.select('.author_name')[0].text]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'itemprop':'datePublished'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M') # ex. 2019-08-05T16:00:35
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        content = ""        
        for p in res.select('.article_content'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                content += paragraph        

        # video: {video_title:video_url}
        if res.find('div', attrs={'class':'plyr__video-wrapper'})==None: video = [] # no video
        else: 
            #video_url = res.select('#player')[0].get('data-plyr-embed-id')
            video_title = [element.find('iframe').get('title').split(u'for')[1] for element in res.select('.plyr__video-wrapper')]
            video_url = [element.find('iframe').get('src') for element in res.select('.plyr__video-wrapper')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        img_title, img_url = [], []     
        if res.find('div', attrs={'class':'article_mainimg'}) != None: # main img
            img_title.extend([res.select('.article_mainimg ')[0].text])
            img_url.extend([res.select('.article_mainimg .article_pic')[0].get('style').split('\'')[1]])
        if res.find('div', attrs={'class':'divarticlimg'}) != None: # article main img
            img_title.extend([res.select('.divarticlimg')[0].text])
            img_url.extend([res.select('.divarticlimg img')[0].get('src')]) 
        img = [dict([element]) for element in zip(img_title, img_url)]  

        # related article: {related_title:related_url}
        related_list = res.select('.article__article-further___2Aw_c')[0].find_all('a', attrs={'href':re.compile("/home")})
        related_title = [element.text for element in related_list] # 延伸閱讀 標題
        related_url = ['https://www.cmmedia.com.tw'+element.get('href') for element in related_list] # 延伸閱讀 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []

        news_dict = {'title':title, 'author':author, 'context':content, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'信傳媒'}
        print(title+' '+time)   
        return news_dict
        

        


    #########################################################################
    ################################# 大紀元 #################################
    #########################################################################
    def epochtimes_all_reader(self):
        n = 1
        while n > 0:                   
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.epochtimes.com/b5/ncid1077884_'+str(n)+'.htm'
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, features="lxml")
            drinks = soup.select('.title a')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    try:
                        news_dict = self.epochtimes_reader(news_url)
                        all_news.insert(0, news_dict)
                    except Exception as e:
                        print(e); continue                    
            n+=1
            self.append_2_json(all_news) # save as json file
        
            
        


    def epochtimes_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')          

        title = res.find('meta', attrs={'property':'og:title'})['content'].split(u' - 大紀元')[0]
        tag_list = [element.text for element in res.find_all('a', attrs={'rel':'tag'})]
        author = [res.select('#artbody')[0].text.split(u'責任編輯：')[1].split('\n')[0]] if len(res.select('#artbody')[0].text.split(u'責任編輯：'))>2 else []

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'property':'article:published_time'})['content'] 
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S+08:00') # ex. 2019-08-13T14:42:46+08:00
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        content = ""        
        for p in res.select('#artbody p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                content += paragraph                

        # video: {video_title:video_url}
        if res.find('iframe', attrs={'src':re.compile('video')})==None: video = [] # no from video source   
        else:
            video_url = [res.find('iframe', attrs={'src':re.compile('video')}).get('src')]
            video_title = [res.find('iframe', attrs={'src':re.compile('video')}).text]
            video = [dict([element]) for element in zip(video_title, video_url)]

        # img: {img_title:img_url}
        img_title, img_url = [], []     
        if res.select('.arttop a') != []: # main img
            if res.select('.arttop .caption')!=[]: img_title.extend([res.select('.arttop .caption')[0].text])
            else: img_title.extend([u''])
            img_url.extend([res.select('.arttop a')[0].get('href')])    
        if res.find('figure') != None: # article main img
            img_title.extend([element.text for element in res.select('figure figcaption')])
            img_url.extend([element.get('href') for element in res.select('figure a')])
        img = [dict([element]) for element in zip(img_title, img_url)]      

        # related article: {related_title:related_url}
        related_title = [element.find('a').text for element in res.select('.related-posts .post-title')] # 相關文章 標題
        related_url = [element.find('a').get('href') for element in res.select('.related-posts .post-title')] # 相關文章 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []

        news_dict = {'title':title, 'author':author, 'context':content, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'大紀元'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ################################ 匯流新聞網 ###############################
    #########################################################################
    def cnews_all_reader(self):     
        n = 1
        while n < 8:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://cnews.com.tw/category/%E6%94%BF%E6%B2%BB%E5%8C%AF%E6%B5%81/page/'+str(n)+'/'
            res = requests.get(url)
            if res.status_code == 404: print("Reach the end page."); break  # check url exist
            soup = BeautifulSoup(res.text, "lxml")
            
            drinks = soup.select('.left-wrapper .slider-photo') # top rolling article
            drinks.extend(soup.select('.special-format')[1:]) # left articles except the first element, this page's url

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.find('a').get('href')

                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.cnews_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
        
        
            
        


    def cnews_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')          

        title = res.find('meta', attrs={'property':'og:title'})['content']
        tag_list = [element.text for element in res.select('.keywords a')]
    
        author = [res.select('#articleTitle .user a')[0].text]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select('#articleTitle .date span')[1].text
        date_obj = datetime.strptime(time_str, '%Y-%m-%d') # ex. 2019-08-13
        time = date_obj.strftime("%Y/%m/%d")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':None}]  

        # article content
        context = ""        
        for p in res.select('article p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph 
        context = context.split(u'更多匯流新聞網報導')[0]        
        
        # video: {video_title:video_url}
        video = []
        
        # img: {img_title:img_url}  
        if res.select('article img') == []: img = []
        else:
            img_title = [element.get('alt') for element in res.select('article img')]
            img_title_tmp = []          
            if res.select('article strong') !=[]: # img title in article, ex. ▲......
                img_title_tmp = [element.text.split(u'▲')[1] for element in res.select('article strong') if u'▲' in element.text]
                for n in range(len(img_title)-len(img_title_tmp),len(img_title_tmp)+1): img_title[n] = img_title_tmp[n-1]
            img_url = [element.get('src') for element in res.select('article img')]
            
            img = [dict([element]) for element in zip(img_title, img_url)]  
        
        # related article: {related_title:related_url}
        related_title = [element.text for element in res.select('.extend-wrapper h3')] # 延伸閱讀 標題
        related_url = [element.find_all('a')[1].get('href') for element in res.select('.extend-wrapper figure')] # 延伸閱讀 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []
        
        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'匯流新聞網'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ################################# 新頭殼 #################################
    #########################################################################
    def newtalk_all_reader(self):   
        n = 1
        while n < 7:
            url = 'https://newtalk.tw/news/subcategory/2/%E6%94%BF%E6%B2%BB/'+str(n)        
            print('================================ page: ' + str(n) + ' ================================')
            
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            
            drinks = soup.select('.news-title') # top rolling article
            drinks.extend(soup.select('.news_title')) # left articles except the first element, this page's url

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.find('a').get('href')
                try:   
                    if news_url == self.last_news_url: # reach has read news
                        self.append_2_json(all_news)
                        raise SyntaxError("Read all news news")
                    else:
                        news_dict = self.newtalk_reader(news_url)
                        all_news.insert(0, news_dict)
                except Exception as e:
                    print(news_url)
                    continue                
            n+=1
            self.append_2_json(all_news) # save as json file

        
            
        


    def newtalk_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')          

        title = res.select('.content_title')[0].text
        tag_list = [element.text for element in res.select('.tag_for_item a')]
        author = [res.find('meta', attrs={'property':'dable:author'})['content']]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'property':'article:published_time'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S+08:00') # ex. 2019-08-13
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]    

        # article content
        context = ""        
        for p in res.select('#news_content p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph 
        context = context.split(u'延伸閱讀')[0]
        
        # video: {video_title:video_url}
        if res.select('.video-container') == []: video = []
        else:
            video_title = [element.find('iframe').get('src') for element in res.select('.video-container')]
            video_url = [element.find('iframe').get('alt') for element in res.select('.video-container')]
            
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}  
        if res.select('#news_content img') == []: img = []
        else:
            img_title = [element.get('alt') for element in res.select('#news_content img')]
            img_url = [element.get('src') for element in res.select('#news_content img')]
            
            img = [dict([element]) for element in zip(img_title, img_url)]  
        
        # related article: {related_title:related_url}
        related_title = [element.text for element in res.select('#news_content a')] # 延伸閱讀 標題
        related_url = [element.get('href') for element in res.select('#news_content a')] # 延伸閱讀 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []
        
        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'新頭殼'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ################################# 風傳媒 #################################
    #########################################################################
    def storm_all_reader(self):
        n = 1
        while n < 55:
            url = 'https://www.storm.mg/category/118/'+str(n)
            print('================================ page: ' + str(n) + ' ================================')            
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('.carousel-inner .carousel-caption') # left top rolling article
            drinks.extend(soup.select('#category_content .col-xs-12')) # left middle articles
            drinks.extend(soup.select('.card_thumbs_left .card_img_wrapper')) # left bottom articles

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.find('a').get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    try:
                        news_dict = self.storm_reader(news_url)
                        all_news.insert(0, news_dict)
                    except Exception as e:
                        print(e); continue                    
            n+=1
            self.append_2_json(all_news) # save as json file
            

        
            
        


    def storm_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')          
        
        title = res.select('#article_title')[0].text
        tag_list = res.find('meta', attrs={'name':'news_keywords'})['content'].split(u', ')
        author = [element.text for element in res.select('#author_block .info_author')]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'itemprop':'datePublished'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S') # ex. 2019-08-22T11:50:01
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]    
        
        # article content
        context = ""        
        for p in res.select('#CMS_wrapper p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph 
        if u'➤更多內容' in context: context = context.split(u'➤更多內容')[0]
        
        
        # video: {video_title:video_url}
        if res.select('#CMS_wrapper iframe') == []: video = []
        else:
            video_title = [element.get('alt') for element in res.select('#CMS_wrapper iframe')]
            video_url = [element.get('src') for element in res.select('#CMS_wrapper iframe')]           
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}  
        img_title = [res.find('meta', attrs={'name':'twitter:image:alt'})['content']]   #main img
        img_url = [res.find('meta', attrs={'name':'twitter:image'})['content']] # main img
        if res.select('.dnd-drop-wrapper img') != []:   # img in article
            img_title.extend([element.get('alt') for element in res.select('.dnd-drop-wrapper img')])
            img_url.extend([element.get('src') for element in res.select('.dnd-drop-wrapper img')]) 
        img = [dict([element]) for element in zip(img_title, img_url)]
        
        # related article: {related_title:related_url}
        related_title = [element.text for element in res.select('.related_link')] # 相關報導 標題
        related_url = ['https://www.storm.mg'+element.get('href') for element in res.select('.related_link')] # 相關報導 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []
        
        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'風傳媒'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ################################# 今日新聞 ################################
    #########################################################################
    def nownews_all_reader(self):       
        n = 1
        while n < 87:            
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.nownews.com/cat/politics/page/'+str(n)
            drinks = []
            while drinks == []:
                text = self.get_url_text(url)
                soup = BeautifulSoup(text, "lxml")
                if n==1: drinks = soup.select('.td-meta-info-container h3, .td_block_padding h3, .td-fix-index h3')
                else: drinks = soup.select('.td-fix-index h3') # except articles on top and middle space (熱門新聞) 

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.find('a').get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    try:
                        news_dict = self.nownews_reader(news_url)
                        all_news.insert(0, news_dict)
                    except Exception as e:
                        print(e); continue                    
            n+=1
            self.append_2_json(all_news) # save as json file
        
            
            

        
            
        


    def nownews_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  

        title = res.find('h1', attrs={'class':'entry-title'}).text
        tag_list = [element.text for element in res.select('.td-tags a')]
        author = [res.find('div', attrs={'class':'td-post-author-name'}).text.strip('\n').strip()]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'itemprop':'datePublished'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S+00:00') # ex. 2019-08-22 11:50:01
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        context = ""        
        for p in res.select('span p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph 

        # related article: {related_title:related_url}
        related_title = [element.text for element in res.select('.relativeArticle_Reynold a')] # 相關報導 標題
        related_url = [element.get('href') for element in res.select('.relativeArticle_Reynold a')] # 相關報導 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        if res.select('.td-content-more-articles-box') == []: recommend_news = []
        else:
            recommend_title = [element.text for element in res.select('.td-content-more-articles-box h3')]
            recommend_url = [element.find('a').get('href') for element in res.select('.td-content-more-articles-box h3')]
            recommend_news = [dict([element]) for element in zip(recommend_title, recommend_url)]

        # video: {video_title:video_url}
        if res.select('iframe') == []: video = []
        else:
            video_title = [res.select('iframe')[0].get('alt')]
            video_url = [res.select('iframe')[0].get('data-src')]           
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('figcaption')==[]: img = [] # no img
        else:
            img_title = [element.text for element in res.select('figcaption')]
            img_url = [element.get('data-src') for element in res.select('figure')]
            img = [dict([element]) for element in zip(img_title, img_url)]          

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'今日新聞'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ############################ 今日新聞 (2020大選) ##########################
    #########################################################################
    def nownews_all_reader_2020(self):       
        n = 1
        while n < 148:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.nownews.com/cat/2020-2/page/'+str(n)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            if n==1: drinks = soup.select('.td-meta-info-container h3, .td-block-span4 h3')
            else: drinks = soup.select('.td-block-span4 h3') # except articles on top and middle space (熱門新聞) 

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.find('a').get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.nownews_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
        

        


    #########################################################################
    ################################# 鏡週刊 #################################
    #########################################################################
    def mirrormedia_all_reader(self):       
        self.browser.get('https://www.mirrormedia.mg/category/political')
        jsCode = "var q=document.documentElement.scrollTop=100000" # control distance of scroller on the right
        for x in range(0,20): 
            self.browser.execute_script(jsCode) # keep scrolling to the bottom
            sleep(1)
        text = self.browser.page_source  

        all_news = []
        res = BeautifulSoup(text, features='lxml')
        drinks = res.select('.listArticleBlock__figure')
        
        for drink in drinks: # .class # #id
            news_url = 'https://www.mirrormedia.mg' + drink.find('a').get('href')           
            if len(news_url.split('https://www.mirrormedia.mg/story/'))==1: continue # skip ad url
            
            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                news_dict = self.mirrormedia_reader(news_url)
                all_news.insert(0, news_dict)
        self.append_2_json(all_news) # save as json file
        

        
            
        


    def mirrormedia_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  

        title = res.title.text
        tag_list = [element.text for element in res.select('.tags a')]
        author = [res.find('meta', attrs={'property':'dable:author'})['content']]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'property':'article:published_time'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.000Z') # ex. 2019-08-19T09:05:25.000Z
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]
        
        # article content
        context = ""        
        for p in res.select('#article-body-content p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph 
        context = context.split(u'更新時間')[0]

        # related article: {related_title:related_url}
        related_title = [element.text for element in res.select('#article-body-content a')] # 相關報導 標題
        related_url = ['https://www.mirrormedia.mg'+element.get('href') for element in res.select('#article-body-content a')] # 相關報導 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []
        
        # video: {video_title:video_url}
        if res.select('article iframe') == []: video = []
        else:
            video_title = [res.select('article iframe')[0].get('alt')]
            video_url = [res.select('article iframe')[0].get('src')]            
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        img_title = [res.select('#hero-image')[0].get('alt')] # cover img
        img_url = [res.select('#hero-image')[0].get('src')]
        if res.select('.thumbnail img')!=[]: # context img
            img_title.extend([element.get('alt') for element in res.select('.thumbnail img')])
            img_url.extend([element.get('src') for element in res.select('.thumbnail img')])
        img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'鏡週刊'}
        print(title+' '+time)       
        return news_dict     
        

        



    #########################################################################
    ############################## 鏡週刊 (2020大選) ##########################
    #########################################################################
    def mirrormedia_all_reader_2020(self, party):       
        n = 1
        while n < 11:
            try:
                if party == 'DPP':  url = 'https://www.mirrormedia.mg/api/getlist?where=%7B%22tags%22%3A%7B%22%24in%22%3A%5B%225d65fbaa486faa3919afaeb9%22%5D%7D%7D&max_results=25&page='+str(n)+'&sort=-publishedDate' # 民進黨 
                elif party == 'KMT': url = 'https://www.mirrormedia.mg/api/getlist?where=%7B%22tags%22%3A%7B%22%24in%22%3A%5B%225d65fbaf486faa3919afaeba%22%5D%7D%7D&max_results=25&page='+str(n)+'&sort=-publishedDate' # 國民黨
                elif party == 'TPP':  url = 'https://www.mirrormedia.mg/api/getlist?where=%7B%22tags%22%3A%7B%22%24in%22%3A%5B%225d65fbb6486faa3919afaebb%22%5D%7D%7D&max_results=25&page='+str(n)+'&sort=-publishedDate' # 民眾黨
                else: raise('Unknown Party Name for Mirror Media News.')
                #resp = urllib2.urlopen(url).getcode() # check url exist
            except:
                print("Reach the end page.")
                break
        
            print('================================ page: ' + str(n) + ' ================================')
            
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = json.loads(soup.text)['_items']

            all_news = []
            for drink in drinks: # .class # #id
                news_url = 'https://www.mirrormedia.mg/story/'+drink['slug']
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.mirrormedia_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file 
            

        


    #########################################################################
    ################################# 新新聞 #################################
    #########################################################################
    def new7_all_reader(self):      
        n = 1
        while n > 0:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.new7.com.tw/NewsList.aspx?t=03&p='+str(n)
            while n:    # check get data, 新新聞 easy to break at page1
                self.browser.get(url)
                if n==1: sleep(10)  # 新新聞 needs to wait to get cookie
                text = self.browser.page_source
                soup = BeautifulSoup(text, features='lxml')
                drinks = soup.select('#ContentPlaceHolder1_DataList1 a')
                if drinks==[]:  # fail to get page1 data
                    self.change_browser()   # reopen chrome driver with new information
                else: self.browser.get('https://www.whatismybrowser.com/'); sleep(10); break           
 
            all_news = []
            for drink in drinks: # .class # #id
                news_url = 'https://www.new7.com.tw'+drink.get('href')
                #print(news_url)

                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.new7_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
            
            

        

        
    def new7_reader(self, url):
        self.browser.get(url)
        res = BeautifulSoup(self.browser.page_source, features='lxml')

        title = res.find('meta', attrs={'property':'og:title'})['content'].split(u'新新聞-')[1]
        tag_list = []
        author = [res.select('.NewsPageEditer')[0].text.strip('\n').strip()]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select('.NewsPageTitle span')[0].text
        date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]        

        # article content
        context = ""        
        for p in res.select('p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph

        
        # related article: {related_title:related_url}
        related_news = []

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []
        
        # video: {video_title:video_url}
        video = []

        # img: {img_title:img_url}
        if res.select('#ContentPlaceHolder1_NewsView_imgpic') == []: img = []
        else:
            img_title = [res.select('#ContentPlaceHolder1_NewsView_imgpic')[0].get('alt')] # cover img
            img_url = [res.select('#ContentPlaceHolder1_NewsView_imgpic')[0].get('src')]
            img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'新新聞'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ############################### 台灣好新聞 ################################
    #########################################################################
    def taiwanhot_all_reader(self):         
        n = 1
        while n > 0:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.taiwanhot.net/?cat=25&page='+str(n)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            if n==1: drinks = soup.select('.col-md-12 a, .news-title a')
            else: drinks = soup.select('.news-title a') # except articles on top and middle space (熱門新聞)    

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.taiwanhot_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
            
            
            

        
            
        


    def taiwanhot_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  

        title = res.find('meta', attrs={'property':'og:title'})['content'].split(u' | 台灣好新聞')[0]
        tag_list = [element.text for element in res.select('.td-tags a')]
        author = [res.select('.reporter_name')[0].text]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select('.txt_gray2 .post_time')[0].text
        date_obj = datetime.strptime(time_str, ' %Y-%m-%d %H:%M')       
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        context = ""        
        for p in res.select('.news_content p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph 
        
        # related article: {related_title:related_url}
        related_title = [element.text.strip('\t').strip() for element in res.select('.col-xs-12 .news_title')] # 相關報導 標題
        related_url = [element.get('href') for element in res.select('.relative_wrapper a')] # 相關報導 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []

        # video: {video_title:video_url}
        if res.select('iframe') == []: video = []
        else:
            video_title = [res.select('iframe')[0].get('alt')]
            video_url = [res.select('iframe')[0].get('src')]            
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('.photo_wrap')==[]: img = [] # no img
        else:
            img_title = [element.text.strip('\n').strip() for element in res.select('.photo_wrap')]
            img_url = [element.find('img').get('src') for element in res.select('.photo_wrap')]
            img = [dict([element]) for element in zip(img_title, img_url)]          

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'台灣好新聞'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ############################### 中央廣播電台 ################################
    #########################################################################
    def rti_all_reader(self):
        n = 1
        while n < 55:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.rti.org.tw/news/list/categoryId/5/page/'+str(n)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('.newslist-box li')

            all_news = []
            for drink in drinks: # .class # #id
                news_url ='https://www.rti.org.tw' +drink.find('a').get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.rti_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
            
            
            

        
            
        


    def rti_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  

        title = res.find('meta', attrs={'property':'og:title'})['content']
        tag_list = [element.text for element in res.select('.keyword-box a')]
        author = [res.select('.source')[1].text.split(u'：')[1]]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select('.date')[0].text.split(u'時間：')[1]
        date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M')        
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        context = ""        
        for p in res.select('p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph 
        
        # related article: {related_title:related_url}
        related_title = [element.text for element in res.select('.popnews-box:nth-child(1) li')] # 相關報導 標題
        related_url = ['https://www.rti.org.tw'+element.get('href') for element in res.select('.popnews-box:nth-child(1) a')] # 相關報導 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []
        
        # video: {video_title:video_url}
        if res.select('iframe') == []: video = []
        else:
            video_title = [res.select('iframe')[0].get('alt')]
            video_url = [res.select('iframe')[0].get('src')]            
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        img_title = [element.text for element in res.select('figure')] # cover in=mg
        img_url = [element.find('img').get('src') for element in res.select('figure')] # cover in=mg
        if res.select('p img')!=[]: 
            img_title.extend([element.text for element in res.select('.news-detail-box span span')])
            img_url.extend([element.get('src') for element in res.select('p img')])
        img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'中央廣播電台'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ######################### 中央廣播電台 (2020大選) ##########################
    #########################################################################
    def rti_all_reader_2020(self):
        n = 1
        while n < 6:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.rti.org.tw/news/list/tag/2020%E5%B0%88%E9%A1%8C/page/'+str(n)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('.newslist-box li')

            all_news = []
            for drink in drinks: # .class # #id
                news_url ='https://www.rti.org.tw' +drink.find('a').get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.rti_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
        

        


    #########################################################################
    ################################ 世界日報 #################################
    #########################################################################
    def worldjournal_all_reader(self):
        n = 1
        while n < 16:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://www.worldjournal.com/topic/%e5%8f%b0%e7%81%a3%e6%96%b0%e8%81%9e%e7%b8%bd%e8%a6%bd/?pno='+str(n)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('h2')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.find('a').get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.worldjournal_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
            
    
            
            

        
            
        


    def worldjournal_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  

        title = res.find('meta', attrs={'property':'og:title'})['content'].split(u' - 世界新聞網')[0]
        author = [res.select('.date span')[0].text.split(u'／')[0]]
        
        tag_list = [element.text for element in res.select('.post-title span')] # tag on web
        if res.find('meta', attrs={'name':'keywords'})!=None: 
            tag_list.extend(res.find('meta', attrs={'name':'keywords'})['content'].split(u',')) # tag behind web
            tag_list = list(set(tag_list)) # unique tag list

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'property':'article:published_time'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S-04:00')       # ex. 2019-09-01T06:10:00-04:00
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        context = ""        
        for p in res.select('.post-content p')[:-1]:
            if len(p) !=0 and u'➤➤➤' not in p.text:
                paragraph = p.text.strip('\n').strip()
                context += paragraph 
 
        # related article: {related_title:related_url}
        related_title = [element.text for element in res.select('.pagination a')] # 相關報導 標題
        related_url = [element.get('href') for element in res.select('.pagination a')] # 相關報導 url
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        if res.select('.post-content p a') == []: recommend_news = [] # no link in article
        else:
            recommend_title = [element.text for element in res.select('.post-content p a')]
            recommend_url = [element.get('href') for element in res.select('.post-content p a')]
            recommend_news = [dict([element]) for element in zip(recommend_title, recommend_url)]

        # video: {video_title:video_url}
        if res.select('p iframe') == []: video = []
        else:
            video_title = [element.get('alt') for element in res.select('p iframe')]
            video_url = [element.get('src') for element in res.select('p iframe')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('.img-holder')==[]: img = [] # no img
        else:
            img_title = [element.find('img').get('alt') for element in res.select('.img-holder')]
            img_url = [element.find('img').get('src') for element in res.select('.img-holder')]
            img = [dict([element]) for element in zip(img_title, img_url)]          

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'世界日報'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ################################ 風向新聞 #################################
    #########################################################################
    def kairos_all_reader(self):        
        n = 1
        while n < 15:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://kairos.news/headlines/politics/page/'+str(n)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('.post-title')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.find('a').get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.kairos_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
            

    
            
            

        
            
        


    def kairos_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  

        title = res.title.text
        tag_list = [element.text for element in res.select('.tagcloud a')]
        author = [res.select('.author-name')[0].text]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'property':'article:published_time'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S+00:00')       # ex. 2019-09-02T09:47:06+00:00
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        context = ""        
        for p in res.select('p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph 
        context = context.split(u'喜歡這篇新聞嗎')[0]
                
        # related article: {related_title:related_url}
        related_title = [element.find('a').get('title') for element in res.select('.related-item')]
        related_url = [element.find('a').get('href') for element in res.select('.related-item')]
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []

        # video: {video_title:video_url}
        if res.select('.fb-video') == []: video = []
        else:
            video_title = [element.get('alt') for element in res.select('.fb-video')]
            video_url = [element.get('data-href') for element in res.select('.fb-video')]
            video = [dict([element]) for element in zip(video_title, video_url)]    
        
        # img: {img_title:img_url}
        img_title = [res.select('.single-featured-image img')[0].get('alt')] # cover ing
        img_url = [res.select('.single-featured-image img')[0].get('src')] # cover img
        if res.select('.wp-caption') != []:  # img in article
            img_title.extend([element.text for element in res.select('.wp-caption-text')])
            img_url.extend([element.find('img').get('src') for element in res.select('.wp-caption')])
        if res.select('.fb-post') != []:  # cite fb posts img
            img_title.extend([element.get('alt') for element in res.select('.fb-post')])
            img_url.extend([element.get('data-href') for element in res.select('.fb-post')])
        img = [dict([element]) for element in zip(img_title, img_url)]  
        
        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'風向新聞'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ################################# 民眾日報 #################################
    #########################################################################
    def mypeople_all_reader(self):
        url = 'http://www.mypeople.tw/index.php?r=site/index&id=22848&channel=1'
        self.browser.get(url)
        jsCode = "var q=document.documentElement.scrollTop=100000" # control distance of scroller on the right
        for x in range(0,15): 
            self.browser.execute_script(jsCode) # keep scrolling to the bottom
            sleep(20)
        text = self.browser.page_source  

        all_news = []
        res = BeautifulSoup(text, features='lxml')
        drinks = res.select('#newslist li')
        
        for drink in drinks: # .class # #id
            news_url = drink.find('a').get('href')      
            
            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                news_dict = self.mypeople_reader(news_url)
                all_news.insert(0, news_dict)
        self.append_2_json(all_news) # save as json file
        

        
            
        


    def mypeople_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  

        title = res.find('meta', attrs={'property':'og:title'})['content']
        tag_list = []

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select('.news_source_date')[0].text
        date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S') # ex. 2019-09-04 16:34:13
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        context = ""        
        for p in res.select('.news_content p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph 
        if u'】' in context: author = [context.split(u'】')[0].split(u'【')[1]]
        elif u'〕' in context: author = [context.split(u'〕')[0].split(u'〔')[1]]
        else: author = []

        # related article: {related_title:related_url}
        related_news = []

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []
        
        # video: {video_title:video_url}
        video = []

        # img: {img_title:img_url}
        if res.select('p img')==[]: img = [] # no context img
        else:   
            img_title = [element.get('alt') for element in res.select('p img')]
            img_url = [element.get('src') for element in res.select('p img')]
            img = [dict([element]) for element in zip(img_title, img_url)]
        
        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'民眾日報'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ################################ 芋傳媒 #################################
    #########################################################################
    def taronews_all_reader(self):  
        #self.taronews_reader('https://taronews.tw/2019/09/11/461962/')
        n = 1
        while n < 173:
            print('================================ page: ' + str(n) + ' ================================')
            url = 'https://taronews.tw/category/politics/page/'+str(n)
            res = requests.get(url)
            text = res.text
            #text = self.get_url_text(url)
            soup = BeautifulSoup(text, "lxml")
            drinks = soup.select('.post-url')[:-5] if n==1 else soup.select('.listing-item-grid-1 .post-url')

            all_news = []
            for drink in drinks: # .class # #id
                news_url = drink.get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    news_dict = self.taronews_reader(news_url)
                    all_news.insert(0, news_dict)
            n+=1
            self.append_2_json(all_news) # save as json file
        
            

    
            
            

        
            
        


    def taronews_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  

        title = res.find('meta', attrs={'property':'og:title'})['content'].split(u' | 芋傳媒 TaroNews')[0]
        tag_list = [element.text for element in res.select('.post-tags a')]
        author = [res.select('.author-title')[0].text]

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.find('meta', attrs={'property':'article:published_time'})['content']
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S+00:00')       # ex. 2019-09-04T17:28:53+08:00
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        context = ""        
        for p in res.select('.single-post-content p'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph         

        # related article: {related_title:related_url}
        related_title = [element.find('a').text.strip('\t').strip() for element in res.select('.item-inner')]
        related_url = [element.find('a').get('href') for element in res.select('.item-inner')]
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []

        # video: {video_title:video_url}
        if res.select('.fb-video') == []: video = []
        else:
            video_title = [element.get('alt') for element in res.select('.fb-video')]
            video_url = [element.get('data-href') for element in res.select('.fb-video')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        img_title = [res.select('.post-header')[0].get('title')] # cover ing
        img_url = [res.select('.post-header')[0].get('data-src')] # cover img
        if res.select('.wp-block-image') != []:  # img in article
            for element in res.select('.wp-block-image'):
                if element.find('figcaption')!=None: img_title.extend([element.find('figcaption').text])
                else: img_title.extend([None])
            img_url.extend([element.find('img').get('src') for element in res.select('.wp-block-image')])
        img = [dict([element]) for element in zip(img_title, img_url)]  

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'芋傳媒'}
        print(title+' '+time)       
        return news_dict
        

        


    #########################################################################
    ############################# Yahoo!奇摩新聞 #############################
    #########################################################################
    def yahoo_all_reader(self):
        url = 'https://tw.news.yahoo.com/politics'
        self.browser.get(url)    
        jsCode = "var q=document.documentElement.scrollTop=100000" # control distance of scroller on the right
        for x in range(0,10): 
            self.browser.execute_script(jsCode) # keep scrolling to the bottom
            sleep(1)
        text = self.browser.page_source

        all_news = []
        res = BeautifulSoup(text, features='lxml')
        drinks = res.select('#Col1-1-Hero-Proxy li, .tdv2-applet-stream h3')
        
        for drink in drinks: # .class # #id
            if 'https://' in drink.find('a').get('href') or 'http://' in drink.find('a').get('href') : continue # skip Yahoo! customize ads
            if '/video/' in drink.find('a').get('href'): continue # skip Yahoo! video (no article text)
            news_url = 'https://tw.news.yahoo.com' + drink.find('a').get('href')            
            
            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                try: news_dict = self.yahoo_reader(news_url)
                except Exception as e: # prevent link to ETtoday's other platform
                    print(news_url); continue
                all_news.insert(0, news_dict)
        self.append_2_json(all_news) # save as json file
        
        
            

        
            
        


    def yahoo_reader(self, url):
        self.browser.get(url)
        text = self.browser.page_source
        res = BeautifulSoup(text, features='lxml')
        
        title = res.title.text.split(u' - Yahoo奇摩新聞')[0]
        if res.find('meta', attrs={'name':'news_keywords'})==None: tag_list = []
        else: tag_list = res.find('meta', attrs={'name':'news_keywords'})['content'].split(u',')
        if res.select('#mrt-node-Col1-5-Tags a')!=[]: 
            for element in res.select('#mrt-node-Col1-5-Tags a'):
                tag_list.extend([element.text.split(u'#')[1] if u'#' in element.text else element.text])
            tag_list = list(set(tag_list)) # unique list
        if res.select('.author-name')!=[]:      author = [res.select('.author-name')[0].text]
        elif res.select('.provider-link')!=[]:  author = [res.select('.provider-link')[0].text]
        elif res.select('.author-link')!=[]:    author = [res.select('.author-link')[0].text]
        else:                                   author = []

        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.select('time')[0].get('datetime')
        date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.000Z')    # ex. 2019-09-03T08:13:25.000Z
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        context = ""
        source = res.select('.auth-logo')[0].get('title') if res.select('.auth-logo')[0].get('title')!=None else u'華視'
        for p in res.select('article p'):
            if u'更多'+source+u'報導' in p.text or u'更多政治相關新聞' in p.text or u'更多相關新聞' in p.text: break # end word in article
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph            

        # related article: {related_title:related_url}
        related_title = [element.text for element in res.select('#mrt-node-Col1-7-RelatedContent ul a')]
        related_url = ['https://tw.news.yahoo.com'+element.get('href') for element in res.select('#mrt-node-Col1-7-RelatedContent ul a')]
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []
        if res.select('p a') == []: recommend_news = []
        else:
            recommend_title = [element.text for element in res.select('p a')]
            recommend_url = [element.get('href') for element in res.select('p a')]
            recommend_news = [dict([element]) for element in zip(recommend_title, recommend_url)]
            if recommend_news[-1].keys()==[u'Yahoo論壇']: recommend_news = recommend_news[:-1] # remove Yahoo論壇 link

        # video: {video_title:video_url}
        if res.select('video') == []: video = []
        else:
            video_title = [element.text for element in res.select('.yvp-start-screen-bar-wrapper h3')] # turn dict in str to dict #.replace("\"","")
            video_url = [element.get('src') for element in res.select('video')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('figure') == []:  img = [] # no img
        else:
            img_title = [element.text for element in res.select('figure figcaption')]
            img_url = [element.get('src') for element in res.select('figure img')[1::2]] # select odd elements to avoid repeat imgs
            img = [dict([element]) for element in zip(img_title, img_url)]

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'Yahoo!奇摩新聞'}
        print(title+' '+time)
        return news_dict
        

        


    #########################################################################
    ###################### Yahoo!奇摩新聞 (2020大選) ##########################
    #########################################################################
    def YAHOOnews_all_reader_2020(self, candidate_name):
        #url = 'https://tw.news.yahoo.com/topic/2020election'
        if candidate_name == "蔡英文": url = 'https://tw.news.yahoo.com/topic/2020election-tsaiingwen'
        elif candidate_name == "韓國瑜": url = 'https://tw.news.yahoo.com/topic/2020election-twherohan/'
        elif candidate_name == "柯文哲": url = 'https://tw.news.yahoo.com/topic/2020election-DoctorKoWJ/'
        else: raise("Unknown candidate name.")
        self.browser.get(url)        
        for x in range(0,10):
            xpath = '//*[@id="Col1-0-TopicWrapper-Proxy"]/div/div[6]/div[2]/div/div/div'
            if x==0: element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))  # check complete loading
            self.browser.find_element_by_xpath(xpath).click()
            sleep(1)
        text = self.browser.page_source

        all_news = []
        res = BeautifulSoup(text, features='lxml')
        drinks = res.select('#TopicHero .Pos\(r\), .TopicList .StreamMegaItem')
        print(len(drinks))

        for drink in drinks: # .class # #id
            if drink.find('a')==None: continue    # avoid non news class
            if drink.select('h3')==[]: news_url = drink.find('a').get('href')  # doen section news
            else: news_url = 'https://tw.news.yahoo.com'+drink.h3.find('a').get('href') # upper section news

            if news_url == self.last_news_url: # reach has read news
                self.append_2_json(all_news)
                raise SyntaxError("Read all news news")
            else:
                try: news_dict = self.yahoo_reader(news_url)
                except Exception as e: # prevent link to ETtoday's other platform
                    print(news_url); continue
                all_news.insert(0, news_dict)
        self.append_2_json(all_news) # save as json file
        
    
        


    #########################################################################
    ############################## Pchome新聞 ################################
    #########################################################################
    def pchome_all_reader(self):
        n = 1
        while n < 20:
            try:
                url = 'http://news.pchome.com.tw/cat/politics/'+str(n)
                #resp = urllib2.urlopen(url).getcode() # check url exist
            except:
                print("Reach the end page.")
                break
        
            print('================================ page: ' + str(n) + ' ================================')
            
            text = self.get_url_text(url)
            soup = BeautifulSoup(text, features='lxml') 
            drinks = soup.select('#catalbk a, a+ p a') if n==1 else soup.select('a+ p a')
            
            all_news = []
            for drink in drinks: # .class # #id
                news_url = 'http://news.pchome.com.tw'+drink.get('href')
                
                if news_url == self.last_news_url: # reach has read news
                    self.append_2_json(all_news)
                    raise SyntaxError("Read all news news")
                else:
                    try:
                        news_dict = self.pchome_reader(news_url)
                        all_news.insert(0, news_dict)
                    except Exception as e:
                        print(news_url)
                        continue
            n+=1
            self.append_2_json(all_news) # save as json file
            

            
        


    def pchome_reader(self, url):
        text = self.get_url_text(url)
        res = BeautifulSoup(text, features='lxml')  

        title = res.find('p', attrs={'class':'article_title'})['title']
        tag_list = [element.text for element in res.select('.ent_kw li:nth-child(1) a')]
        
        author_with_city = False
        citys = [u"台北", u"基隆", u"新北", u"連江", u"宜蘭", u"新竹", u"新竹", u"桃園", u"苗栗", u"台中", u"彰化", u"南投", u"嘉義", u"雲林", u"台南", u"高雄", u"澎湖", u"金門", u"屏東", u"台東", u"花蓮"]
        for city in citys:
            if city in res.time.text: 
                author = [res.time.text.split(u'　')[1].split(city)[0]] # ex. 中央社台北10日電
                if u'記者' in author[0]: author = [author[0].split(u'記者')[1]]   # ex. 中央社記者余祥台北10日電
                if u'、' in res.time.text: author = author[0].split(u'、') # ex. 中央社記者郭芷瑄、楊思瑞屏東縣10日電
                author_with_city = True 
                break           
        if author_with_city == False:
            if u'／' in res.time.text: author = [res.time.text.split(u'　')[1].split(u'／')[1]] # 政治中心／綜合報導
            else: author = [res.time.text.split(u'　')[1]]
        print(author)
        # reported time: {time, time_year, time_month, time_day, time_hour_min}
        time_str = res.time.get('datetime')
        date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')     # ex. 2019-09-04 17:28:53
        time = date_obj.strftime("%Y/%m/%d %H:%M")
        time_detail = [{'time':time, 'time_year':date_obj.strftime("%Y"), 'time_month':date_obj.strftime("%m"), 'time_day':date_obj.strftime("%d"), 'time_hour_min':date_obj.strftime("%H:%M")}]

        # article content
        context = ""        
        for p in res.select('#newsContent div'):
            if len(p) !=0:
                paragraph = p.text.strip('\n').strip()
                context += paragraph         

        # related article: {related_title:related_url}
        related_title = [element.get('title') for element in res.select('.newlist2 li a')]
        related_url = ['http://news.pchome.com.tw'+element.get('href') for element in res.select('.newlist2 li a')]
        related_news = [dict([element]) for element in zip(related_title, related_url)]

        # recommend article: (recommend_title:recommend_url)
        recommend_news = []
        
        # video: {video_title:video_url}
        if res.select('.ytplayer') == []: video = []
        else:
            video_title = [element.get('alt') for element in res.select('.ytplayer')]
            video_url = ['https://www.youtube.com/watch?time_continue=2&v='+element.get('data-value') for element in res.select('.ytplayer')]
            video = [dict([element]) for element in zip(video_title, video_url)]    

        # img: {img_title:img_url}
        if res.select('#newsContent img') == []:  img = [] # no img
        else:
            img_title = [element.get('alt') for element in res.select('#newsContent img')]
            img_url = [element.get('src') for element in res.select('#newsContent img')]
            img = [dict([element]) for element in zip(img_title, img_url)]  

        news_dict = {'title':title, 'author':author, 'context':context, 'url':url, 'tag':tag_list, 'time':time_detail, 'related_news':related_news,'recommend_news':recommend_news, 'source_video':video, 'source_img':img, 'media':'Pchome新聞'}
        print(title+' '+time)   
        return news_dict
        




    #########################################################################
    ################################# 用url #################################
    #########################################################################
    def crawler_by_url(self, url):
        print(url)
        for media in self.media_func.keys():
            if media+'.' in url: 
                try: 
                    news_dict = self.media_func[media](url)
                    print(news_dict['title'])
                    print(news_dict['author'])
                    return news_dict
                except Exception as e: return None
                finally: self.browser.quit()
                



    def get_media_abbr(self): return list(self.media_func.keys())

    def media_cn_2_en(self, media_cn_str, get_abbr):
        media_cn = ["自由時報","蘋果日報","聯合報","中國時報","TVBS","ETtoday","台視","中視","華視","民視","公視","三立新聞","中天新聞","年代新聞","非凡新聞","中央通訊社","關鍵評論網","民報","上報-調查","上報-焦點","大紀元","信傳媒","匯流新聞網","新頭殼","風傳媒","今日新聞","鏡週刊","台灣好新聞","中央廣播電台","世界日報","風向新聞","民眾日報","芋傳媒","Pchome新聞","Yahoo!奇摩新聞"]
        media_en = ["Liberty News", "Apple Daily", "UDN News", "China Times", "TVBS", "ETtoday", "TTV", "CTV", "CTV", "FTV News", "PTS", "STEN", "CTITV", "ERA News", "USTV", "CNA", "The News Lens", "People News", "Up Media", "Up Media", "Epoch Times", "CM Media", "CNEWS", "Newtalk", "Storm Media", "NOW News", "Mirror Media", "Taiwan Hot", "RTI News", "World Journal", "Kairos News", "Mypeople News", "Taro News", "Pchome News", "YAHOO News"]
        media_en_abbr = ["ltn","appledaily","udn","chinatimes","tvbs","ettoday","ttv","ctv","cts","ftv","pts","sten","ctitv","era","ustv","cna","thenewslens","peoplenews","upmedia","upmedia","epochtimes","cmmedia","cnews","newtalk","storm","nownews","mirrormedia","taiwanhot","rti","worldjournal","kairos","mypeople","taronews","pchome","yahoo"]
        
        if get_media_abbr: return media_en_abbr[media_cn.index(media_cn_str)]
        else: return media_en[media_cn.index(media_cn_str)]


    #########################################################################
    ################################ 統一接口 ################################
    #########################################################################
    def crawler_news(self, media_input):
        # crawler media list by user input
        if media_input==str(len(media_list)-1): media_crawler_id_list = range(0,len(media_list)-1) # crawler all media
        elif " " not in media_input and "," not in media_input:  media_crawler_id_list = [int(media_input)] # crawler one media # ex. input = 2
        elif ' ' in media_input: media_crawler_id_list = map(int, media_input.split(" ")) # ex. input = 2 3
        elif ',' in media_input: media_crawler_id_list = map(int, media_input.split(",")) # ex. input= 2,3
        else: print('Input Error: Unknown News Resources!')

        try:
            for media_id in media_crawler_id_list:
                media = media_list[media_id]; print('爬取媒體(Crawlering News): '+media)
                self.output_file = PATH+media+'/'+date.today().strftime("%Y%m%d")+'.json'
                print(self.output_file)
                # get last crawler file date & url, print time              
                if TEST: self.last_news_url = None
                else:
                    last_date = date.today(); last_file = PATH+media+'/'+last_date.strftime("%Y%m%d")+'.json'
                    while not os.path.isfile(last_file): last_file = PATH+media+'/'+last_date.strftime("%Y%m%d")+'.json'; last_date -= timedelta(days=1)
                    last_news = sorted(json.load(open(last_file)), key=lambda k: k['time'])[-1] # py2
                    #last_news = sorted(json.load(open(last_file)), key=lambda k: datetime.strptime(k['time'][0]['time'], '%Y/%m/%d %H:%M'))[-1] # py3
                    self.last_news_url = last_news['url']
                    print(last_news['time']) # last crawler time
                # crawler program for each media
                try:
                    if media == "中國時報(China Times)": self.chinatimes_all_reader()
                    elif media == "自由時報(Liberty News)": self.ltn_all_reader()
                    elif media == "聯合報(UDN News)-要聞": self.udn_all_reader()
                    elif media == "TVBS": self.tvbs_all_reader()
                    elif media == "蘋果日報(Apple Daily)": self.appledaily_all_reader()
                    elif media == "ETtoday": self.ettoday_all_reader()
                    elif media == "台視(TTV)": self.ttv_all_reader()
                    elif media == "中視(CTV)": self.ctv_all_reader()
                    elif media == "華視(CTS)": self.cts_all_reader()
                    elif media == "民視(FTV News)": self.ftv_all_reader()
                    elif media == "公視(PTS)": self.pts_all_reader()
                    elif media == "三立新聞(STEN)": self.sten_all_reader()
                    elif media == "中天新聞(CTITV)": self.ctitv_all_reader() # before this, unrenewed columns:{time, author}
                    elif media == "年代新聞(ERA News)": self.era_all_reader()
                    elif media == "非凡新聞(USTV)": self.ustv_all_reader()
                    elif media == "中央通訊社(CNA)": self.cna_all_reader()
                    elif media == "關鍵評論網(The News Lens)": self.thenewslens_all_reader()
                    elif media == "民報(People News)": self.peoplenews_all_reader()
                    elif media == "上報(Up Media)-調查": self.upmedia_all_reader('調查')
                    elif media == "上報(Up Media)-焦點": self.upmedia_all_reader('焦點')
                    elif media == "大紀元(Epoch Times)": self.epochtimes_all_reader()
                    elif media == "信傳媒(CM Media)": self.cmmedia_all_reader()
                    elif media == "匯流新聞網(CNEWS)": self.cnews_all_reader()                   
                    elif media == "新頭殼(Newtalk)": self.newtalk_all_reader()
                    elif media == "風傳媒(Storm Media)": self.storm_all_reader()
                    elif media == "今日新聞(NOW News)": self.nownews_all_reader()
                    elif media == "鏡週刊(Mirror Media)": self.mirrormedia_all_reader()                   
                    elif media == "新新聞(New7)": self.new7_all_reader()
                    elif media == "台灣好新聞(Taiwan Hot)": self.taiwanhot_all_reader()
                    elif media == "中央廣播電台(RTI News)": self.rti_all_reader()
                    elif media == "世界日報(World Journal)": self.worldjournal_all_reader()
                    elif media == "風向新聞(Kairos News)": self.kairos_all_reader()
                    elif media == "民眾日報(Mypeople News)": self.mypeople_all_reader()
                    elif media == "芋傳媒(Taro News)": self.taronews_all_reader()
                    elif media == "Yahoo!奇摩新聞(YAHOO News)": self.yahoo_all_reader()
                    elif media == "Pchome新聞(Pchome News)": self.pchome_all_reader()
                    elif media == "TVBS-2020選舉": self.tvbs_all_reader_2020()
                    elif media == "聯合報(UDN News)-2020選舉": self.udn_all_reader_2020()
                    elif media == "華視(CTS)-2020選舉": self.cts_all_reader_2020()
                    elif media == "公視(PTS)-2020選舉": self.pts_all_reader_2020()
                    elif media == "今日新聞(NOW News)-2020選舉": self.nownews_all_reader_2020()
                    elif media == "鏡週刊(Mirror Media)-2020選舉-民進黨": self.mirrormedia_all_reader_2020('DPP')
                    elif media == "鏡週刊(Mirror Media)-2020選舉-國民黨": self.mirrormedia_all_reader_2020('KMT')
                    elif media == "鏡週刊(Mirror Media)-2020選舉-民眾黨": self.mirrormedia_all_reader_2020('TPP')
                    elif media == "中央廣播電台(RTI News)-2020選舉": self.rti_all_reader_2020()
                    elif media == "Yahoo!奇摩新聞(YAHOO News)-2020選舉-蔡英文": self.YAHOOnews_all_reader_2020('蔡英文')
                    elif media == "Yahoo!奇摩新聞(YAHOO News)-2020選舉-韓國瑜": self.YAHOOnews_all_reader_2020('韓國瑜')
                    elif media == "Yahoo!奇摩新聞(YAHOO News)-2020選舉-柯文哲": self.YAHOOnews_all_reader_2020('柯文哲')
                    else: raise SyntaxError('Crawler '+media+' Fail.')
                except Exception as except_error:
                    print(except_error)
                    continue
        finally: self.browser.quit()



if __name__ == '__main__':
    """
    # execute by machine shedule
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=24) # keep running in next 24 hours

    while datetime.now() < end_time:
        next_time = datetime.now() + timedelta(hours=3) # execute in each 3 hours
        next_time = next_time.replace(minute=00)

        crawler.read_news("7") # crawler all news media

        while datetime.now() < next_time:
            sleep(20*60) # sleep for 20*60 secs (20 mins)
    """

    #print('\nPlease input the media want to crawler')
    media_list = ["蘋果日報(Apple Daily)","三立新聞(STEN)", "上報(Up Media)-調查", "上報(Up Media)-焦點", "新頭殼(Newtalk)", "民報(People News)","大紀元(Epoch Times)", "鏡週刊(Mirror Media)","中央廣播電台(RTI News)", "民視(FTV News)", "台視(TTV)","全部媒體(ALL)" ]
    #"Yahoo!奇摩新聞(YAHOO News)-2020選舉-蔡英文", "Yahoo!奇摩新聞(YAHOO News)-2020選舉-韓國瑜", "Yahoo!奇摩新聞(YAHOO News)-2020選舉-柯文哲"
    """
    media_list = ["蘋果日報(Apple Daily)","自由時報(Liberty News)","聯合報(UDN News)-要聞","中國時報(China Times)", # paper media
    "TVBS", "ETtoday", "台視(TTV)", "中視(CTV)", "華視(CTS)", "民視(FTV News)", # tv media
    "公視(PTS)", "三立新聞(STEN)", "中天新聞(CTITV)", "年代新聞(ERA News)", "非凡新聞(USTV)", "中央通訊社(CNA)", # tv media
    "關鍵評論網(The News Lens)", "民報(People News)","上報(Up Media)-調查", "上報(Up Media)-焦點", "大紀元(Epoch Times)", "信傳媒(CM Media)", # online media
    "匯流新聞網(CNEWS)", "新頭殼(Newtalk)", "風傳媒(Storm Media)", "今日新聞(NOW News)", "鏡週刊(Mirror Media)",  # online media
    "台灣好新聞(Taiwan Hot)", "中央廣播電台(RTI News)", "世界日報(World Journal)", "風向新聞(Kairos News)", # online media
    "民眾日報(Mypeople News)", "芋傳媒(Taro News)", # online media
    "Pchome新聞(Pchome News)", "Yahoo!奇摩新聞(YAHOO News)", # search web media
    "聯合報(UDN News)-2020選舉", "TVBS-2020選舉", "華視(CTS)-2020選舉", "公視(PTS)-2020選舉", "今日新聞(NOW News)-2020選舉", # 2020 election
    "鏡週刊(Mirror Media)-2020選舉-民進黨", "鏡週刊(Mirror Media)-2020選舉-國民黨", "鏡週刊(Mirror Media)-2020選舉-民眾黨",  # 2020 election
    "中央廣播電台(RTI News)-2020選舉", "Yahoo!奇摩新聞(YAHOO News)-2020選舉-蔡英文", "Yahoo!奇摩新聞(YAHOO News)-2020選舉-韓國瑜", "Yahoo!奇摩新聞(YAHOO News)-2020選舉-柯文哲",   # 2020 election
    "全部媒體(ALL)"]
    """
    for media_id,media in zip(range(0,len(media_list)),media_list): print(str(media_id) + ': ' + media)
    
    # execute by users
    crawler = crawler()
    #crawler.crawler_news(raw_input())
    # py3
    crawler.crawler_news(raw_input())



    # avoid error: Max retries exceeded with url (retry 3 times if connect to url fail)
    #session = requests.Session()
    #retry = Retry(connect=3, backoff_factor=0.5)
    #adapter = HTTPAdapter(max_retries=retry)
    #session.mount('https://', adapter)

    # avoid error: Max retries exceeded with url (connect too much https and don't close)
    #requests.adapters.DEFAULT_RETRIES = 5 # reconnect time to url
    #session = requests.session()
    #session.keep_alive = False # close non-used url
    
    
    """ rerun privious url, save to 'new' file
    import glob
    output_path = '/Users/ritalliou/Desktop/IIS/News_Ideology/myCrawlerResult/politics/new/'
    path = '/Users/ritalliou/Desktop/IIS/News_Ideology/myCrawlerResult/politics/'+media+'/'
    for file_path in glob.glob(path+"*.json"):
        print(file_path)
        with open(file_path) as data_file:
            all_news = []
            articles = json.load(data_file)
            for article in articles:
                try:
                    all_news.insert(0, crawler.YAHOOnews_reader(article['url']))
                except Exception as e:
                    print(article['url'])
                    continue
            with open(output_path+file_path.split(')/')[1], 'ab+') as json_file:
                json.dump(all_news, json_file, indent=4, sort_keys=True)
    """

    


    #httplib2.Http().request(url, 'HEAD')

    #print(requests.head('https://tw.news.appledaily.com/politics/realtime/1').status_code)
    #print(requests.head('https://tw.news.appledaily.com/politics/realtime/20').status_code)
    

    """
    with open(PATH+'自由時報'+'/'+DATE+'.json') as data_file:
        data_loaded = json.load(data_file)
        #data_renew = pd.DataFrame(data_loaded).drop_duplicates().to_dict('r') # remove duplicated dict in the list
        data_renew = {x['url']:x for x in data_loaded}.values() # remove duplicated dict by url in the list
        data_renew = sorted(data_renew, key=lambda k: k['time']) # sort time by acend
        json.dump(data_renew, data_file, indent=4, sort_keys=True)
    """













#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(json.dumps(xmltodict.parse(my_xml)))

"""
addItem = {'title': drink.get_text(),'href' : drink.find('a').get('href')}
obj['article'].append(addItem)
with open('bonze.json', 'w') as f:
    json.dump(obj,f,ensure_ascii=False,sort_keys = True ,indent = 4)


import json
import feedparser # read RSS file

def get_data_rss():
    rss_url = 'https://udn.com/rssfeed/news/2/6638/12702?ch=news'
    rss = feedparser.parse(rss_url)
    
    #feeds = feedparser.parse(rss_url) # 获得订阅
    #print(rss.version) # 获得rss版本
    # 获得Http头
    #print(rss.headers)
    #print(rss.headers.get('content-type')) 
    #print(rss['feed']['title']) # rss的标题   
    #print(feeds['feed']['link']) # 链接   
    #print(rss.feed.subtitle) # 子标题 
    #print(len(feeds['entries'])) # 查看文章数量
    #print(rss['entries'][0]['title']) # 获得第一篇文章的标题
    #print(feeds.entries[0]['link']) # 获得第一篇文章的链接
    #print(rss.entries[0]['updated']) # Tue, 25 Jun 2019 15:53:57 +0800
    #print(rss.entries[0]['updated_parsed']) # time.struct_time(tm_year=2019, tm_mon=6, tm_mday=25, tm_hour=7, tm_min=53, tm_sec=57, tm_wday=1, tm_yday=176, tm_isdst=0)
    #print('title2 ' + rss.entries[0]['title']) #print('title1 ' + rss['entries'][0]['title'])
    #print(rss.entries[0]['title_detail']['value'])
    #print('link ' + rss.entries[0]['link'])
    #print('summary ' + rss.entries[0]['summary'])

    for post in rss.entries:
        title = post.title
        url = post.link
def get_data_Xpath(url):
    session = requests.Session()
    req = session.get(url)
    #req.encoding = 'utf8'
    html = etree.HTML(req.content)
    my_xpath = '//*[(@id = "pack2")] | //*[(@id = "pack1")] | //*[contains(concat( " ", @class, " " ), concat( " ", "img", " " ))]'
    result = html.xpath(my_xpath)
    print(result)

    session = requests.Session()
    for id in [1,2]:
        URL = 'https://movie.douban.com/top250/?start=' + str(id)
        req = session.get(URL)
        # 设置网页编码格式
        req.encoding = 'utf8'
        # 将request.content 转化为 Element
        root = etree.HTML(req.content)
        # 选取 ol/li/div[@class="item"] 不管它们在文档中的位置
        items = root.xpath('//ol/li/div[@class="item"]')
        for item in items:
            print(item)
            # 注意可能只有中文名，没有英文名；可能没有quote简评
            rank, name, alias, rating_num, quote, url = "", "", "", "", "", ""
            try:
                title = item.xpath('./div[@class="info"]//a/span[@class="title"]/text()') 
                name = title[0].encode('gb2312', 'ignore').decode('gb2312') # 中文名
                alias = title[1].encode('gb2312', 'ignore').decode('gb2312') if len(title) == 2 else "" # 英文名
                rank = item.xpath('./div[@class="pic"]/em/text()')[0] # 排名          
                rating_num = item.xpath('.//div[@class="bd"]//span[@class="rating_num"]/text()')[0] # 评分
                quote_tag = item.xpath('.//div[@class="bd"]//span[@class="inq"]') # 简介tag
                if len(quote_tag) is not 0: quote = quote_tag[0].text.encode('gb2312', 'ignore').decode('gb2312').replace('\xa0', '') # 简介
            except:
                print('faild!')
                pass

def get_CHDTV():
    for page in range(1,1):
        url - 'https://www.chinatimes.com/politic/total?page=' + page + '&chdtv'
        data = json.loads(urllib2.urlopen(query_url).read())
        return data

def utfy_dict(dic):
    if isinstance(dic,unicode):
            return(dic.encode("utf-8"))
        elif isinstance(dic,dict):
            for key in dic:
                dic[key] = utfy_dict(dic[key])
            return(dic)
        elif isinstance(dic,list):
            new_l = []
            for e in dic:
                new_l.append(utfy_dict(e))
            return(new_l)
        else:
            return(dic)

def csv_print():
    url = 'https://www.chinatimes.com/politic/total?page=2&chdtv'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

    obj = {}
    obj['article'] = []

    url = 'https://www.chinatimes.com/realtimenews/20190625002010-260407?chdtv'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    #soup = BeautifulSoup(res.text, "lxml")
    #print(soup.find('h1').get_text())
    #my_xml = soup.find('script').text # find_all("html_element", class_="class_name")


    #print(soup.prettify())
    #print(soup.title.string)
    #print(soup.script.string)
    #print(json.loads(soup.script.string, encoding='utf-8')) #a = yaml.safe_load(soup.script.string)
    a = json.loads(soup.script.string)
    #print(a)
    a = [{u'dateModified': u'2019-06-25T12:23:50&#x2B;08:00', u'author': {u'@type': u'Person', u'name': u'\u8b1d\u96c5\u67d4'}, u'headline': u'\u6731\u7acb\u502b\u6c11\u8abf\u66b4\u885d \u8b1d\u5bd2\u51b0\u795e\u5206\u6790\u5f15\u767c\u71b1\u8b70', u'image': {u'url': u'https://images.chinatimes.com/newsphoto/2019-06-25/900/20190625002013.jpg', u'width': 656, u'@type': u'ImageObject', u'height': 487}, u'publisher': {u'logo': {u'url': u'https://static.chinatimes.com/images/2019/category-logo/logo-ct-politic.png', u'width': 260, u'@type': u'ImageObject', u'height': 60}, u'@type': u'Organization', u'name': u'\u653f\u6cbb - \u4e2d\u6642\u96fb\u5b50\u5831'}, u'datePublished': u'2019-06-25T12:23:50&#x2B;08:00', u'articleSection': u'\u653f\u6cbb', u'mainEntityOfPage': {u'@id': u'https://www.chinatimes.com/realtimenews/20190625002010-260407?chdtv', u'@type': u'WebPage'}, u'@context': u'https://schema.org', u'@type': u'NewsArticle'}, {u'dateModified': u'2019-06-25T12:23:50&#x2B;08:00', u'author': {u'@type': u'Person', u'name': u'\u8b1d\u96c5\u67d4'}, u'headline': u'\u6731\u7acb\u502b\u6c11\u8abf\u66b4\u885d \u8b1d\u5bd2\u51b0\u795e\u5206\u6790\u5f15\u767c\u71b1\u8b70', u'image': {u'url': u'https://images.chinatimes.com/newsphoto/2019-06-25/900/20190625002013.jpg', u'width': 656, u'@type': u'ImageObject', u'height': 487}, u'publisher': {u'logo': {u'url': u'https://static.chinatimes.com/images/2019/category-logo/logo-ct-politic.png', u'width': 260, u'@type': u'ImageObject', u'height': 60}, u'@type': u'Organization', u'name': u'\u653f\u6cbb - \u4e2d\u6642\u96fb\u5b50\u5831'}, u'datePublished': u'2019-06-25T12:23:50&#x2B;08:00', u'articleSection': u'\u653f\u6cbb', u'mainEntityOfPage': {u'@id': u'https://www.chinatimes.com/realtimenews/20190625002010-260407?chdtv', u'@type': u'WebPage'}, u'@context': u'https://schema.org', u'@type': u'NewsArticle'}]
    #fd = codecs.open('/Users/ritalliou/Desktop/news.json', 'wb', 'utf-8')
    #fd.write(a[1].keys())
    for n in range(0,len(a)):
        print( a[n])
        print( a[n].values())
        #fd.write(a[n].values())
        print('\n')
    #fd.close()


    # original print for csv files
    fd = codecs.open('/Users/ritalliou/Desktop/news.json', 'wb', 'utf-8')  
    for c in json.loads(soup.script.string) :
        fd.write( json.dumps(c) [1:-1] )   # json dumps writes ["a",..]
        fd.write('\n')
    fd.close()


    with open('/Users/ritalliou/Desktop/news.csv','w') as f:
        #f.write(u'\ufeff'.encode('utf8'))
        #listOfStr = ["hello", "at" , "test" , "this" , "here" , "now"]
        #listOfInt = [56, 23, 43, 97, 43, 102]
        #zipbObj = zip(listOfStr, listOfInt) # Create a zip object from two lists
        #dictOfWords = dict(zipbObj) # Create a dictionary from zip object

        writedCsv = csv.DictWriter(f, a.keys())
        writedCsv.writeheader()
        writedCsv.writerows([a])
"""