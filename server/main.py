from flask import Flask, jsonify, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from modules import get_images_url as gsearch
from models.users import users_model as users
from models.users import add_new_user as new_user
from models.images import images_model as images
from models.images import get_image
import json
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
	OAUTH1_PROVIDER_ENFORCE_SSL=False
)

# Initialize db
db = SQLAlchemy(app)
Users, favorite_images = users(db)
Images = images(db)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/images/<query>', methods=['GET'])
def get_images(query):
	query = query.replace('%20', ' ')
	image_links = gsearch.get_images(query)

	return jsonify(image_links)


@app.route('/register/new_user', methods=['POST'])
def register_new_user():
	data = json.loads(request.data)

	ret = new_user(db, Users, data)

	return jsonify(ret)


@app.route('/authentication', methods=['POST'])
def authenticate_user():
    data = json.loads(request.data)

    identity = data.get('identity')
    password = data.get('password')

    user = Users.query.filter((Users.username == identity) | (Users.email == identity)).first()

    if user is None:
        return jsonify({"Error": "Invalid username/email"})

    if user.password != password:
        return jsonify({"Error": "Password mismatch"})

    return jsonify({
        "Success": "Login successful",
        "username": user.username,
        "name": user.name,
        "email": user.email
    })


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

if __name__ == "__main__":
	manager.run()
