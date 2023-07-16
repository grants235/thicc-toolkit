import shlex
import json
import os
import fnmatch


def get_tokens(text: str) -> list:
    try:
        tokens = shlex.split(text)
    except ValueError:
        # return a response that wont match a next command
        tokens = ['lajfhlaksjdfhlaskjfhafsdlkjh']

    return tokens

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_in_scope(project, host): 
    hosts = get_hosts(project)
    simple_hosts = []
    for x in hosts['exclude']:
        simple_hosts.append(x["host"])
    if host in simple_hosts:
        return False
    not_found = True
    for x in simple_hosts:
        if fnmatch.fnmatchcase(host, x):
            not_found = False
    return not_found

# state ops
def get_state(project) -> dict:
    with open(f"{project}/.thicc-state.json", "r") as thicc_state:
        state = json.loads(thicc_state.read())
    return state

def write_state(project, state: dict):
    with open(f"{project}/.thicc-state.json", "w") as thicc_state:
        thicc_state.write(json.dumps(state, indent=2))

# scope ops
def get_scope(project) -> dict:
    with open(f"{project}/scope.json", "r") as thicc_scope:
        scope = json.loads(thicc_scope.read())
    return scope

def write_scope(project, scope: dict): 
    with open(f"{project}/scope.json", "w") as thicc_scope:
        thicc_scope.write(json.dumps(scope, indent=2))

# host ops
def get_hosts(project) -> dict:
    with open(f"{project}/.hosts.json", "r") as host_file:
        hosts = json.loads(host_file.read())
    return hosts

def write_hosts(project, hosts):
    with open(f"{project}/.hosts.json", "w") as host_file:
        host_file.write(json.dumps(hosts, indent=2))
