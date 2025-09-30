from django.shortcuts import render
from django.http import HttpResponse

def one_c_handler(request):
    return HttpResponse("Request handled successfully.")

def index(request):
    return render(request, 'index.html')