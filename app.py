import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

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
            filename = secure_filename(img_file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img_file.save(img_path)
            img_url = '/uploads/' + filename
            base64.b64encode(img_file)

            out_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            out_url = '/outputs/' + filename
            proc.do(img_path, out_path)
            return render_template('index.html', img_url=img_url, out_url=out_url)
        else:
            return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('index'))


@app.route('/img_api', methods=['POST'])
def imgApi():
    # parse body json
    request.data
    in_img_base64 = 
    setting = 


    # call img process
    out_img_base64 = proc.do(in_img_base64, setting)

    # make response json
    response = {

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
