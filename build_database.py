import configparser
from py2neo import Graph, Node
import os
import json

def flatten_monster(monster: dict, parent_key: str='', sep: str='_') -> dict:
    """
    Recursively flatten a complex moster property into primitives so data is compatible with neo4j
    i.e.
    {...,
    "actions": [
        {
            "name": "Multiattack",
            "desc": "The a-mi-kuk makes two attacks: one with its bite and one with its grasping claw."
        },
        {
            "name": "Bite",
            "desc": "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 12 (2d6 + 5) piercing damage.",
            "attack_bonus": 8,
            "damage_dice": "2d6+5"
        }
    ],
    ...}

    becomes
    {
        "actions_0_name": "Multiattack",
        "actions_0_desc": "The a-mi-kuk makes two attacks: one with its bite and one with its grasping claw.",
        "actions_1_name": "Bite",
        "actions_1_desc": "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 12 (2d6 + 5) piercing damage.",
        "actions_1_attack_bonus": 8,
        "actions_1_damage_dice": "2d6+5"
    }
    """
    items = []
    for k, v in monster.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k

        if isinstance(v, dict):
            items.extend(flatten_monster(v, new_key, sep=sep).items())
        
        elif isinstance(v, list) and all(isinstance(i, dict) for i in v):
            for idx, item in enumerate(v):
                items.extend(flatten_monster(item, f'{new_key}{sep}{idx}', sep=sep).items())
        
        else:
            items.append((new_key, v))

    return dict(items)

def insert_monster(monster: dict):
    try:
        flattened_monster = flatten_monster(monster)
        monster_node = Node("Monster", **flattened_monster)
        graph.create(monster_node)
        print(f"Monster '{monster.get('name', 'unknown')} inserted successfully")
    except Exception as e:
        print(f"Error inserting monster '{monster.get('name', 'unknown')}: {e}")

config_file = os.path.join('auth.cfg')
if not os.path.exists(config_file):
    raise FileNotFoundError(f"Configuration file {config_file} was not found. Please create config to connect to neo4j db.")

config = configparser.ConfigParser()
config.read(config_file)
address = config['NEO4J']['ADDRESS']
user = config['NEO4J']['USER']
password = config['NEO4J']['PASSWORD']
graph = Graph(address, auth=(user, password))

monsters_dat = os.path.join('monsters/monsters.json')
if not os.path.exists(monsters_dat):
    raise FileNotFoundError(f"Monsters data source {monsters_dat} was not found. Please run 'get_data.py' before proceeding.")

with open(monsters_dat, 'r') as file:
    monsters_data = json.load(file)

for monster in monsters_data:
    insert_monster(monster)

print('Mosnters written to monsters database')
