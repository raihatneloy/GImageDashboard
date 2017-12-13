from flask import Flask, jsonify, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from modules import get_images_url as gsearch
from modules.facebook import facebook
from models.users import users_model as users
from models.users import add_new_user as new_user
from models.fbpages import pages_model as pages
from models.fbpages import get_page
from models.fbusers import fbuser_model as fb_user
from models.images import images_model as images
from models.images import get_image
import base64
import json
import requests
import yaml
import os


# Directories
server_dir = os.path.dirname(os.path.abspath(__file__))

# Load config file
configs = yaml.load(open('%s/config/configuration.yaml' % server_dir).read())

# Load database configs
db_host = configs.get('db_config').get('host') or 'localhost'
db_port = configs.get('db_config').get('port') or 3306
db_username = configs.get('db_config').get('username') or 'root'
db_password = configs.get('db_config').get('password') or ''
db_name = configs.get('db_config').get('database') or 'GImageDashboard'

# Initialize app
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='mysql://%s:%s@%s:%s/%s' % (db_username, db_password, db_host, db_port, db_name),
    OAUTH1_PROVIDER_ENFORCE_SSL=False,
    SEND_FILE_MAX_AGE_DEFAULT=0
)

# Initialize db
db = SQLAlchemy(app)
Users, favorite_images, pinned_pages = users(db)
Images = images(db)
Pages = pages(db)
FBUsers = fb_user(db)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Initialize facebook class
fb = None


@app.route('/privacy')
def privacy():
    return "<h2>All privraecy and rights reserved</h2>"


@app.route('/images/<query>', methods=['GET'])
def get_images(query):
    query = query.replace('%20', ' ')
    image_links = gsearch.get_images(query)

    return jsonify(image_links)


@app.route('/pages/<query>', methods=['GET'])
def get_pages(query):
    query = query.replace('%20', ' ')
    pages = fb.get_pages(query)

    return jsonify(pages)


@app.route('/register/new_user', methods=['POST'])
def register_new_user():
    data = json.loads(request.data)
    data['password'] = base64.b64encode(data['password'])
    ret = new_user(db, Users, data)

    return jsonify(ret)


@app.route('/authentication', methods=['POST'])
def authenticate_user():
    data = json.loads(request.data)

    identity = data.get('identity')
    password = base64.b64encode(data.get('password'))

    user = Users.query.filter((Users.username == identity) | (Users.email == identity)).first()

    if user is None:
        return jsonify({"Error": "Invalid username/email"})

    if user.password != password:
        return jsonify({"Error": "Password mismatch"})

    fb_info = FBUsers.query.join(Users).filter(Users.id == user.id).first()

    auth_response = {
        "Success": "Login successful",
        "username": user.username,
        "name": user.name,
        "email": user.email
    }

    if fb_info:
        auth_response['facebook_name'] = fb_info.name
        auth_response['facebook_id'] = fb_info.fbid

    return jsonify(auth_response)


@app.route('/add_fbuser', methods=['POST'])
def add_fbuser():
    global fb

    data = json.loads(request.data)

    access_token = data['access_token']
    fb = facebook(access_token)
    user_fb_info = requests.get('https://graph.facebook.com/me?access_token=%s' % access_token)

    username = data['username']

    user_object = Users.query.filter(Users.username == username).first()
    fbuser_object = FBUsers(user_fb_info.json()['name'], user_fb_info.json()['id'], access_token)
    user_object.fbuser.append(fbuser_object)

    db.session.commit()

    return jsonify({
        'facebook_name' : user_fb_info.json()['name'],
        'facebook_id': user_fb_info.json()['id']
    })


@app.route('/remove_fbuser', methods=['POST'])
def remove_fbuser():
    data = json.loads(request.data)

    fb_info = FBUsers.query.filter(FBUsers.fbid == data['facebook_id']).first()

    db.session.delete(fb_info)
    db.session.commit()

    return jsonify({"Success": "Facebook Disconnected"})


@app.route('/get_fbuser_token', methods=['POST'])
def get_fbuser_token():
    data = json.loads(request.data)

    fb_info = FBUsers.query.join(Users).filter(Users.username == data['username']).first()

    res = { 'Success': 'Query Done' }

    if fb_info:
        res['facebook_name'] = fb_info.name
        res['facebook_id'] = fb_info.fbid

    return jsonify(res)


@app.route('/favorite', methods=['POST'])
def add_to_favorite():
    data = json.loads(request.data)

    images = data['images']
    username = data['username']
    email = data['email']

    user = Users.query.filter((Users.username == username) | (Users.email == email)).first()

    for image in images:
        image_object = get_image(db, Images, image)
        user.favorites.append(image_object)

    db.session.commit()

    return jsonify({"Success": True})


@app.route('/pinpage', methods=['POST'])
def add_to_pin():
    data = json.loads(request.data)

    pages = data['pages']
    username = data['username']
    email = data['email']

    user = Users.query.filter((Users.username == username) | (Users.email == email)).first()

    for page in pages:
        page_object = get_page(db, Pages, page)
        user.pages.append(page_object)

    db.session.commit()

    return jsonify({"Success": True})


@app.route('/get_favorites/<username>', methods=['GET'])
def get_favorites(username):
    images = Images.query.join(favorite_images).join(Users).filter(Users.username == username).all()
    
    images_dict = []

    for image in images:
        body = {}
        body['link'] = image.image_link
        body['thumbnail'] = image.thumbnail_link

        images_dict.append(body)

    return jsonify(images_dict);


@app.route('/get_pinpages/<username>', methods=['GET'])
def get_pinpages(username):
    pages = Pages.query.join(pinned_pages).join(Users).filter(Users.username == username).all()

    pages_dict = []

    for page in pages:
        body = {}

        body['name'] = page.name
        body['id'] = page.page_id
        body['cover'] = page.cover
        body['picture'] = page.picture

        pages_dict.append(body)

    return jsonify(pages_dict)


if __name__ == "__main__":
    manager.run()
