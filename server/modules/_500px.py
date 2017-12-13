import requests

class _500px:
    consumer_key = None

    def __init__(self, consumer_key):
        self.consumer_key = consumer_key

    def get_users(self, keyword):
        api_url = 'https://api.500px.com/v1/users/search?term=%s&page=1&rpp=100&consumer_key=%s' % (keyword, self.consumer_key)

        users_data = requests.get(api_url).json()['users']
        users_info = []

        for user in users_data:
            user_info = {}

            user_info['name'] = user.get('fullname')
            user_info['_500pxid'] = user.get('id')
            user_info['username'] = user.get('username')
            user_info['cover'] = user.get('cover_url')
            user_info['picture'] = user.get('userpic_url')

            users_info.append(user_info)

        return users_info