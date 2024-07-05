
from loguru import logger
from rest_framework import decorators, response, status

from core.gemini_helper import call_gemini, predict_image_using_gemini

import os
import time
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from .forms import UploadFileForm


@decorators.api_view(['GET'])
# @timeit("endpoints.ttfb.autocomplete_message")
def process_message(request):
    try:
        message = request.query_params['query']
        logger.debug("Asked Question: ", message)

        query_result = call_gemini(message)
        
        return response.Response({
            'response': query_result
        })
    except Exception as e:
        logger.error(e)
        return response.Response(
                {
                    'status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : e,
                    'exception_class' : e.__class__.__name__,
                    'exception_message' : e.args[0]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

@decorators.api_view(['POST'])
# @timeit("endpoints.ttfb.autocomplete_message")
def predict_image(request):
    try:
        # message = request.query_params['query']
        # logger.debug("Asked Question: ", message)
        
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            print(f"File uploaded successfully. File path: {file_path}")
    
        query_result = predict_image_using_gemini(file_path)
        
        return response.Response(
            query_result
        )
    except Exception as e:
        logger.error(e)
        return response.Response(
                {
                    'status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : e,
                    'exception_class' : e.__class__.__name__,
                    'exception_message' : e.args[0]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def handle_uploaded_file(f):
    timestamp = int(time.time())
    filename = f"{timestamp}_{f.name}"
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    print("**Upload File Path:**",file_path)
    print("**Upload File Name:**",filename)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    print(f"Absolute file path: {file_path}")
    return file_path

