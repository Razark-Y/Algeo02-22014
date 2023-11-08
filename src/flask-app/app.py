from flask import Flask,request,json
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/',methods=['GET'])
def get_images_list():
    data = []
    for filename in os.listdir("src/vue-app/src/assets/img") :
        dataObject = {
            'imageTitle': filename
        }
        data.append(dataObject)
    return json.dumps(data)

app.run()