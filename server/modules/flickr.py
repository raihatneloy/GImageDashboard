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

            body['username'] = user.get('username')
            body['name'] = user.get('realname', body['username'])
            body['flickr_id'] = user.get('id')
            body['follower'] = user.get('followersCount', 0)
            body['picture'] = 'http://farm%s.staticflickr.com/%s/buddyicons/%s.jpg' % (user['iconfarm'], user['iconserver'], user['id'])

            if body['name'] == '':
                body['name'] = body['username']

            info.append(body)

        return info