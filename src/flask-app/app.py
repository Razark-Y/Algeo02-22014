from flask import Flask,request,json,jsonify,url_for,session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from CBIRWarna import *
from CBIRTekstur import compareImage
from util import deleteFolderContent
from io import BytesIO
from scrapper import scrape_images
from multiprocessing import Pool
import os
import base64
from PIL import Image
import zipfile

app = Flask(__name__)
CORS(app,supports_credentials=True) 
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = "uploads"
app.config['DB_FOLDER'] = "../vue-app/src/assets/img"
# app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

@app.route('/uploadDB',methods=['POST'])
def uploadDB():
    folder = request.files.getlist('files')
    deleteFolderContent("../vue-app/src/assets/img")
    for file in folder:
        if file:
            filename = secure_filename(file.filename)
            filename = filename.replace(" ","_")
            filepath = os.path.join(app.config['DB_FOLDER'],filename)
            file.save(filepath)
    return jsonify("Congrats!")

@app.route('/uploadScrap',methods=['POST'])
def uploadScrap():
    url = request.json['string']
    print(url)
    deleteFolderContent("../vue-app/src/assets/img")
    scrape_images(url,"../vue-app/src/assets/img")
    return jsonify({'status': 'Succes'})

@app.route('/uploadColor',methods=['POST','GET'])
def cbir_color_list():
    data = []
    if 'image' in request.files:
        image = request.files['image']
        imageinput_result = create_histograms_for_segments(image)
        if image:
            filename = secure_filename(image.filename)
            for fileDB in os.listdir('../vue-app/src/assets/img') :
                # fileDBPath = '../vue-app/src/assets/img/'+fileDB
                imageDB_result = create_histograms_for_segments("../vue-app/src/assets/img/"+fileDB)
                dataObject = {
                    'imageTitle': fileDB,
                    'similarity': calculate_weighted_cosine_similarity(imageinput_result,imageDB_result)
                }
                data.append(dataObject)
    return jsonify(data)

@app.route('/uploadColorCamera',methods=['POST','GET'])
def cbir_color_list_camera():
    print("tes kamera")
    data = []
    # Get the image data from the request
    base64_string = request.json['file']

    base64_list = base64_string.split(',')
    # decoded_data = base64.urlsafe_b64decode(base64_string + '=' * (-len(base64_string) % 4))
    imgdata = base64.b64decode(base64_list[1])
    img = (BytesIO(imgdata))
    imageinput_result = create_histograms_for_segments(img)
    # # if image:
    # #     filename = secure_filename(image.filename)
    for fileDB in os.listdir('../vue-app/src/assets/img') :
        imageDB_result = create_histograms_for_segments("../vue-app/src/assets/img/"+fileDB)
        dataObject = {
            'imageTitle': fileDB,
            'similarity': calculate_weighted_cosine_similarity(imageinput_result,imageDB_result)
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
                }
                data.append(dataObject)
    return jsonify(data)

@app.route('/uploadTextureCamera',methods=['POST','GET'])
def cbir_texture_list_camera():
    data = []
    # Get the image data from the request
    base64_string = request.json['file']

    base64_list = base64_string.split(',')
    # decoded_data = base64.urlsafe_b64decode(base64_string + '=' * (-len(base64_string) % 4))
    imgdata = base64.b64decode(base64_list[1])
    img = Image.open(BytesIO(imgdata))
    img.save("uploads/gambarTemp.png")
    for fileDB in os.listdir('../vue-app/src/assets/img') :
        dataObject = {
            'imageTitle': fileDB,
            'similarity': float(compareImage("uploads/gambarTemp.png",'../vue-app/src/assets/img/'+fileDB)) * 100
        }
        data.append(dataObject)
    os.remove("uploads/gambarTemp.png")
    return jsonify(data)

app.run()