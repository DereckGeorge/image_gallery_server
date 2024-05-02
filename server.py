from flask import Flask, jsonify, send_from_directory
from flask_restful import Api, Resource
import os

app = Flask(__name__)
api = Api(app)

# Allow requests from all origins
from flask_cors import CORS
CORS(app)

# Serve static files from the 'images' folder
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(app.root_path, 'images'), filename)

# Route to fetch images from categories
class GalleryData(Resource):
    def get(self):
        images_folder = os.path.join(app.root_path, 'images')
        try:
            categories = os.listdir(images_folder)
            categories_with_images = []
            for category in categories:
                category_path = os.path.join(images_folder, category)
                images_in_category = [{'name': image, 'path': f'/images/{category}/{image}'} for image in os.listdir(category_path)]
                categories_with_images.append({'name': category, 'images': images_in_category})
            return jsonify(categories_with_images)
        except Exception as e:
            print('Error reading images directory:', e)
            return jsonify({'error': 'Internal Server Error'}), 500

api.add_resource(GalleryData, '/gallery_data')

if __name__ == '__main__':
    app.run(port=3002)
