import os
import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from werkzeug.utils import secure_filename

from apis.apiresponse import APIResponse
from apis.serializers import APIResponseSerializer
from utils.mongoUtil import get_mongo_client
import json


UPLOAD_FOLDER = '../../data/files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class AnnotationDataViewSet(APIView):
    pass


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_remote_file(request):
    """
    load data from file to mongodb, this is the main interface to load data
    :return:
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.FILES:
            # flash('No file part')
            return redirect(request.url)
        file = request.FILES['file']
        print((file.name))
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.name == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.name):
            # save file
            filename = secure_filename(file.name)
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            # read file
            ca = get_mongo_client(uri='mongodb://localhost:27017/')
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    txt = line.strip()
                    text_uuid = uuid.uuid1()
                    ca["annotation_data"].insert_one({"txt": txt, "uuid": text_uuid})
            response = APIResponse(data={"status": "success"}, code=200, message="load success")
            serializer = APIResponseSerializer(response)
            return JsonResponse(serializer.data)
    return JsonResponse(data={"status": "fail"}, code=302, message="the upload file is incorrect")


def export_data(request):
    """

    :return:
    """
    filepath = request.GET.get("filepath")
    response = APIResponse(data={"status": "success"}, code=200, message="load success")
    serializer = APIResponseSerializer(response)
    return JsonResponse(serializer.data)