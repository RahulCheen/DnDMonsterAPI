import configparser
import os
from py2neo import Graph, Relationship

config_file = os.path.join('auth.cfg')
if not os.path.exists(config_file):
    raise FileNotFoundError(f"Configuration file {config_file} was not found. Please create config to connect to neo4j db.")

config = configparser.ConfigParser()
config.read(config_file)
address = config['NEO4J']['ADDRESS']
user = config['NEO4J']['USER']
password = config['NEO4J']['PASSWORD']
graph = Graph(address, auth=(user, password))

def create_relationship(property: str, weight: float):
    query = f"""
    MATCH (m1:Monster), (m2:Monster)
    WHERE m1.{property} = m2.{property} and m1 <> m2
    MERGE (m1)-[r:SIMILAR_{property.upper()}]->(m2)
    ON CREATE SET r.score = {weight}
    """

    return query

properties_to_relate = [
    ("size", 0.5),
    ("type", 1),
    ("alignment", 0.1),
    ("challenge_rating", 0.5),
    ("strength", 0.2),
    ("dexterity", 0.2),
    ("constitution", 0.2),
    ("intelligence", 0.2),
    ("wisdom", 0.2),
    ("charisma", 0.2),
    ("damage_vulnerabilities", 0.5),
    ("damage_resistances", 0.5),
    ("damage_immunities", 0.5),
    ("condition_immunities", 0.5)
]

for property, weight in properties_to_relate:
    graph.run(create_relationship(property, weight))
    print(f"Successfully defined relationships for {property}")
