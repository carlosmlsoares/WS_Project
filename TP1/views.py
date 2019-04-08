from django.shortcuts import render
from TP1.db import sparql


# Create your views here.
def index(request):
    return render(request, "index.html", {
        'genres': get_genres()
    })


def movies(request):
    return render(request, "movies.html", {})


def movie(request, id):
    return render(request, "movie.html", {'id': id})


def actors(request):
    return render(request, "actors.html", {})


def actor(request, id):
    return render(request, "actor.html", {'id': id})


def directors(request):
    return render(request, "directors.html", {})


def director(request, id):
    return render(request, "director.html", {'id': id})


def genre(request, id):
    return render(request, "genre.html", {'id': id})


def search(request):
    return render(request, "search.html", {})


def get_genres():
    return sparql("""
        SELECT ?id ?name
        WHERE { 
            ?id genre:name ?name.
            ?movie movie:genre ?id.
        }
        GROUP BY ?id ?name
        ORDER BY DESC(COUNT(?movie))
    """)
