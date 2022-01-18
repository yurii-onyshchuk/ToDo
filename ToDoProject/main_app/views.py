from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, 'main_app/index.html')
