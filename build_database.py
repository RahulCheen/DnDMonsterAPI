import configparser
from py2neo import Graph, Node

config = configparser.ConfigParser()
config.read('auth.cfg')

address = config['NEO4J']['ADDRESS']
user = config['NEO4J']['USER']
password = config['NEO4J']['PASSWORD']

graph = Graph(address, auth=(user, password))

