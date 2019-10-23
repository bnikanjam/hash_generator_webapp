import hashlib

from django.shortcuts import render, redirect
from django.http import JsonResponse

from .forms import HashForm
from .models import Hash


def home_view(request):
    template = 'hash/home.html'
    context = {}

    if request.method == 'POST':
        filled_form = HashForm(request.POST)
        if filled_form.is_valid():
            text = filled_form.cleaned_data['text']
            sha256 = hashlib.sha256(text.encode('utf-8')).hexdigest()

            try:
                Hash.objects.get(sha256=sha256)
                return redirect(hash_url, sha256)

            except Hash.DoesNotExist:
                new_record = Hash()
                new_record.text = text
                new_record.sha256 = sha256
                new_record.save()
                context = {
                    'text': text,
                    # 'sha256': sha256
                }
                # return render(request, template_name=template, context=context)
                return redirect(hash_url, new_record.sha256)

    # elif request.method == 'GET':

    form = HashForm()
    context = {'form': form}
    return render(request, template_name=template, context=context)


def hash_url(request, sha256):
    template = 'hash/hashpage.html'
    row = Hash.objects.get(sha256=sha256)
    context = {
        'text': row.text,
        'sha256': row.sha256
    }
    return render(request, template_name=template, context=context)


def quickhash(request):
    text = request.GET['text']
    print('--->\t',text)
    sha256 = hashlib.sha256(text.encode('utf-8')).hexdigest()

    data = {
        # 'text': text,
        'sha256': sha256,
    }
    return JsonResponse(data)
