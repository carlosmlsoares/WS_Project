from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF
import re
import csv

serializer = re.compile('[^A-Za-z0-9]+')


g = Graph()
imdb = Namespace('http://ourimdb.com/imdb#')
movie = Namespace('http://ourimdb.com/imdb/movie#')
movie_genre = Namespace('http://ourimdb.com/imdb/movie/genre#')
worker = Namespace('http://ourimdb.com/imdb/worker#')

with open('assets/movie_metadata.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if not all([row[predicate] for predicate in ['director', 'actor_1_name', 'title', 'year', 'score']]):
            continue
        current = URIRef(movie[row['movie_imdb_link'].split('title/')[1].split('/')[0]])

        # director
        director = URIRef(worker[serializer.sub('', row['director']).lower()])
        g.add((director, RDF.type, imdb.worker))
        g.add((director, worker.name, Literal(row['director'])))
        g.add((director, worker.directed, current))
        # g.add((current, movie.directed_by, director))

        # actors
        for actor_col in ['actor_1_name', 'actor_2_name', 'actor_3_name']:
            if not row[actor_col]:
                continue
            actor = URIRef(worker[serializer.sub('', row[actor_col]).lower()])
            g.add((actor, RDF.type, imdb.worker))
            g.add((actor, worker.name, Literal(row[actor_col])))
            g.add((actor, worker.played_on, current))
            # g.add((current, movie.played_by, actor))

        # genres
        for genre_name in row['genres'].split('|'):
            genre = URIRef(movie_genre[serializer.sub('', genre_name).lower()])
            g.add((genre, RDF.type, imdb.genre))
            g.add((genre, movie_genre.name, Literal(genre_name)))
            g.add((current, movie.genre, genre))

        # each literal
        g.add((current, RDF.type, imdb.movie))
        for predicate in ['title', 'year', 'score', 'duration', 'color', 'language', 'country', 'budget', 'aspect_ratio']:
            g.add((current, movie[predicate], Literal(row[predicate])))


# Bind a few prefix, namespace pairs for more readable output
g.bind("imdb", imdb)
g.bind("movie", movie)
g.bind("genre", movie_genre)
g.bind("worker", worker)

g.serialize('assets/movie_metadata.n3', format='n3')
# color,director_name,num_critic_for_reviews,duration,director_facebook_likes,actor_3_facebook_likes,actor_2_name,actor_1_facebook_likes,gross,genres,actor_1_name,movie_title,num_voted_users,cast_total_facebook_likes,actor_3_name,facenumber_in_poster,plot_keywords,movie_imdb_link,num_user_for_reviews,language,country,content_rating,budget,title_year,actor_2_facebook_likes,imdb_score,aspect_ratio,movie_facebook_likes

res = g.query(
    "select *" +
    "where { " +
    "    ?m rdf:type imdb:movie." +
    "    ?m movie:title ?t." +
    "    ?m movie:year ?y." +
    "    FILTER (?y >= '2016')." +
    "} limit 100 ")

for r in res:
    print(r)
