# OMIKB-toolbox: The OpenModel Knowledge-Base Tool-Box

A python class with methods to make working with OMIKB easy. 

## Features: 
- provide an easy way to connect either from within the OMI hub (on the remote jupyter session on hub.openmode.app) or from your own workstation (windows or linux or mac.. ) to any service running on omi.openmodel.app in a secure manner 
- provide simple ways to check the status of services (e.g. to ping a fuseki server)
- provide simple methods for users to access the API without worrying about authenitcation headers/low level request libraries etc. 
- Providers an example for OMI service providers and developers a template to build a new or extend omiKB for other services.
- to log in and use API, the user has to only login to the online hub, and establish a session, which will normally last for 60 minutes, but the user can extend it by relogin. 
- omiKB fetches a temporary key for using the remote servcies, provided the user has generated and stored their own API Key from the hub. See documentation later. 

## How does it work

Here is a simple example, the same works on omi hub (https://hub.openmodel.app) or on your own machine running python. 

We assume you already installed all requirements (see next chapter) and have a proper python environment. 

We also assume the user has set up and configured a key and created an omikb.yml config file (which should be in the home folder of the user in either the remote hub, or the workstation/client they are using).


- Open a session to the OMI default service which is now an Apache Jena Fuseki Sparql end point supporting the standard Sparql [w3C RDF query language](https://www.w3.org/TR/rdf-sparql-query/).

``` 
from omikb.omikb import kb_toolbox
...

kb=kb_toolbox()
...

```
this creates an instance, which contains all the information you need to acccess the service, provides of course you have logged in. 




# Installation 

Install the package directly from GitHub:

```sh
pip install git+https://github.com/H2020-OpenModel/OMIKB-toolbox.git
```

to upgrade do: 

```sh
pip install --upgrade git+https://github.com/H2020-OpenModel/OMIKB-toolbox.git
```


# Usage: 

See the jupyter Notebook demo in doc folder 

```python 

from omikb.omikb import kb_toolbox 
```