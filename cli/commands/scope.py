import click
from ..utils import defaults
from ..commands import hosts

def list(state, args):
    scope = state.get_scope()

    if len(scope['include']) != 0:

        click.secho("""Included Scope
--------------""", bold=True)

        for host in scope['include']:
            click.secho(host)
        click.secho("")
    else:
        click.secho("No included hosts!", dim=True)
    
    if len(scope['exclude']) != 0:

        click.secho("""Excluded Scope
--------------""", bold=True)

        for host in scope['exclude']:
            click.secho(host)
    else:
        click.secho("No excluded hosts!", dim=True)
    

def add_included(state, host):
    add(state, host[0], 'include')
    

def add_excluded(state, host):
    add(state, host[0], 'exclude')

def add(state, host, verb):
    scope = state.get_scope()
    if host not in scope[verb]:
        scope[verb].append(host)
        state.write_scope(scope)
        click.secho(f"Added {host} to {verb}d scope", dim=True)
        hosts.update_scope(state, host, verb)
        click.secho(f"Updated the hosts list based on new scope", dim=True)
    else:
        click.secho(f"ERROR: {host} already in {verb}d scope", fg='yellow')

def remove(state, host):
    scope = state.get_scope()
    host = host[0]
    if host in scope['include']:
        scope['include'].remove(host)
        state.write_scope(scope)
        click.secho(f"Removed {host} from included scope", dim=True)
    elif host in scope['exclude']:
        scope['exclude'].remove(host)
        state.write_scope(scope)
        click.secho(f"Removed {host} from excluded scope", dim=True)
    else:
        click.secho(f"ERROR: {host} is not is scope", fg='yellow')

def clear(state, args):
    state.write_scope(defaults.DEFAULT_SCOPE)
    click.secho("Cleared project scope", dim=True)