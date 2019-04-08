from django.shortcuts import render
from TP1.db import sparql


def index(request):
    return render(request, "index.html", {
        'genres': get_genres(),
        'new': get_new_movies(),
        'trending': get_trending_movies()
    })


def movies(request):
    return render(request, "movies.html", {
        'genres': get_genres(),
        'movies': get_all_movies()
    })


def movie(request, id):
    return render(request, "movie.html", {
        'id': id,
        'genres': get_genres()
    })


def actors(request):
    return render(request, "actors.html", {
        'genres': get_genres()
    })


def actor(request, id):
    return render(request, "actor.html", {
        'id': id,
        'name': get_worker_name(id),
        'content': get_actor_movies(id)
    })


def directors(request):
    return render(request, "directors.html", {
        'genres': get_genres()
    })


def director(request, id):
    return render(request, "director.html", {
        'id': id,
        'name': get_worker_name(id),
        'content': get_director_movies(id)
    })


def genre(request, id):
    return render(request, "genre.html", {
        'id': id,
        'genres': get_genres()
    })


def search(request):
    term = request.GET['term'] if 'term' in request.GET else 'John Doe'

    return render(request, "search.html", {
        'genres': get_genres(),
        'term': term,
        'directors': search_directors(term),
        'movies': search_movies(term),
        'actors': search_actors(term)
    })


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


def get_new_movies():
    return sparql("""
        SELECT *
        WHERE { 
            ?id movie:title ?title.
            ?id movie:year ?year.
            ?id movie:score ?score.
        }
        ORDER BY DESC(?year) DESC(?score)
        LIMIT 6
    """)


def get_trending_movies():
    return sparql("""
        SELECT *
        WHERE { 
            ?id movie:title ?title.
            ?id movie:year ?year.
            OPTIONAL{
                ?id movie:score ?score.
            }
        }
        ORDER BY DESC(?year) DESC(?views)
        LIMIT 6
    """)


def get_all_movies():
    return sparql("""
        SELECT *
        WHERE { 
            ?id movie:title ?title.
            ?id movie:year ?year.
            ?id movie:score ?score.
        }
        ORDER BY DESC(?year) DESC(?score)
        LIMIT 40
    """)


def get_worker_name(id):
    worker = sparql("""
        SELECT ?name
        WHERE {
            worker:""" + id + """ worker:name ?name.
            }
        LIMIT 1
    """)

    return worker[0]['name'] if worker and 'name' in worker[0] else None


def get_actor_movies(id):
    return sparql("""
        SELECT ?movie ?title ?year ?score
        WHERE {
            worker:""" + id + """ worker:played_on ?movie .
            ?movie movie:title ?title.
            ?movie movie:year ?year.
            ?movie movie:score ?score.
        
        }
    """)


def get_director_movies(id):
    return sparql("""
        SELECT ?movie ?title ?year ?score
        WHERE {
            worker:""" + id + """ worker:directed ?movie .
            ?movie movie:title ?title.
            ?movie movie:year ?year.
            ?movie movie:score ?score.
        }
    """)


def search_movies(term):
    return sparql("""
        SELECT ?id ?title ?year ?score
        WHERE {
            ?id movie:title ?title.
            ?id movie:year ?year.
            ?id movie:score ?score.
            FILTER (CONTAINS(LCASE(?title), LCASE("TERM")))
        }
    """.replace("TERM", term))


def search_directors(term):
    return sparql("""
        SELECT ?id ?name (COUNT(?movie) AS ?movies)
        WHERE {
            ?id worker:directed ?movie.
            ?id worker:name ?name.
            FILTER (CONTAINS(LCASE(?name), LCASE("TERM")))
        }
        GROUP BY ?id ?name
        ORDER BY DESC (?movies)
    """.replace("TERM", term))


def search_actors(term):
    return sparql("""
        SELECT ?id ?name (COUNT(?movie) AS ?movies)
        WHERE {
            ?id worker:played_on ?movie.
            ?id worker:name ?name.
            FILTER (CONTAINS(LCASE(?name), LCASE("TERM")))
        }
        GROUP BY ?id ?name
        ORDER BY DESC (?movies)
    """.replace("TERM", term))
