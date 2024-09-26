#!/usr/bin/env python

from omikb.omikb import kb_toolbox
import json
import rdflib
from typing import Union
# from ontoflow.engine import OntoFlowEngine
# from tripper import Triplestore
import os, yaml
import pprint

"""
- initialise the tool box
- requires properly defined omikb.yml file (see examples folder)
- requires the user to be loged into the remobe omi hub (e.g. https://hub.openmodel.app)
"""
kb = kb_toolbox()

"""
test if the connection is alive, this will print a log message """
print(kb.ping())

""" a more machine freindly test, return true or false"""
print(kb.is_online)

""" get the stats, assuming it is a fuseki end point, otherwise not defined """
print(kb.stats())

""" lets send a sparql query to the query end point """
sparql_query = "SELECT * WHERE { ?s ?p ?o } LIMIT 100"
s = kb.query(sparql_query)
print(s.content)

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
s = kb.update(update_query)

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


s = kb.update(update_query)
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
