import base64
import os
import re
from binascii import Error

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .cognitive_search import search_index, view_result


@login_required
def index(request):
    return render(request, 'cognitive_search/index.html', {})


@login_required
def search(request):
    if request.htmx:
        if not str(request.POST['query']) == "":
            results = search_index(str(request.POST['query']))
            context = {
                'results': results
            }
            return render(request, 'cognitive_search/_results.html', context)
        return render(request, 'cognitive_search/_results.html', {})


@login_required
def view(request, key_id=None):
    result = view_result(key_id)
    relevant_results = list()
    padding = '===='
    remainder = len(result['metadata_storage_path']) % 4
    try:
        storage_path = str(base64.urlsafe_b64decode(f"{result['metadata_storage_path']}{padding[-remainder]}"), "UTF-8")
    except Error:
        storage_path = str(base64.urlsafe_b64decode(f"{result['metadata_storage_path'][:-1]}{padding[-remainder]}"), "UTF-8")
    result['extension'] = str(result['metadata_storage_name'][-3:]).lower()
    result['storage_path'] = f"{storage_path}?{os.getenv('AZURE_COG_SEARCH_BUCKET_TOKEN')}"

    storage_paths = list()
    for keyword in result['people']:
        result_list = search_index(re.sub('[^A-Za-z0-9]+', '', str(keyword)))
        for temp_result in result_list:
            if temp_result['metadata_storage_path'] not in storage_paths:
                relevant_results.append(temp_result)
                storage_paths.append(temp_result['metadata_storage_path'])

    return render(request, 'cognitive_search/view.html', {
        'result': result,
        'relevant_results': relevant_results
    })
