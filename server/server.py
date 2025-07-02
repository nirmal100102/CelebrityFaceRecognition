from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import util

app = Flask(__name__)
CORS(app)

@app.route('/classify_image', methods=['POST'])
def classify_image():
    image_data = request.form['image_data']
    print(">>> Received image data.")
    result = util.classify_image(image_data)
    print(">>> Classification result:", result)
    return jsonify(result)

if __name__ == "__main__":
    print("Starting Python Flask Server For Celebrity Classification")
    util.load_saved_artifacts()
    app.run(port=5000)
