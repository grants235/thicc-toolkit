import click

from ..utils import helpers
from ..utils import defaults

from .tools.sublister import run as sublister_run


def all(state, host):
    return "todo"

def sublister(state, host):
    host = host[0]
    state.push_to_queue(sublister_run, (host, f"{state.project}/{host}/sublist3r.txt"), sublister_callback, f"{host} - Sublist3r")
    
def sublister_callback(state, future, future_succeeded):
    if not future_succeeded:
        return
    if len(future.result()) == 0:
        click.secho("No subdomains found with sublist3r", dim=True)
    else:
        #todo
        return
    