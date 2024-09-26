#!/usr/bin/env python
# coding: utf-8

# In[10]:


from omikb.omikb import kb_toolbox
import json
import rdflib
from typing import Union
#from ontoflow.engine import OntoFlowEngine
#from tripper import Triplestore
import os, yaml
import pprint

# # Using the OMIKBK Tool Box
# - Manages in the back stage all internal setup needed to access protected services
# - provide convenient easy to use interface to the Knowledge Base triple store back end including
#   - keywords search on all triples 
#   - sparql query, including INSERT, SPARQL, DELETE etc
#   - Graph Store Protocol Query for entire datasets 
#   - Provide easy access to all end points 
#   - enable OMI users to obtain shared API Keys for access from outside the omi (WIP)
#   
# ## Installing
#   OMIKB is builtin, and no need to install it, but if you want to develop or work on pre release, simpley go to OMIKB git hub repo](https://github.com/H2020-OpenModel/OMIKB-toolbox) and follow the instructions to install here (basically open a terminal and type the pip...)
#   
# ## Using
# See this example and the other ones. 
# 

# In[11]:


kb=kb_toolbox() # initialise the tool box, which shows some information.


# In[13]:


print(kb.ping()) # ping the triple store server to see if it is alive


# In[14]:


print(kb.is_online)


# In[15]:


print(kb.data_iri)  # this is the external facing end point, which should be used from outside. kb.

# you can also check the other end points

#kb.query_iri = "https://dev.openmodel.app/fuseki/dataset/sparql"
#kb.update_iri= "https://dev.openmodel.app/fuseki3/dataset/update"
#kb.data_iri = "https://dev.openmodel.app/fuseki3/dataset/data"
#kb.ping_iri = "https://dev.openmodel.app/fuseki/$/ping"
#kb.stats_iri = "https://dev.openmodel.app/fuseki/$/stats"


# In[17]:


print(kb.stats())


# in the next example we test some queries

# In[18]:


sparql_query = "SELECT * WHERE { ?s ?p ?o } LIMIT 100"


# In[19]:


s=kb.query(sparql_query)


# In[20]:


pprint.pprint(s.content, indent=2, width=80)

print(kb.access_token)

print(f"kb.query_iri {kb.query_iri}")
print(f"kb.pquery_iri {kb.pquery_iri}")

