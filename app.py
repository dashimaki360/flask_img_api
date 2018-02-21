import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import base64
import json
import requests
import datetime

import process


app = Flask(__name__)
proc = process.processImg()

UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './outputs'
ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG', 'gif', 'GIF'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        img_file = request.files['img_file']
        if img_file and allowed_file(img_file.filename):
            # TODO add timestamp to filename
            now = datetime.datetime.now()
            timestamp = "{0:%Y%m%d-%H%M%S}_".format(now)
            filename = timestamp + secure_filename(img_file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img_url = '/uploads/' + filename
            in_img_base64 = base64.b64encode(img_file.stream.read()).decode('utf-8')
            img_file.save(img_path)

            request_dict = {
                "requests": [
                    {
                        "image": in_img_base64,
                        "features": [
                            {
                            }
                        ]
                    }
                ]
            }
            print(request_dict)

            res = requests.post(
                'http://127.0.0.1:5000/img_api',
                json.dumps(request_dict),
                headers={'Content-Type': 'application/json'}
                )
            res = json.loads(res)
            print(res)
            out_img = base64.b64decode(res['image'].encode())
            out_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            out_url = '/outputs/' + filename
            out_img.save(out_path)
            return render_template('index.html', img_url=img_url, out_url=out_url)
        else:
            return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('index'))


@app.route('/img_api', methods=['POST'])
def imgApi():
    # parse body json
    data = json.loads(request.data)
    print(data)
    req = data["requests"][0]
    in_img_base64 = req['image']
    setting = req['featues'][0]

    # call img process
    # out_img_base64, result = proc.do(in_img_base64, setting)
    out_img_base64 = in_img_base64
    result = {}

    # make response json
    response = {
        "image": out_img_base64,
        "result": result
    }

    # return
    return jsonify(response)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/outputs/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    app.debug = True
    app.run()
