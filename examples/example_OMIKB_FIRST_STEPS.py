#!/usr/bin/env python
# coding: utf-8

# In[10]:


from omikb.omikb import kb_toolbox
import json
import rdflib
from typing import Union
# from ontoflow.engine import OntoFlowEngine
# from tripper import Triplestore
import os, yaml
import pprint

kb = kb_toolbox()  # initialise the tool box, which shows some information.

print(kb.ping())  # ping the triple store server to see if it is alive

print(kb.is_online)

print(kb.stats())

sparql_query = "SELECT * WHERE { ?s ?p ?o } LIMIT 100"

s = kb.query(sparql_query)
print(s.content)

update_query = """
PREFIX ex: <http://example.org/>
INSERT DATA {
    ex:subject ex:predicate "object" .
    ex:aaaaaaaaaaaaaaaaaaaaaaaa ex:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb ex:c .
}
"""
s = kb.update(update_query)

# print(kb.access_token)
s = kb.query(sparql_query)
print(s.content)


update_query = """
DELETE WHERE {?s ?p ?o .}

"""
s = kb.update(update_query)

# print(kb.access_token)
s = kb.query(sparql_query)
print(s.content)

update_query="DELETE WHERE { ?subject ?predicate ?object . }"


s = kb.update(update_query)
s = kb.query(sparql_query)

print(s.content)
