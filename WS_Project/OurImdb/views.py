from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"../templates/index.html", {})

def details(request):
    return render(request,"../templates/single.html", {})

def list(request):
    return render(request,"../templates/list.html", {})

def actors(request):
    return render(request,"../templates/actors.html", {})

def directors(request):
    return render(request,"../templates/directors.html", {})

def genres(request):
    return render(request,"../templates/genres_list.html", {})

def search(request):
    return render(request,"../templates/search.html", {})
