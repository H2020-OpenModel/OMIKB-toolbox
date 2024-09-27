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
print("kb.ping", kb.ping())

""" a more machine freindly test, return true or false"""
print(kb.is_online)

""" get the stats, assuming it is a fuseki end point, otherwise not defined """
print(kb.stats())


update_query = """
DELETE WHERE {?s ?p ?o .}

"""
s = kb.update(update_query)

sparql_query = "SELECT * WHERE { ?s ?p ?o } LIMIT 10"
s = kb.query(sparql_query)
print(json.dumps(json.loads(s.content), indent=2))