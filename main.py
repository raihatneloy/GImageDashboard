from flask import Flask, jsonify
from modules import get_images_url as gsearch
import os

app = Flask(__name__)
app.config.update(
	DEBUG=True
)


@app.route('/images/<query>', methods=['GET'])
def get_images(query):
	query = query.replace('%20', ' ')
	image_links = gsearch.get_images(query)

	return jsonify(image_links)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)