from flask import Flask,request,jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from io import BytesIO
import os
import base64
from PIL import Image

# Import library buatan
from util import deleteFolderContent
from CBIRTekstur import compareImage
from CBIRWarna import *
from scrapper import scrape_images

# Flask Setup
app = Flask(__name__)
CORS(app,supports_credentials=True) 
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = "uploads"
# app.config['DB_FOLDER'] = "../vue-app/src/assets/img"
app.config['DB_FOLDER'] = "database"

# Router for Database Upload
@app.route('/uploadDB',methods=['POST'])
def uploadDB():
    folder = request.files.getlist('files')
    deleteFolderContent("database")
    for file in folder:
        if file:
            filename = secure_filename(file.filename)
            filename = filename.replace(" ","_")
            filepath = os.path.join(app.config['DB_FOLDER'],filename)
            file.save(filepath)
    return jsonify({'status': 'Succes'})

# Router for Scrapper
@app.route('/uploadScrap',methods=['POST'])
def uploadScrap():
    url = request.json['string']
    print(url)
    deleteFolderContent("database")
    scrape_images(url,"database")
    return jsonify({'status': 'Succes'})

# Router for CBIR - Colour
@app.route('/uploadColor',methods=['POST','GET'])
def cbir_color_list():
    data = []
    if 'image' in request.files:
        image = request.files['image']
        imageinput_result = create_histograms_for_segments(image)
        if image:
            filename = secure_filename(image.filename)
            for fileDB in os.listdir('database') :
                imageDB_result = createHistogram("cache.json","database/"+fileDB)
                with open("database/"+fileDB, 'rb') as f:
                    image_data = f.read()
                    base64_data = base64.b64encode(image_data).decode('utf-8')
                    dataObject = {
                        'imageTitle': base64_data,
                        'similarity': calculate_weighted_cosine_similarity(imageinput_result,imageDB_result)
                    }
                    data.append(dataObject)
    return jsonify(data)

# Router for CBIR - Colour with Camera Feed
@app.route('/uploadColorCamera',methods=['POST','GET'])
def cbir_color_list_camera():
    print("tes kamera")
    data = []
    base64_string = request.json['file']
    base64_list = base64_string.split(',')
    imgdata = base64.b64decode(base64_list[1])
    img = (BytesIO(imgdata))
    imageinput_result = create_histograms_for_segments(img)
    for fileDB in os.listdir('database') :
        imageDB_result = createHistogram("cache.json","database/"+fileDB)
        dataObject = {
            'imageTitle': fileDB,
            'similarity': calculate_weighted_cosine_similarity(imageinput_result,imageDB_result)
        }
        data.append(dataObject)
    return jsonify(data)

# Router for CBIR - Texture
@app.route('/uploadTexture',methods=['POST','GET'])
def cbir_texture_list():
    data = []
    if 'image' in request.files:
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            image.save(filepath)
            for fileDB in os.listdir('database') :
                dataObject = {
                    'imageTitle': fileDB,
                    'similarity': float(compareImage(filepath,'database/'+fileDB)) * 100
                }
                data.append(dataObject)
    return jsonify(data)

# Router for CBIR - Texture with Camera Feed
@app.route('/uploadTextureCamera',methods=['POST','GET'])
def cbir_texture_list_camera():
    data = []
    base64_string = request.json['file']
    base64_list = base64_string.split(',')
    imgdata = base64.b64decode(base64_list[1])
    img = Image.open(BytesIO(imgdata))
    img.save("uploads/gambarTemp.png")
    for fileDB in os.listdir('database') :
        dataObject = {
            'imageTitle': fileDB,
            'similarity': float(compareImage("uploads/gambarTemp.png",'database/'+fileDB)) * 100
        }
        data.append(dataObject)
    os.remove("uploads/gambarTemp.png")
    return jsonify(data)

# Menjalankan aplikasi flask
app.run()