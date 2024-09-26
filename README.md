# OMIKB-toolbox: The OpenModel Knowledge-Base Tool-Box

A python class with methods to make working with OMIKB as easy as possible. 

## Features: 
- allows to acces the knowledge base (KB) and other API services from within the user's own network, e.g. local desktop and the remote omi services 
-  allows to acces the knowledge base (KB) and other API services from within the omi jupyter hub network  
- provide simple ways to check the status of services (for now supports only fuseki servers)
- Authenticate users seamlesly with the omi hub 

## How does it work

Once the user installes omikb, they need to configure an omikb.yml file and save it in their home folder. This will be read by omikb. 

the user has to store the omi hub API key obtianed as described in the omi infrastructure project [see omi docs on git hub for example](https://github.com/H2020-OpenModel/infrastructure/tree/main/docs).

once instantiated, omikb uses the API key to obtain an access key to the omi. This access key has a limited life span of 1 hour (can be extended if needed, please contact developers.)

## Example

Here is a simple example, the same works on omi hub (https://hub.openmodel.app) or on your own machine running python. 

- Open a session to the OMI default service which is now an Apache Jena Fuseki Sparql end point supporting the standard Sparql [w3C RDF query language](https://www.w3.org/TR/rdf-sparql-query/).

``` 
from omikb.omikb import kb_toolbox
...

kb=kb_toolbox()
...

```
this creates an instance, which contains all the information you need to access the service, provides of course you have logged in. 

Now we can use things like kb.query("some sparql query"), or kb.update("some INSERT statement"), etc to seamlessly interact with the knowledge base

see [first steps example here](./examples/example_OMIKB_FIRST_STEPS.py)

# Installation 

Install the package directly from GitHub:

```sh
pip install git+https://github.com/H2020-OpenModel/OMIKB-toolbox.git
```

to upgrade do: 

```sh
pip install --upgrade git+https://github.com/H2020-OpenModel/OMIKB-toolbox.git
```


# Developers guide and what next 
currently, version 0.1 supports only one service, which is an apache jena fuseki end point, however, one can build support for other services by following the steps: 

1. copy the existing kb_toolbox class
2. modify the methods according to the service end points as defined in omi 
3. add a services section to omikb.yml 

for example, one can create remote access to OntoFlow or other services in a similar manner. 

See the jupyter Notebook demo in doc folder 

```python 

from omikb.omikb import kb_toolbox 
```