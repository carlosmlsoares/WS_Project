from SPARQLWrapper import SPARQLWrapper, JSON
from unidecode import unidecode

CONN = SPARQLWrapper("https://query.wikidata.org/sparql")
PREFIXES = [
    ('wd', 'http://www.wikidata.org/entity/'),
    ('wdt', 'http://www.wikidata.org/prop/direct/'),
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


def wikisparql(query):
    CONN.setQuery(PREFIXES_SPARQL + query)
    CONN.setReturnFormat(JSON)
    json = CONN.query().convert()

    headers = json['head']['vars']
    result = [{var: clean(row[var]["value"]) for var in headers}
              for row in json["results"]["bindings"] if all([var in row for var in headers])]
    return result
