from flask import Flask,request,jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from io import BytesIO
import os
import base64
from PIL import Image

# Import library buatan
from util import deleteFolderContent
from CBIRTekstur import *
from CBIRWarna import *
from scrapper import scrape_images
from convertPDF import *

# Flask Setup
app = Flask(__name__)
CORS(app,supports_credentials=True) 
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = "uploads"
# app.config['DB_FOLDER'] = "../vue-app/src/assets/img"
app.config['DB_FOLDER'] = "database"

@app.route('/convertpdf',methods=['POST'])
def pdfconverter():
    clear_json("data.json")
    data = request.json['data']
    with open('data.json', 'w') as f:
        json.dump(data, f)
    toPDF("data.json")
    return jsonify({'status':'succes'})


# Router for Database Upload
@app.route('/uploadDB',methods=['POST'])
def uploadDB():
    deleteFolderContent("database")
    folder = request.files.getlist('files')
    for file in folder:
        if file:
            filename = secure_filename(file.filename)
            filename = filename.replace(" ","_")
            filepath = os.path.join(app.config['DB_FOLDER'],filename)
            file.save(filepath)
    createHistogram("database","cache.json")
    processDataset("database")
    return jsonify({'status': 'Succes'})

# Router for Scrapper
@app.route('/uploadScrap',methods=['POST'])
def uploadScrap():
    url = request.json['string']
    deleteFolderContent("database")
    scrape_images(url,"database")
    createHistogram("database","cache.json")
    processDataset("database")
    return jsonify({'status': 'Succes'})

# Router for CBIR - Colour
@app.route('/uploadColor',methods=['POST','GET'])
def cbir_color_list():
    data = []
    if 'image' in request.files:
        image = request.files['image']
        imageinput_result = create_histograms_for_segments(image)
        arrdata = caching("cache.json",imageinput_result)
        for (filename,similarity) in arrdata :
            with open(filename.replace("\\","/"), 'rb') as f:
                image_data = f.read()
                base64_data = base64.b64encode(image_data).decode('utf-8')
                dataObject = {
                    'imageTitle': base64_data,
                    'similarity': similarity
                }
                data.append(dataObject)
    return jsonify(data)

# Router for CBIR - Colour with Camera Feed
@app.route('/uploadColorCamera',methods=['POST','GET'])
def cbir_color_list_camera():
    data = []
    base64_string = request.json['file']
    base64_list = base64_string.split(',')
    imgdata = base64.b64decode(base64_list[1])
    img = (BytesIO(imgdata))
    imageinput_result = create_histograms_for_segments(img)
    arrdata = caching("cache.json",imageinput_result)
    for (filename,similarity) in arrdata :
        with open(filename.replace("\\","/"), 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            dataObject = {
                'imageTitle': base64_data,
                'similarity': similarity
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
            arrData = compareImageWithDataset(filepath.replace("\\","/"))
            print(arrData)
            for (similarity,name) in arrData :
                with open("database/"+name,'rb') as f:
                    image_data = f.read()
                    base64_data = base64.b64encode(image_data).decode('utf-8')
                    dataObject = {
                        'imageTitle': base64_data,
                        'similarity': float(similarity) * 100
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
    arrData = compareImageWithDataset("uploads/gambarTemp.png")
    print(arrData)
    for (similarity,name) in arrData :
        with open("database/"+name,'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            dataObject = {
                'imageTitle': base64_data,
                'similarity': float(similarity) * 100
            }
            data.append(dataObject)
    os.remove("uploads/gambarTemp.png")
    return jsonify(data)

# Menjalankan aplikasi flask
app.run()