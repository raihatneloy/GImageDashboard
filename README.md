# GImage Dashboard



## Project Setup
The framework used in this project is Python-flask

Follow the steps for project installation:

* Install pip : `sudo apt-get install python-pip`

* Install python requirements: `pip install -r requirements.txt`



## Setting up database

The project expects a mysql server with a database with any name. You can give the database configuration in the file of `server/config/configuration.yaml`. 

The contains of database config should be like the followings:

```
db_config:
  host: <url of your mysql server to interact, default will be localhost>
  port: <port to connect to your mysql server, default will be 3306>
  database: <the name of database on which should we work>
  username: <the username which will be used to connect the mysql server>
  password: <password for the username>
```

There will be three tables in the database.
`users`, `images`, `favorite_images`

`users` contains all the information of an user. His/her username, name, email, password.

`images` contains images' url and thumbnail links that are selected to be saved by users.

`favorite_images`, this is an assosiative table that keeps the relation between user_id and image_id.

Now, you have to run the following commands to make this application communicate with the database:

```
cd server
python main.py db init
python main.py db migrate
python main.py db upgrade
```



## Configuration files
Server related configurations are stored in `server/config/configuration.yaml` and client related configuration are stored in `client/config/configuration.yaml`. You will have to overwrite these two files for making any changes in configurations.

## Running the app
### Run the server/backend:
Command: `python server/main.py runserver -h 0.0.0.0 -p 5000`

### Run the client/frontend:
Command: `python client/main.py runserver -h 0.0.0.0 -p 5001`