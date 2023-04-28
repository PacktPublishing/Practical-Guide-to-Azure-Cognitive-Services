import base64
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .cognitive_vision import poll
from .models import Results


@login_required
def index(request):
    results = Results.objects.all()

    context = {
        'results': results
    }
    return render(request, 'cognitive_vision/index.html', context)


@login_required
def check(request):
    if request.htmx:
        messages = poll()
        for msg in messages:
            try:
                decoded_bytes = json.loads(json.loads(str(base64.b64decode(msg['content']), "utf-8")))
            except KeyError:
                decoded_bytes = msg
            new_result = Results(
                file_name=decoded_bytes['file_name'],
                good=decoded_bytes['Good tail'],
                bad=decoded_bytes['Bad tail'])
            new_result.passed = True if float(new_result.good) > float(new_result.bad) else False
            new_result.save()

    results = Results.objects.all()

    context = {
        'results': results
    }
    return render(request, 'cognitive_vision/_results.html', context)


@login_required
@csrf_exempt
def reclassify(request, result_id):
    result = Results.objects.get(id__exact=result_id)
    good = result.good
    bad = result.bad
    if result.passed:
        result.good = bad
    else:
        result.bad = good
    result.save()
    return index
