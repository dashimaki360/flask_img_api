from flask import Flask, jsonify, render_template, request
import json
import process

app = Flask(__name__)
proc = process.processImg()


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
