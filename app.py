# imports
import numpy as np
from flask import Flask, request, render_template, redirect
import os
import ImageHandler
import cv2
import pickle
import base64

os.environ['THEANO_FLAGS'] = 'optimizer=None'
app = Flask(__name__)

model = None

MODEL_PATH = "./models/model.p"
UPLOAD_FOLDER = './static/img'
filename = "single_file.png"

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# The code above will limit the maximum allowed payload to 16 megabytes. 
# If a larger file is transmitted, Flask will raise a RequestEntityTooLarge exception.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

def load_model():
    global model
    model = pickle.load(open(MODEL_PATH, 'rb'))


def convert_and_save(b64_string):
    io = StringIO()
    with open(io, "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))
    return io

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
    # predict using model (within tf graph namespace?)
    # with graph.as_default():
    #     result = model.predict_classes(ih.images)
    result = model.predict_classes(ih.images)
    
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
    load_model()
    app.run()