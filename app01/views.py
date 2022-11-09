from django.shortcuts import render


# Create your views here.
def get_index(request):
    return render(request, "index.html")


def news(request):
    return render(request, "news.html")


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")
