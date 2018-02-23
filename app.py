from flask import Flask, jsonify, render_template, request
import json

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


@app.route('/img_api', methods=['POST'])
def imgApi():
    # parse body json
    data = json.loads(request.data)
    req = data["requests"][0]
    in_img_base64 = req['image']['content']
    setting = req['features'][0]

    # call img process
    out_img_base64, result = proc.do(in_img_base64, setting)

    # make response json
    response = {
        "image": out_img_base64,
        "result": result
    }

    # return
    return jsonify(response)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
