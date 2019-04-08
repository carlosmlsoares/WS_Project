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
        'movies': get_all_movies()
    })


def movie(request, id):
    return render(request, "movie.html", {'id': id})


def actors(request):
    return render(request, "actors.html", {})


def actor(request, id):
    query = """SELECT ?name
                    WHERE {
                        worker:""" + id + """ worker:name ?name.
                        }
                    LIMIT 1
                    """

    name = sparql(query)[0]['name']

    query = """SELECT ?movie ?title ?year ?score
            WHERE {
                worker:""" + id + """ worker:played_on ?movie .
                ?movie movie:title ?title.
                ?movie movie:year ?year.
                ?movie movie:score ?score.

            }"""

    content = sparql(query)

    return render(request, "actor.html", {'id': id, 'name': name, 'content': content})

def directors(request):
    return render(request, "directors.html", {})


def director(request, id):
    query = """SELECT ?name
                WHERE {
                    worker:"""+id+""" worker:name ?name.
                    }
                LIMIT 1
                """

    name = sparql(query)[0]['name']

    query="""SELECT ?movie ?title ?year ?score
        WHERE {
            worker:""" +id+""" worker:directed ?movie .
            ?movie movie:title ?title.
            ?movie movie:year ?year.
            ?movie movie:score ?score.
            
        }"""

    content = sparql(query)


    return render(request, "director.html", {'id': id,'name':name,'content':content})


def genre(request, id):
    return render(request, "genre.html", {'id': id})


def search(request):

    term=request.GET['term']


    query="""SELECT ?id ?title ?year ?score
        WHERE {
            ?id movie:title ?title.
            ?id movie:year ?year.
            ?id movie:score ?score.
            FILTER (CONTAINS(LCASE(?title), "TERM"))
        }
        GROUP BY ?id ?title 
        LIMIT 20""".replace("TERM", term)

    movies=sparql(query)
    print(movies)


    query="""SELECT ?id ?name (COUNT(?movie) AS ?movies)
        WHERE {
            ?id worker:directed ?movie.
            ?id worker:name ?name.
            FILTER (CONTAINS(LCASE(?name), "TERM"))
        }
        GROUP BY ?id ?name
        ORDER BY DESC (?movies)
        LIMIT 20 """.replace("TERM", term)

    directors = sparql(query)
    print(directors)


    query = """SELECT ?id ?name (COUNT(?movie) AS ?movies)
            WHERE {
                ?id worker:played_on ?movie.
                ?id worker:name ?name.
                FILTER (CONTAINS(LCASE(?name), "TERM"))
            }
            GROUP BY ?id ?name
            ORDER BY DESC (?movies)
            LIMIT 20 """.replace("TERM", term)

    actors = sparql(query)
    print(actors)

    return render(request, "search.html", {'term':term,'directors':directors,'movies':movies,'actors':actors})


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

