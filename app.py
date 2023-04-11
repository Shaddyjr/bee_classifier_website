# imports
import numpy as np
from flask import Flask, request, render_template, redirect
import os
import ImageHandler
import cv2 # opencv-python
import base64
from tensorflow.keras.models import load_model

os.environ['THEANO_FLAGS'] = 'optimizer=None'
app = Flask(__name__)

model = None

MODEL_PATH = "./models/best_original.h5"
UPLOAD_FOLDER = './static/img'
filename = "single_file.png"

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# The code above will limit the maximum allowed payload to 16 megabytes. 
# If a larger file is transmitted, Flask will raise a RequestEntityTooLarge exception.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def form():
    return render_template("form.html")

@app.route('/submit', methods = ["POST"])
def submit():
    if 'file' not in request.files:
        return redirect("/")
    file = request.files['file']

    if file.filename == '':
        return redirect("/")

    ### HANDLING MODEL PREDICTION ###    
    file.seek(0)
    #read image file string data
    filestr = file.read()
    #convert string data to numpy array
    npimg = np.fromstring(filestr, np.uint8)
    # convert numpy array to image
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    # resize and normalize data for modeling
    ih = ImageHandler.ImageHandler([img]).resize((54,50)).normalize()
    # predict using model
    model = load_model(MODEL_PATH, compile=False)
    result = model.predict(ih.images)
    
    ### HANDLING IMAGE VISUALIZATION ###
    file.seek(0)
    file.save(file_path)
    with open(file_path, "rb") as imageFile:
        image_data = base64.b64encode(imageFile.read())

    return render_template(
        "results.html", 
        result = result[0][0],
        image_data = image_data.decode()
        )

if __name__ == '__main__':
    port = os.environ.get("PORT", 5000) # Heroku will set the PORT environment variable for web traffic
    app.run(debug = False, host='0.0.0.0', port = port)