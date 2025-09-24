from django.shortcuts import render

# Create your views here.

def startgame(request, *args, **kwargs):
    return render(request, 'index.html')