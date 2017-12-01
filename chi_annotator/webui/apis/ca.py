import json

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
            # print(file.read())

            # save file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # read file
            ca = get_mongo_client(uri='mongodb://localhost:27017/')
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    label, txt = line.split(" ", 1)
                    ca["test"].insert_one({"txt": txt, "label": label})
            return jsonify(data={"status": "success"}, code=200, message="load success")
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


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
            ca["test"].insert_one({"txt": txt, "label": label})

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

        annotations = ca["test"].find({}).batch_size(50)
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

    :return:
    """
    # read file
    ca = get_mongo_client()
    text = ca["test"].find_one({"label": {"$exists": False}})

    return jsonify(data={"text": text.get("txt")}, code=200, message="load success")


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
    text = ca["test"].insert_one({"label": label, "text": text})

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
    text = ca["test"].insert_one({"label": label, "text": text})

    return jsonify(data={"progress": 50}, code=200, message="annotate success")

if __name__=="__main__":
    app.run(
        host = '0.0.0.0',
        port = 5000,  
        debug = True 
    )