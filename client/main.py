from flask import Flask, jsonify, request, render_template, session, url_for, redirect
from flask_script import Manager
from flask_jsglue import JSGlue
from tables.authentication import Login, Register
from werkzeug.datastructures import ImmutableMultiDict
import os
import json
import requests
import yaml

# Directories
client_dir = os.path.dirname(os.path.abspath(__file__))

# Load config file
configs = yaml.load(open('%s/config/configuration.yaml' % client_dir).read())

# Initialize app
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='7d441f27d441f27567d441f2b6176a'
)

# Backend url
server_endpoint = configs.get('server_endpoint')

# Add Manager
manager = Manager(app)

# Configure JSGlue
jsglue = JSGlue(app)

@app.route('/login')
def login():
    if session.get('user'):
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
    if session.get('user'):
        del session['user']
    return redirect(url_for('login', _external=True))


@app.route('/search', defaults={'keyword': None})
@app.route('/search/gimage', defaults={'keyword': None})
@app.route('/search/<keyword>')
@app.route('/search/gimage/<keyword>')
def search(keyword):
    search_result = None

    if keyword == '':
        return redirect(url_for('search'))

    if keyword:
        search_result = requests.get('%s/images/%s' % (server_endpoint, keyword)).json()

    global searched_images
    searched_images = search_result
    session['searched_images'] = search_result
    print session['searched_images']

    return render_template('search.html', images=search_result, type='gimage')


@app.route('/search/fbpost', defaults={'keyword': None})
@app.route('/search/fbpost/<keyword>')
def search_fb(keyword):
    return render_template('search.html', images=None, type='facebook')


@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    x = request.form.to_dict(flat=False)
    selected_images = None
    for key, value in x.iteritems():
        selected_images = key
    
    selected_images = json.loads(selected_images)
    image_objects = []
    global searched_images
    
    for index in selected_images['images']:
        print searched_images[int(index)-1]
        image_objects.append(searched_images[int(index)-1])

    print image_objects

    response = requests.post(
        '%s/favorite' % server_endpoint,
        json={
            'images': image_objects, 
            'username': session['user'],
            'email': session['email']
        }
    )
    print response.json()

    return jsonify({"Success": True})


@app.route('/dashboard')
def dashboard():
    username = session['user']

    response = requests.get(
        '%s/get_favorites/%s' % (server_endpoint, username)
    )

    return render_template('dashboard.html', fav_images=response.json())


@app.route('/')
def index():
    if not session.get('user'):
        return redirect(url_for('login', _external=True))
    return render_template('index.html')


if __name__ == "__main__":
    manager.run()
