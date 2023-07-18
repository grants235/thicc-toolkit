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

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def is_in_scope(state, host): 
    hosts = state.get_hosts()
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
