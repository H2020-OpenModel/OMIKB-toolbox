import requests
from rdflib import Graph, URIRef, Literal
import yaml 
import os
import json
from urllib.parse import urljoin

class kb_toolbox:
    def __init__(self):
        """with open("~/OMIKB/kb_config.yml", 'r') as _file:
        kb_config = yaml.safe_load(_file)
        if kb_config is None:
            raise ValueError("Missing Configuration for knowledge base, please read the documentation")
            # should add a link to it, 
        """
        self.query_iri = "https://openmodel.app/fuseki/dataset/sparql"
        self.update_iri= "https://openmodel.app/fuseki3/dataset/update"
        self.ping_iri = "https://openmodel.app/fuseki/$/ping"
        self.stats_iri = "https://openmodel.app/fuseki/$/stats"
        
        
        self.hub_iri = "https://hub.openmodel.app"
        self.hub_token= "df0937d5a5a641bc83e61f2fa040798d"
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
            print(f"Error fetching user data: {response.status_code} - Sorry, you are not able to use OMI - Contact Admin")
        self.access_token=access_token=user_data['auth_state']['access_token']
        self.userinfo=user_data['auth_state']['oauth_user']
        self.omi_headers= {
                              'accept': 'application/json',
                              'Authorization': f'Bearer {access_token}'
        }
        print("Initialised Knowledge Base and OMI access from the jupyter interface for the user:")
        print(print(json.dumps(self.userinfo, indent=2)))
        
        
    def query(self, query):
        response = requests.get(self.query_iri+f"?query={query}", headers=self.omi_headers, timeout=50)
        return (response)
    
    def search_keyword(self, keyword):
        query = f"""
                SELECT ?s ?p ?o
                WHERE {{
                  ?s ?p ?o .
                  FILTER (regex(str(?s), "{search_string}", "i") ||
                          regex(str(?p), "{search_string}", "i") ||
                          regex(str(?o), "{search_string}", "i"))
                }}
                """
        response = requests.get(self.query_iri+f"?query={query}", headers=self.omi_headers, timeout=50)
        return (response)
    
    @property
    def ping(self):
        try:
            response = requests.get(self.ping_iri, headers=self.omi_headers, timeout=50)
            if response.status_code == 200:
                return ("The OpenModel Knowledge Base is Alive!")
            else:
                return ("The OpenModel Knowledge Base is Alive!")
            except requests.RequestException as e:
                return f"server down: {e}"
    # check if the server is online
    @property
    def is_online(self):
        try:
            response = requests.get(self.ping_iri, headers=self.omi_headers, timeout=50)
            if response.status_code == 200:
                return True
            else:
                return False
            except requests.RequestException as e:
                return f"Server down, exception obtained: {e}"

    def stats(self):
        response = requests.get(self.stats_iri, headers=self.omi_headers, timeout=50)
        print(json.dumps(json.loads(response.text), indent=2))

        #return (json.dumps(response.text, indent=2))
                
            
    def update(self, query):
        create_headers = lambda access_token: {
        "Content-Type": "application/sparql-update",
        "Authorization": f"Bearer {access_token}"
        }
        self.headers = create_headers(self.access_token)
        response = requests.post(self.update_iri, data=query, headers=self.headers)
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


