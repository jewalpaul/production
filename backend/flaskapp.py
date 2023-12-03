import logging
from flask import Flask, request, send_file
from flask import make_response
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import os
logging.basicConfig(filename='app.log', level=logging.INFO)
app = Flask(__name__)
CORS(app)
@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        file = request.files['file']
        format = request.form.get('format', 'PNG')
        img = Image.open(file.stream)
        R = remove(img)
        output_image = Image.new('RGBA', R.size, (255, 255, 255, 255))
        output_image.paste(R, (0, 0), R)
        byte_arr = io.BytesIO()
        output_image.save(byte_arr, format=format)
        byte_arr.seek(0)
        return send_file(byte_arr, mimetype='image/' + format.lower())
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return {'error': str(e)}, 400
@app.route('/resize-image', methods=['POST'])
def resize_image():
    try:
        file = request.files['file']
        width = request.form.get('width')
        height = request.form.get('height')
        format = request.form.get('format', 'PNG')
        img = Image.open(file.stream)
        resized_image = img.resize((int(width), int(height)))
        byte_arr = io.BytesIO()
        resized_image.save(byte_arr, format=format)
        byte_arr.seek(0)
        return send_file(byte_arr, mimetype='image/' + format.lower())
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return {'error': str(e)}, 400
if __name__ == '__main__':
    app.run(debug=True, port=81)