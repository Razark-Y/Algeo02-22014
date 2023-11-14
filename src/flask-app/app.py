from flask import Flask,request,json,jsonify,url_for,session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from CBIRWarna import cbirColorCompare
from CBIRTekstur import compareImage
import os

app = Flask(__name__)
CORS(app,supports_credentials=True) 
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = "uploads"

@app.route('/uploadDB',methods=['POST'])
def uploadDB():
    if 'imageDB' in request.files:
        image = request.files['imageDB']
        if image:
            filename = secure_filename(image.filename)
            filename.replace(" ","_")
            filepath = os.path.join("../vue-app/src/assets/img",filename)
            image.save(filepath)
    return jsonify("upload berhasil!")

@app.route('/uploadColor',methods=['POST','GET'])
def cbir_color_list():
    data = []
    if 'image' in request.files:
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            # filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            # image.save(filepath)
            for fileDB in os.listdir('../vue-app/src/assets/img') :
                dataObject = {
                    'imageTitle': fileDB,
                    'similarity': cbirColorCompare(image,'../vue-app/src/assets/img/'+fileDB)
                    # 'similarity': cbirColorCompare("src/flask-app/bandara.jpeg",fileDB)
                }
                data.append(dataObject)
    return jsonify(data)

@app.route('/uploadTexture',methods=['POST','GET'])
def cbir_texture_list():
    data = []
    if 'image' in request.files:
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            image.save(filepath)
            for fileDB in os.listdir('../vue-app/src/assets/img') :
                dataObject = {
                    'imageTitle': fileDB,
                    'similarity': float(compareImage(filepath,'../vue-app/src/assets/img/'+fileDB)) * 100
                    # 'similarity': cbirColorCompare("src/flask-app/bandara.jpeg",fileDB)
                }
                data.append(dataObject)
    return jsonify(data)

app.run()