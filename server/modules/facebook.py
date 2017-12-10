import requests

class facebook:
    access_token = None

    def __init__(self, client_id, client_secret):
        self.access_token = requests.get('https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials' % (client_id, client_secret)).json()['access_token']
        print self.access_token

    def get_pages(self, keyword):
        api_url = 'https://graph.facebook.com/search?q=%s&type=page&limit=100&fields=name,cover,picture&access_token=%s' % (keyword, self.access_token)

        response = requests.get(api_url)
        page_data = response.json()['data']
        page_infos = []

        for page in page_data:
            page_info = {}

            page_info['name'] = page.get('name')
            page_info['id'] = page.get('id')

            if page.get('cover') and page['cover'].get('source'):
                page_info['cover'] = page['cover']['source']

            if page.get('picture') and page['picture'].get('data'):
                page_info['picture'] = page['picture']['data']['url']

            page_infos.append(page_info)

        return page_infos