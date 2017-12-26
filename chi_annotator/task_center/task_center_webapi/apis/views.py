from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def test_connect(request):
    """
    test if connect is OK
    :param request:
    :return:
    """
    return JsonResponse(data={"training_process": 50, "code":200, "message":"annotate success"})