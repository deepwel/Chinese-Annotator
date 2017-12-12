import json
import uuid

from flask import Flask, request, redirect, url_for, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from utils.mongoUtil import get_mongo_client

UPLOAD_FOLDER = '../../data/files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


@app.route("/")
def hello():
    return "chinese annotatoer"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_remote_file', methods=['GET', 'POST'])
def upload_remote_file():
    """
    load data from file to mongodb, this is the main interface to load data
    :return:
    """
    print("test>>>>>")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print((file.filename))
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # save file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # read file
            ca = get_mongo_client(uri='mongodb://localhost:27017/')
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    txt = line.strip()
                    text_uuid = uuid.uuid1()
                    ca["annotation_data"].insert_one({"txt": txt, "uuid": text_uuid})
            return jsonify(data={"status": "success"}, code=200, message="load success")
    return jsonify(data={"status": "fail"}, code=302, message="the upload file is incorrect")


@app.route('/load_local_dataset', methods=['GET', 'POST'])
def load_local_dataset():
    """
    load local unlabeled dataset
    :return:
    """
    if request.method == 'POST':
        filepath = request.data.get("filepath")
    else:
        filepath = request.args.get("filepath")
    print(filepath)
    # read file
    ca = get_mongo_client(uri='mongodb://localhost:27017/')
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # label, txt = line.split(" ", 1)
            print("get string %s" % line)
            label, txt = line.split(" ", 1)
            ca["annotation_data"].insert_one({"txt": txt, "label": label})

    return jsonify(data={"status": "success"}, code=200, message="load success")


@app.route('/export_data', methods=['GET'])
def export_data():
    """

    :return:
    """
    filepath = request.args.get("filepath")

    # # read file
    ca = get_mongo_client(uri='mongodb://localhost:27017/')
    with open("../../data/files/test.json", "w") as f:
        # texts = list(ca["test"].find())
        # print(texts)
        # datas = [delattr(text, "_id") for text in texts if "_id" in text]

        annotations = ca["annotation_data"].find({}).batch_size(50)
        result = []
        for annotation in annotations:
            data = {
                "label": annotation["label"],
                "txt": annotation["txt"]
            }
            result.append(data)
        json.dump(result, f)

    return send_from_directory('../../data/files', "test.json")


@app.route('/load_single_unlabeled', methods=['GET', 'POST'])
def load_single_unlabeled():
    """
    load one unlabeled text from Mongo DB to web
    :return:
    """
    # read file
    ca = get_mongo_client(uri='mongodb://localhost:27017/')
    text = ca["annotation_data"].find_one({"label": {"$exists": False}})

    return jsonify(data={"text": text.get("txt"), "uuid": text.get("uuid")}, code=200, message="load success")
    # text = "贵公司负责人：你好！ 本公司(祥泰实业有限公司）具有良 好有的进口来源，有剩余的发票及广泛的网 络可为贵公司谋利获得双嬴，本公司原则是 满意付款。有诚意来电洽商。 电  话：013631690076 邮  箱：shitailong-9688@163.com 联系人：郭 生"
    # text_uuid = uuid.uuid1()
    # return jsonify(data={"text": text, "uuid": text_uuid}, code=200, message="load success")


@app.route('/annotate_single_unlabeled', methods=['POST'])
def annotate_single_unlabeled():
    """

    :return:
    """
    # read file
    text = request.form.get("text", "")
    label = request.form.get("label", "")
    print(text)
    print(label)
    ca = get_mongo_client()
    text = ca["annotation_data"].insert_one({"label": label, "text": text})

    return jsonify(data={}, code=200, message="annotate success")


@app.route('/check_offline_progress', methods=['POST'])
def check_offline_progress():
    """

    :return:
    """
    # read file
    text = request.form.get("text", "")
    label = request.form.get("label", "")
    print(text)
    print(label)
    ca = get_mongo_client()
    text = ca["annotation_data"].insert_one({"label": label, "text": text})

    return jsonify(data={"progress": 50}, code=200, message="annotate success")

if __name__=="__main__":
    app.run(
        host = '0.0.0.0',
        port = 5000,  
        debug = True 
    )