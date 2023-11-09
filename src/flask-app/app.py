from flask import Flask,request,json,jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from CBIRWarna import cbirColorCompare
import os

app = Flask(__name__)
CORS(app) 
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = "src/flask-app/uploads"

@app.route('/upload',methods=['POST'])
def get_images_list():
    data = []
    if 'image' in request.files:
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            image.save(filepath)
        for fileDB in os.listdir("src/vue-app/src/assets/img") :
            dataObject = {
                'imageTitle': fileDB,
                'similarity': cbirColorCompare(image,"src/vue-app/src/assets/img/"+fileDB)
            }
            data.append(dataObject)
    return jsonify(data)

app.run()