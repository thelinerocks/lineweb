import time
import numpy as np
import json
from picture_classifier import *
from RandomImages import *
from instagram import *
from text_sentiment import *
import os



class get_values(object):
    def __init__(self):
        self.mins_index = 0
        self.hours_index = 0
        self.secs_index = 0
        self.hours = np.zeros(24)
        self.mins = np.zeros(60)
        self.secs = np.zeros(6)
        self.interval = 10
        self.oldtime = round(time.time())
        self.localtime = round(time.time())
        data_list = []
        self.id = 0
        self.social_text = []
        self.url = []
        documents = {}

    def add_values(self,url):
        while True:
            self.localtime = round(time.time())
            data_list = []
            self.id = 0
            self.social_text = []
            self.url = []
            documents = {}

            while self.localtime-self.oldtime < 10:
                self.get_insta()
                self.get_twitter()
                self.localtime = time.time()

            documents['documents'] = self.social_text
            results = get_text_sentiment(documents)
            value = sum(self.url)
            self.secs_index = int((self.secs_index+1)%(60/self.interval))
            self.secs[self.secs_index] = value

            if(time.localtime(self.localtime).tm_hour != self.hours[self.hours_index]):
                self.hours_index = time.localtime(self.localtime).tm_hour
                self.hours[self.hours_index] = np.sum(self.mins)
            if(time.localtime(self.localtime).tm_min != self.mins_index):
                self.mins_index = time.localtime(self.localtime).tm_min
                self.mins[self.mins_index] = np.sum(self.secs)
            self.calculate_value()
            self.oldtime = self.localtime
            print(self.calculate_value())

    def calculate_value(self):
        value = np.sum(self.hours)*5 + np.sum(self.mins)**1.5 + np.sum(self.secs) ** 2
        return value

    def get_twitter(self):
        if not os.path.exists('twitter'):
            os.makedirs('twitter')
        tweets = os.listdir('twitter')
        numbers = []
        for i in tweets:
            numbers.append(int(i.split('.')[0]))
        numbers = sorted(numbers)
        for i in numbers:
            filename = str(i) + '.json'
            with open(os.path.join('twitter',filename),'r') as file:
                data = json.loads(file.read())
                if 'url' in data:
                    if '.png' in data['url'] or '.jpg' in data['url']:
                        self.url.append(get_data(data['url']))
                if 'text' in data:
                    text = {}
                    text['id'] = str(self.id)
                    text['language'] = 'en'
                    text['text'] = data['text']
                    self.social_text.append(text)
            os.remove(os.path.join('twitter',filename))

    def get_insta(self):
        posts = get_instagram_posts("faces", self.localtime - (60*60*48), host="http://108.61.175.107:3000", limit=20)
        for post in posts:
            self.url.append(get_data(post['url']))
            text = {}
            text['id'] = str(self.id)
            text['language'] = 'en'
            text['text'] = post['text']
            self.social_text.append(text)
            self.id = self.id+1

gv = get_values()
#gv.get_twitter()

print(gv.add_values(url = 'https://media1.s-nbcnews.com/j/newscms/2016_30/1639976/160726-keith-weglin-713p_801485078c1d37cb8920b8a779546666.nbcnews-ux-2880-1000.jpg'))