import requests
from rdflib import Graph, URIRef, Literal
import yaml 
import os
import json
from urllib.parse import urlparse, urljoin
from pathlib import Path
from typing import Union


class kb_toolbox:
    def __init__(self):
        """with open("~/OMIKB/kb_config.yml", 'r') as _file:
        kb_config = yaml.safe_load(_file)
        if kb_config is None:
            raise ValueError("Missing Configuration for knowledge base, please read the documentation")
            # should add a link to it, 
        """
        self.query_iri = "https://dev.openmodel.app/fuseki/dataset/sparql"
        self.update_iri= "https://dev.openmodel.app/fuseki3/dataset/update"
        self.data_iri = "https://dev.openmodel.app/fuseki3/dataset/data"
        self.ping_iri = "https://dev.openmodel.app/fuseki/$/ping"
        self.stats_iri = "https://dev.openmodel.app/fuseki/$/stats"
        
        
        self.hub_iri = "https://hub_dev.openmodel.app"
        self.hub_token= " 422ad0c0e52e45faab27204dd2464f39"
        self.username= os.getenv('JUPYTERHUB_USER')
        self.hub_api_header= {
                                 'Authorization': f'token {self.hub_token}',
                                    }
        response = requests.get(f"{self.hub_iri}/hub/api/users/{self.username}", headers=self.hub_api_header)
        if response.status_code == 200:
            user_data = response.json()
            auth_state = user_data.get('auth_state', {})
            access_token = auth_state.get('access_token',{})
            print("Hello Usr: Yout access token is obtained: (Showing last 10 digits only)", access_token[-10:])
        else:
            print(f"Error fetching user data: {response.status_code} - \
                      Sorry, you are not able to use OMI - Contact Admin")
        self.access_token=access_token=user_data['auth_state']['access_token']
        self.userinfo=user_data['auth_state']['oauth_user']
        self.omi_get_headers= {
                              'accept': "application/json, text/turtle",
                              'Authorization': f'Bearer {access_token}'
        }
        create_headers = lambda access_token: {
        "Content-Type": 'text/turtle',
        "Authorization": f"Bearer {access_token}"
        }
        self.data_headers = create_headers(self.access_token)
        
        create_headers = lambda access_token: {
        "Content-Type": "application/sparql-update",
        "Authorization": f"Bearer {access_token}"
        }
        self.update_headers = create_headers(self.access_token)
       
        print("Initialised Knowledge Base and OMI access from the jupyter interface for the user:")
        print(print(json.dumps(self.userinfo, indent=2)))
        
        
    def query(self, query):
        # note proper encoding, seems like response does not encode. 
        params = {'query': query}
        response = requests.get(self.query_iri, params=params, headers=self.omi_get_headers, timeout=50)
        return (response)
    
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
        params = {'query': query}
        response = requests.get(self.query_iri, params=params, headers=self.omi_get_headers, timeout=50)
        return (response)
    
    def ping(self):
        try:
            response = requests.get(self.ping_iri, headers=self.omi_get_headers, timeout=50)
            if response.status_code == 200:
                return "The OpenModel Knowledge Base is Alive!"
            else:
                return f"Unexpected status code: {response.status_code}"
        except requests.RequestException as e:
            return f"server down: {e}"
        
    # check if the server is online
    @property
    def is_online(self):
        try:
            response = requests.get(self.ping_iri, headers=self.omi_get_headers, timeout=50)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException as e:
            return f"Server down, exception obtained: {e}"

    def stats(self):
        response = requests.get(self.stats_iri, headers=self.omi_get_headers, timeout=50)
        #return(json.dumps(json.loads(response.text), indent=2))

        #return (json.dumps(response.text, indent=2))
        return(response.json())
            
    def update(self, query):

        response = requests.post(self.update_iri, data=query, headers=self.update_headers)
        if response.status_code == 200:
            print("SPARQL update executed successfully.")
        else:
            print(f"Error: {response.status_code} - {response.text}")

            
    def triples_count(self):

        # query to count all triples
        query = """
        SELECT (COUNT(*) as ?triplesCount)
        WHERE { ?s ?p ?o }
        """

        
        
    def import_ontology(self, source: Union[str, Path]) -> requests.Response:
        # should add graph name (default user;s named graph) 
    
        if not source:
            raise ValueError("Error - You must specify either a URL of an ontology or a file path as source!.")
        g=Graph()
        g.parse(source, format="turtle")
        ttl_data=g.serialize(format='turtle').encode('utf-8')
        #graph_url = f"{fuseki_url}/data?graph={graph_name}"
        
        response = requests.post(self.data_iri, data=ttl_data, headers=self.data_headers)
        if response.status_code in [200, 201, 204]:
            graph_name="default"
            print(f"Successfully added {len(g)} triplets to the dataspace {graph_name} in the knowledge base.")
        else:
            print(f"failed to import ontology: {response.status_code}, {response.text}")

        return response
