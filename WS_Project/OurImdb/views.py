from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"../templates/index.html", {})

def details(request):
    return render(request,"../templates/single.html", {})

def list(request):
    return render(request,"../templates/list.html", {})
