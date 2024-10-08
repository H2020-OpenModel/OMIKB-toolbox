import requests
from rdflib import Graph, URIRef, Literal
import yaml
import os
import json
from urllib.parse import urlparse, urljoin
from pathlib import Path
from typing import Union

"""
The Dome 4.0 Knowledge Base Interface, built based on omikb.py by removing the bearer key as we are 
directly connecting to the DOME4.0 fuseki image behind the semantic discovery and changed the default service. 

this shares the same k services files, still named omikb.py, though this may change in teh future. 

"""


def triples_count():
    # query to count all triples
    query = """
    SELECT (COUNT(*) as ?triplesCount)
    WHERE { ?s ?p ?o }
    """


class KbToolBox:
    def __init__(self, service=None):
        """
        if service is none, the default one is used, other wise the specified one of exists
        the service is the name of the service in omikb.yml
        :param service:
        """

        service = service or "dome_kb"

        with open(os.path.expanduser('~/omikb.yml'), 'r') as file:
            config = yaml.safe_load(file)

        self.query_iri = config["services"][service]["end_point"]["query"]
        self.update_iri = config["services"][service]["end_point"]["update"]
        self.data_iri = config["services"][service]["end_point"]["data"]
        self.ping_iri = config["services"][service]["end_point"]["ping"]
        self.stats_iri = config["services"][service]["end_point"]["stats"]

        self.omi_get_headers = {
            'Accept': "application/json"
        }
        self.data_headers = {
            'Accept': "application/json",
            'Content-Type': 'text/turtle'
        }
        self.update_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/sparql-update'
        }
        self.ping_headers = self.omi_get_headers
        self.ping_headers["Content-Type"] = "application/x-www-form-urlencoded"

    def query(self, query):
        # note proper encoding, seems like response does not encode. 
        params = {'query': query}
        response = requests.post(self.query_iri, params=params, headers=self.omi_get_headers, timeout=50)
        return response

    def search_keyword(self, keyword):
        query = f"""
                SELECT ?s ?p ?o
                WHERE {{
                  ?s ?p ?o .
                  FILTER (regex(str(?s), "{keyword}", "i") ||
                          regex(str(?p), "{keyword}", "i") ||
                          regex(str(?o), "{keyword}", "i"))
                }}
                """
        response = self.query(query)
        return response

    def ping(self):
        try:

            response = requests.post(self.ping_iri, headers=self.ping_headers, timeout=50)
            if response.status_code == 200:
                return "The DOME 4.0 (internal) Knowledge Base is Alive!"
            else:
                return f"Unexpected status code: {response.status_code}"
        except requests.RequestException as e:
            return f"server down: {e}"

    # check if the server is online
    @property
    def is_online(self):
        try:

            response = requests.post(self.ping_iri, headers=self.ping_headers, timeout=50)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException as e:
            return f"Server down, exception obtained: {e}"

    def stats(self):
        response = requests.post(self.stats_iri, headers=self.ping_headers, timeout=50)
        return response.json()

    def update(self, query):
        response = requests.post(self.update_iri, data=query, headers=self.update_headers)
        if response.status_code == 200:
            print("SPARQL update executed successfully.")
        else:
            print(f"--Error: {response.status_code} - {response.text}")

    def import_ontology(self, source: Union[str, Path]) -> requests.Response:
        # should add graph name (default user;s named graph) 

        if not source:
            raise ValueError("Error - You must specify either a URL of an ontology or a file path as source!.")
        g = Graph()
        g.parse(source, format="turtle")
        ttl_data = g.serialize(format='turtle').encode('utf-8')

        response = requests.post(self.data_iri, data=ttl_data, headers=self.data_headers)
        if response.status_code in [200, 201, 204]:
            graph_name = "default"
            print(f"Successfully added {len(g)} triplets to the dataspace {graph_name} in the knowledge base.")
        else:
            print(f"failed to import ontology: {response.status_code}, {response.text}")

        return response

    def curl(self):
        curl_command = f"curl -X GET '{self.stats_iri}' " + \
                       " ".join([f"-H '{key}: {value}'" for key, value in self.omi_get_headers.items()])

        print(curl_command)

