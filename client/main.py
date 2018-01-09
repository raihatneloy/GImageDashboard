from flask import Flask, jsonify, request, render_template, session, url_for, redirect
from flask_script import Manager
from flask_jsglue import JSGlue
from OpenSSL import SSL
from tables.authentication import Login, Register
from werkzeug.datastructures import ImmutableMultiDict
from urlparse import urlparse
from PIL import Image
import os
import json
import requests
import yaml

# Directories
client_dir = os.path.dirname(os.path.abspath(__file__))

# Load config file
configs = yaml.load(open('%s/config/configuration.yaml' % client_dir).read())

# SSL config
if os.path.exists(configs['ssl_key_file']):
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.use_privatekey_file(configs['ssl_key_file'])
    context.use_certificate_file(configs['ssl_crt_file'])

# Initialize app
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='7d441f27d441f27567d441f2b6176a',
    SSL_CONTEXT=context if os.path.exists(configs['ssl_key_file']) else None
)

# Backend url
server_endpoint = configs.get('server_endpoint')

# Add Manager
manager = Manager(app)

# Configure JSGlue
jsglue = JSGlue(app)

# Facebook API's
fb_oauth_uri = 'https://www.facebook.com/v2.11/dialog/oauth'


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    response.headers['Pragma'] = 'no-cache'

    return response


@app.route('/get_fbinfo')
def get_fbinfo():
    if session.get('facebook_id'):
        del session['facebook_id']
        del session['facebook_name']
    
    response = requests.post(
            '%s/get_fbuser_token' % server_endpoint,
            json={
                'username': session.get('user')
            }
        ).json()

    session['facebook_id'] = response.get('facebook_id')
    session['facebook_name'] = response.get('facebook_name')

    return jsonify(response)


def check_auth():
    if not session.get('user'):
        return False

    get_fbinfo()

    return True


@app.route('/login')
def login():
    if check_auth():
       return redirect(url_for('index', _external=True))

    return render_template('login.html')

searched_images = None


@app.route('/authenticate', methods=['POST'])
def authenticate():
    login_form = Login(request.form)

    if login_form.validate():
        response = requests.post(
            '%s/authentication' % server_endpoint,
            json=request.form
        )

        if response.json().get('Success'):
            session['user'] = response.json().get('username')
            session['name'] = response.json().get('name')
            session['email'] = response.json().get('email')
            session['avatar'] = response.json().get('name')[0].upper()
            session['facebook_name'] = response.json().get('facebook_name')
            session['facebook_id'] = response.json().get('facebook_id')

        return json.dumps(response.json())
    else:
        return json.dumps(login_form.errors)


@app.route('/register', methods=['POST'])
def register():
    register_form = Register(request.form)

    if register_form.validate():
        response = requests.post(
            '%s/register/new_user' % server_endpoint,
            json=request.form
        )

        return json.dumps(response.json())
    else:
        return json.dumps(register_form.errors)


@app.route('/logout')
def logout():
    if check_auth():
        del session['user']
    return redirect(url_for('login', _external=True))


@app.route('/fb_auth')
def fb_auth():
    get_fbinfo()

    if session.get('facebook_id'):
        return redirect(url_for('search_fb'))

    uri = '%s?client_id=%s&redirect_uri=%s&response_type=token' % (fb_oauth_uri, configs['facebook_client_id'], url_for('fb_callback', _external=True))

    return redirect(uri)


@app.route('/fb_callback')
def fb_callback():
    return '''  <script type="text/javascript">
                    var token = window.location.href.split("access_token=")[1]; 
                    window.location = "/facebook/callback?access_token=" + token;
                </script> '''


@app.route('/facebook/callback', methods=['GET', 'POST'])
def facebook_callback():
    access_token = request.args.get("access_token")
    print access_token

    if access_token == "undefined":
        flash("You denied the request to sign in.", "error")
        return redirect(url_for('index'))

    response = requests.post(
            "%s/add_fbuser" % server_endpoint,
            json={
                "access_token": access_token,
                "username": session["user"]
            }
        )

    session["facebook_name"] = response.json()['facebook_name']
    session["facebook_id"] = response.json()['facebook_id']

    return redirect(url_for('search_fb'))


@app.route('/fb_auth_remove')
def fb_auth_remove():
    check_auth()
    response = requests.post(
            '%s/remove_fbuser' % server_endpoint,
            json={
                'facebook_id': session['facebook_id']
            }
        )

    del session['facebook_id']
    del session['facebook_name']

    return redirect(url_for('search_fb'))


@app.route('/search', defaults={'keyword': None})
@app.route('/search/gimage', defaults={'keyword': None})
@app.route('/search/<keyword>')
@app.route('/search/gimage/<keyword>')
def search(keyword):
    if not check_auth():
        return redirect(url_for('login', _external=True))

    search_result = None

    if keyword == '':
        return redirect(url_for('search'))

    if keyword:
        search_result = requests.get('%s/images/%s' % (server_endpoint, keyword)).json()

    global searched_images
    searched_images = search_result

    if searched_images:
        for image in searched_images:
            image['base_url'] = urlparse(image['link']).netloc

    return render_template('search.html', images=search_result, type='gimage')


@app.route('/search/fbpost', defaults={'keyword': None})
@app.route('/search/fbpost/<keyword>')
def search_fb(keyword):
    if not check_auth():
        return redirect(url_for('login', _external=True))

    search_result = None

    if keyword:
        search_result = requests.get('%s/pages/%s' % (server_endpoint, keyword)).json()

    global searched_images
    searched_images = search_result

    return render_template('search.html', images=search_result, type='facebook')


@app.route('/search/500px', defaults={'keyword': None})
@app.route('/search/500px/<keyword>')
def search_500px(keyword):
    if not check_auth():
        return redirect(url_for('login', _external=True))

    search_result = None
    global searched_images
    print keyword
    if keyword == '':
        return redirect(url_for('search_500px'))

    if keyword and keyword != 'None':
        print keyword
        search_result = requests.get('%s/_500px/%s' % (server_endpoint, keyword)).json()
        searched_images = search_result
    
    print keyword
    print searched_images

    return render_template('search.html', images=search_result, type='500px')


@app.route('/search/flickr', defaults={'keyword': None})
@app.route('/search/flickr/<keyword>')
def search_flickr(keyword):
    if not check_auth():
        return redirect(url_for('login', _external=True))

    search_result = None
    global searched_images

    if keyword == '':
        return redirect(url_for('search_flickr'))

    if keyword and keyword != 'None':
        search_result = requests.get('%s/flickr/%s' % (server_endpoint, keyword)).json()
        searched_images = search_result

    return render_template('search.html', images=search_result, type='flickr')


@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    x = request.form.to_dict(flat=False)
    selected_images = None
    print x
    for key, value in x.iteritems():
        selected_images = key
    
    selected_images = json.loads(selected_images)
    image_objects = []
    global searched_images
    
    for index in selected_images['images']:
        #print searched_images[int(index)-1]
        image_objects.append(searched_images[int(index)-1])

    #print image_objects

    response = requests.post(
        '%s/favorite' % server_endpoint,
        json={
            'images': image_objects, 
            'username': session['user'],
            'email': session['email']
        }
    )
    #print response.json()

    return jsonify({"Success": True})


@app.route('/add_page', methods=['POST'])
def add_page():
    x = request.form.to_dict(flat=False)
    print x
    selected_pages = None

    for key, value in x.iteritems():
        selected_pages = key

    selected_pages = json.loads(selected_pages)
    page_objects = []
    global searched_images
    #print searched_images

    for id in selected_pages['pages']:
        #print id
        for page in searched_images:
            if id == page['id']:
                page_objects.append(page)
                break

    response = requests.post(
        '%s/pinpage' % server_endpoint,
        json={
            'pages': page_objects,
            'username': session['user'],
            'email': session['email']
        }
    )

    return jsonify({"Success": True})


@app.route('/add_500px', methods=['POST'])
def add_500px():
    x = request.form.to_dict(flat=False)

    selected_500px = None

    for key, value in x.iteritems():
        selected_500px = key
    
    selected_500px = json.loads(selected_500px)
    print selected_500px
    _500px_objects = []
    global searched_images
    print searched_images

    for id in selected_500px['users']:
        for user in searched_images:
            if int(id) == int(user['_500pxid']):
                print id, user['_500pxid']
                _500px_objects.append(user)

    response = requests.post(
        '%s/pin500px' % server_endpoint,
        json={
            'users': _500px_objects,
            'username': session['user'],
            'email': session['email']
        }
    )

    return jsonify({'Success': True})


@app.route('/add_flickr', methods=['POST'])
def add_flickr():
    x = request.form.to_dict(flat=False)

    selected_flickr = None

    for key, value in x.iteritems():
        selected_flickr = key

    selected_flickr = json.loads(selected_flickr)
    flickr_objects = []
    global searched_images

    for id in selected_flickr['flickr']:
        for user in searched_images:
            if str(id) == str(user['flickr_id']):
                flickr_objects.append(user)

    response = requests.post(
        '%s/pinflickr' % server_endpoint,
        json={
            'flickr': flickr_objects,
            'username': session['user'],
            'email': session['email']
        }
    )

    return jsonify({'Success': True})


@app.route('/dashboard')
def dashboard():
    username = session['user']

    response = requests.get(
        '%s/get_favorites/%s' % (server_endpoint, username)
    ).json()

    response2 = requests.get(
        '%s/get_pinpages/%s' % (server_endpoint, username)
    ).json()

    response3 = requests.get(
        '%s/get_500px/%s' % (server_endpoint, username)
    ).json()

    response4 = requests.get(
        '%s/get_flickr/%s' % (server_endpoint, username)
    ).json()

    if response:
        for image in response:
            image['base_url'] = urlparse(image['link']).netloc

    return render_template('dashboard.html', fav_images=response, pin_pages=response2, pin_500px=response3, pin_flickr=response4)


@app.route('/certify', methods=['GET', 'POST'])
def certify():
    if not check_auth():
        return redirect(url_for('login', _external=True))
    return render_template('certificate.html')


@app.route('/badge', methods=['GET'])
def badge():
    if not check_auth():
        return redirect(url_for('login', _external=True))
    return render_template('badge.html')


@app.route('/badge_info', methods=['POST'])
def badge_info():
    data = request.form.to_dict(flat=False)
    print data
    response = requests.post(
            '%s/add_badge' % server_endpoint,
            json=data
        ).json()

    return jsonify(response)


@app.route('/get_badge_info/<id>', methods=['GET'])
def get_badge_info(id):
    response = requests.get(
            '%s/badge/%s' % (server_endpoint, id)
        ).json()

    return jsonify(response)


@app.route('/getbadge', defaults={'id': None, 'size': 300})
@app.route('/getbadge/<id>', defaults={'size': 300})
@app.route('/getbadge/<id>/<int:size>')
def getbadge(id, size):
    if id is None:
        return "<html>Error! No badge ID found</html>"

    response = requests.get(
            '%s/badge/%s' % (server_endpoint, id)
        ).json()

    variables = {}
    variables['data'] = response
    variables['id'] = id
    variables['size'] = size

    variables['country_size'] = size/100 - (0 if len(response['country']) < 9 else 1)
    variables['catagory_size'] = size/100 -(0 if len(response['catagory']) < 9 else 1)
    variables['month_size'] = size/100 - (0 if len(response['month']) < 9 else 1)
    variables['year_size'] = size/100 - (0 if len(response['year']) < 9 else 1)

    return render_template('badge_show.html', vars=variables)


@app.route('/save_file', methods=['POST'])
def save_file():
    upload_path = '%s/static/upload/%s.jpg' % (os.path.dirname(os.path.realpath(__file__)), request.form['name'])

    with open(upload_path, "w") as fp:
        request.files['profile-picture'].save(fp)

    img = Image.open(upload_path)
    img.save(upload_path, optimize=True,quality=40)

    return jsonify({"success": True})


@app.route('/rotate', methods=['POST'])
def rotate():
    upload_path = '%s/static/upload/%s.jpg' % (os.path.dirname(os.path.realpath(__file__)), request.form['name'])
    img = Image.open(upload_path)
    img = img.convert('RGB')
    rotated_img = img.rotate(int(request.form['angle']), expand=True)
    rotated_img.save(upload_path)

    return jsonify({"success": True})


@app.route('/')
def index():
    if not session.get('user'):
        return redirect(url_for('login', _external=True))
    return render_template('index.html')


if __name__ == "__main__":
    manager.run()
