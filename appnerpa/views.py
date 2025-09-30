from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def one_c_handler(request):
    return HttpResponse("Request handled successfully.")

def index(request):
    return render(request, 'index.html')