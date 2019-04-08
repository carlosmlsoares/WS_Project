from SPARQLWrapper import SPARQLWrapper, JSON
from unidecode import unidecode

CONN = SPARQLWrapper("http://localhost:7200/repositories/imdb")
PREFIXES = [
    ('imdb', 'http://ourimdb.com/imdb#'),
    ('movie', 'http://ourimdb.com/imdb/movie#'),
    ('genre', 'http://ourimdb.com/imdb/movie/genre#'),
    ('worker', 'http://ourimdb.com/imdb/worker#')
]

PREFIXES_SPARQL = ''.join(['PREFIX ' + p + ': <' + uri + '>\n' for p, uri in PREFIXES])


def clean(value):
    if any([(uri in value) for p, uri in PREFIXES]):
        return value.split('#')[-1]

    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except:
        return unidecode(value).strip()


def sparql(query):
    CONN.setQuery(PREFIXES_SPARQL + query)
    CONN.setReturnFormat(JSON)
    json = CONN.query().convert()

    headers = json['head']['vars']
    result = [{var: clean(row[var]["value"]) for var in headers}
              for row in json["results"]["bindings"] if all([var in row for var in headers])]
    return result
