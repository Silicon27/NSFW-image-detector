import os
import base64
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from nsfw_detector import predict
from PIL import Image
import io

app = Flask(__name__)

# Load pre-trained model
model_path = '/path/to/nsfw_mobilenet2.224x224.h5'
model = predict.load_model(model_path)



UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST'])
def analyze_image():

    if 'file' not in request.files:
        return jsonify({'error': 'No file included in the request'}), 400

    base64_image = request.files['file'].read()
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'received_image.jpg')
    image.save(filepath)

    predictions = predict.classify(model, filepath)

    result = process_predictions(predictions)

    os.remove(filepath)

    return jsonify(result)

def process_predictions(predictions):
    print(predictions)
    # Convert probabilities to percentages and calculate total probability
    total_percentage = 0
    result = {}
    for image_name, probabilities in predictions.items():
        result[image_name] = {}
        for category, probability in probabilities.items():
            percentage = probability * 100
            result[image_name][category] = round(percentage, 2)
            total_percentage += probability

    # Check if total percentage exceeds 100% or contains non-neutral/drawing categories
    is_nsfw = False
    if total_percentage > 100:
        is_nsfw = True
    else:
        for image_name, probabilities in predictions.items():
            for category, probability in probabilities.items():
                if category not in ['neutral', 'drawings']:
                    is_nsfw = True
                    break
            if is_nsfw:
                break

    # Print NSFW status
    if is_nsfw:
        result['result'] = 'NSFW'
    else:
        result['result'] = 'Not NSFW'

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0')


