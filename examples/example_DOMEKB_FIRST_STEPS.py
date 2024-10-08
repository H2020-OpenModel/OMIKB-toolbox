#!/usr/bin/env python

from omikb.domekb import KbToolBox as DomeKB
import json
import rdflib
from typing import Union
# from ontoflow.engine import OntoFlowEngine
# from tripper import Triplestore
import os, yaml
import pprint
from discomat.cuds.utils import InsertLib, QueryLib
"""
- initialise the tool box
- requires properly defined omikb.yml file (see examples folder)
- requires the user to be loged into the remobe omi hub (e.g. https://hub.openmodel.app)
"""
kb = DomeKB("dome_kb")


print("kb.ping", kb.ping())

print(kb.is_online)

print(kb.stats())


update_query = """
DELETE WHERE {?s ?p ?o .}

"""
s = kb.update(update_query)



""" lets send a sparql query to the query end point """
sparql_query = "SELECT * WHERE { ?s ?p ?o } LIMIT 10"
s = kb.query(sparql_query)
print(json.dumps(json.loads(s.content), indent=2))

""" lets send an update query """
update_query = """
PREFIX ex: <http://example.org/>
PREFIX miso: <https://materials-discovery.org/miso#>
PREFIX mio: <https://materials-discovery.org/mio#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT DATA {
    ex:subject ex:predicate "object" .
    miso:sim0  rdfs:type miso:Simulation . 
    miso:sim0 mio:has miso:a_boundary_condition .
    miso:sim1 mio:has miso:another_boundary_condition .
}
"""

s = kb.update(update_query)
""" fetch and print to check it is updated"""
s = kb.query(sparql_query)
print(json.dumps(json.loads(s.content), indent=2))

""" delete all triples"""

update_query = """
DELETE WHERE {?s ?p ?o .}

"""
#s = kb.update(update_query)

""" check if all is printed """
s = kb.query(sparql_query)
print(json.dumps(json.loads(s.content), indent=2))


""" again using named graphs """
update_query = """
PREFIX ex: <http://example.org/>
PREFIX miso: <https://materials-discovery.org/miso#>
PREFIX mio: <https://materials-discovery.org/mio#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT DATA {
    GRAPH miso:some_simulation { 
        ex:subject ex:predicate "object" .
        miso:sim0  rdfs:type miso:Simulation . 
        miso:sim0 mio:has miso:a_boundary_condition .
        miso:sim1 mio:has miso:another_boundary_condition .
    }
}
"""
s = kb.update(update_query)

""" check if all is printed, note we need to query all graphs """
sparql_query = """
SELECT * WHERE {
  {
    # Default graph
    ?s ?p ?o .
  } UNION {
    # Named graphs
    GRAPH ?g { ?s ?p ?o }
  }
} LIMIT 100
"""

s = kb.query(sparql_query)
print(json.dumps(json.loads(s.content), indent=2))


update_query= """
DELETE WHERE {
  GRAPH ?g {
    ?subject ?predicate ?object .
  }
}"""


#s = kb.update(update_query)
s = kb.query(sparql_query)

print(json.dumps(json.loads(s.content), indent=2))


""" import an ontology """
kb.import_ontology("http://www.w3.org/People/Berners-Lee/card")

""" look for any triplet having Literal object as 'Tim Berners-Lee'"""
sparql_query = "SELECT * WHERE { ?s ?p 'Tim Berners-Lee' } LIMIT 100"
s = kb.query(sparql_query)
print(json.dumps(json.loads(s.content), indent=2))

""" search as keyword"""
s=kb.search_keyword("Berners-Lee")
print(json.dumps(json.loads(s.content), indent=2))


update_query = """
DELETE WHERE {?s ?p ?o .}

"""
#s = kb.update(update_query)


print(f" The server is {kb.query_iri}")