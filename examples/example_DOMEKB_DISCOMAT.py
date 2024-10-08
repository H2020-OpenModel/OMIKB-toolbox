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
from discomat.ontology.namespaces import CUDS, MIO, MISO

"""
- initialise the tool box
- requires properly defined omikb.yml file (see examples folder)
- requires the user to be loged into the remobe omi hub (e.g. https://hub.openmodel.app)
"""
kb = DomeKB("dome_kb")


print("kb.ping", kb.ping())

print(kb.is_online)

print(kb.stats())
prefixes = {
    "ex": "http://example.org/",
    "miso" : "https://materials-discovery.org/miso#",
    "mio"  : "https://materials-discovery.org/mio#",
    "rdfs" : "http://www.w3.org/2000/01/rdf-schema#"
    }


query=InsertLib.add_triple(s="miso:sim0",  p="rdfs:type", o="miso:WAWA", prefixes=prefixes)

kb.update(query)