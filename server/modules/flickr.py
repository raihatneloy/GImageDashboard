import os
import json

class Flickr:
    def get_flickr_users(self, keyword):
        url = 'https://www.flickr.com/search/people/?username=%s' % keyword

        html = os.popen('curl "%s"' % url).read()
        index1 = html.find('{"_data":[{') + 9
        data = html[index1:]
        index2 = data.find('"}]')+2
        data = json.loads(data[:index2+1])

        info = []

        for user in data:
            body = {}

            body['username'] = user['username']
            body['name'] = user['realname']
            body['flickr_id'] = user['id']
            body['follower'] = user['followersCount']
            body['picture'] = 'http://farm%s.staticflickr.com/%s/buddyicons/%s.jpg' % (user['iconfarm'], user['iconserver'], user['id'])

            info.append(body)

        return info