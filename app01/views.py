from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def get_index(request):
    return render(request, "index.html")


def news(request):
    return render(request, "news.html")


def login(request):
    if request.method == 'POST':
        data = request.data
        return JsonResponse(data)
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")
