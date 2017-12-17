from bs4 import BeautifulSoup
import requests
import urllib2
import json


class Flickr:
    def get_soup(self, url, header):
        return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)), 'html.parser')

    def get_flickr_users(self, keyword):
        keyword = keyword.split()
        keyword = '%20'.join(keyword)
        url = 'https://www.flickr.com/search/people/?username=%s' % keyword

        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        html = self.get_soup(url, header).text
        index1 = html.find('{"_data":[{') + 9
        data = html[index1:]
        index2 = data.find('"}]')+2
        data = json.loads(data[:index2+1])

        info = []

        for user in data:
            body = {}

            body['username'] = user.get('username')
            body['name'] = user.get('realname', body['username'])
            body['flickr_id'] = user.get('id')
            body['follower'] = user.get('followersCount', 0)
            body['picture'] = 'http://farm%s.staticflickr.com/%s/buddyicons/%s.jpg' % (user['iconfarm'], user['iconserver'], user['id'])

            if body['name'] == '':
                body['name'] = body['username']

            info.append(body)

        return info
