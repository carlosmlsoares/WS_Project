from django.shortcuts import render
from TP1.db import sparql
from TP1.wikidata import wikisparql


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
        'genres': get_genres(),
        'movie': get_movie_details(id),
        'actors': get_movie_actors(id),
        'movie_genres': get_movie_genres(id),
        'awards':get_movie_awards(id),
        'nomeations': get_movie_nomeations(id),
        'companies': get_movie_companies(id)
    })


def actors(request):
    return render(request, "actors.html", {
        'genres': get_genres(),
        'actors': get_all_actors()
    })


def actor(request, id):
    return render(request, "actor.html", {
        'id': id,
        'genres': get_genres(),
        'name': get_worker_name(id),
        'content': get_actor_movies(id),
        'worked_with': get_worked_with(id)
    })


def directors(request):
    return render(request, "directors.html", {
        'genres': get_genres(),
        'directors': get_all_directors()
    })


def director(request, id):
    return render(request, "director.html", {
        'id': id,
        'name': get_worker_name(id),
        'content': get_director_movies(id),
        'genres':get_genres()
    })


def genre(request, id):
    return render(request, "genre.html", {
        'id': id,
        'genres': get_genres(),
        'movies': movies_by_genre(id)
    })


def inferences(request):
    return render(request, "inferences.html", {
        'genres': get_genres()
    })


def exec_inferences(request, id):
    if id == '00':
        sparql("""
                INSERT {
                    ?next movie:isNew true
                }
                WHERE { 
                    {
                        ?old movie:isNew true
                    } UNION { 
                        SELECT ?next
                        WHERE {
                            ?next movie:year ?year.
                            ?next movie:score ?score.
                        }
                        ORDER BY DESC(?year) DESC(?score)
                        LIMIT 6
                    }
                }
            """)
    elif id == '01':
        sparql("""
                INSERT {
                    ?next movie:isTrending true
                }
                WHERE { 
                    {
                        ?old movie:isTrending true
                    } UNION { 
                        SELECT ?next
                        WHERE {
                            ?next movie:year ?year.
                            ?next movie:views ?views.
                        }
                        ORDER BY DESC(?year) DESC(?views)
                        LIMIT 6
                    }
                }
            """)
    elif id == '02':
        sparql("""
                SELECT ?id ?name
                WHERE { 
                    ?id genre:name ?name.
                    ?movie movie:genre ?id.
                }
                GROUP BY ?id ?name
                ORDER BY DESC(COUNT(?movie))
            """)
    return 'OK'


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
            ?id movie:isNew true.
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
            ?id movie:isTrending true.
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


def get_all_actors():
    return sparql("""
            SELECT ?id ?name (COUNT(?movie) AS ?movies)
            WHERE {
                ?id worker:played_on ?movie.
                ?id worker:name ?name.
            }
            GROUP BY ?id ?name
            ORDER BY DESC (?movies)
        LIMIT 500""")


def get_all_directors():
    return sparql("""
            SELECT ?id ?name (COUNT(?movie) AS ?movies)
            WHERE {
                ?id worker:directed ?movie.
                ?id worker:name ?name.
            }
            GROUP BY ?id ?name
            ORDER BY DESC (?movies)
        LIMIT 500""")


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


def movies_by_genre(genre):
    return sparql("""
        SELECT *
        WHERE { 
            ?id movie:title ?movie.
            OPTIONAL{
                ?id movie:year ?year.
                ?id movie:score ?score.
                ?id movie:genre genre:toSearch
            }
        }
        ORDER BY DESC(?year) DESC(?score)
        LIMIT 500
    """.replace("toSearch", genre))


def get_movie_details(id):
    result = sparql("""
        SELECT *
        WHERE {
            movie:""" + id + """ movie:title ?title.
            movie:""" + id + """ movie:year ?year.
            movie:""" + id + """ movie:score ?score.
            ?director_id worker:directed movie:""" + id + """.
            ?director_id worker:name ?director.
        }
    """)
    return result[0] if result else None


def get_movie_genres(id):
    return sparql("""
        SELECT *
        WHERE {
            movie:""" + id + """ movie:genre ?id.
            ?id genre:name ?name.
        }
    """)


def get_movie_actors(id):
    return sparql("""
        SELECT *
        WHERE {
            ?id worker:played_on movie:""" + id + """.
            ?id worker:name ?name.
        }
    """)


def get_movie_awards(id):
    return wikisparql("""
        SELECT ?awardsLabel 
            WHERE 
            {
              ?movie wdt:P345 "ID".
              ?movie wdt:P166 ?awards.
              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
    """.replace("ID",id))


def get_movie_nomeations(id):
    return wikisparql("""
        SELECT ?nominatedForLabel 
            WHERE 
            {
              ?movie wdt:P345 "ID".
              ?movie wdt:P1411 ?nominatedFor.
              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
    """.replace("ID",id))


def get_movie_companies(id):
    return wikisparql("""
        SELECT ?id ?companiesLabel
            WHERE 
            {
              ?movie wdt:P345 'tt1431045'.
              ?movie wdt:P272 ?companies.
              ?companies wdt:P345 ?id
              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
    """.replace("ID",id))


def get_worked_with(id):
    return sparql("""
            SELECT *
            WHERE {
                worker:""" + id + """ movie:workedWith ?id.
                ?id worker:name ?name.
            }
            LIMIT 6
        """)
