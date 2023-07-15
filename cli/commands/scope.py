import click
from ..utils import helpers
from ..utils import defaults

def list(project, args):
    scope = helpers.get_scope(project)

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
    

def add_included(project, host):
    add(project, host[0], 'include')
    

def add_excluded(project, host):
    add(project, host[0], 'exclude')

def add(project, host, verb):
    scope = helpers.get_scope(project)
    if host not in scope[verb]:
        scope[verb].append(host)
        helpers.write_scope(project, scope)
        click.secho(f"Added {host} to {verb}d scope", dim=True)
    else:
        click.secho(f"ERROR: {host} already excluded in scope", dim=True)

def remove(project, host):
    scope = helpers.get_scope(project)
    host = host[0]
    if host in scope['include']:
        scope['include'].remove(host)
        helpers.write_scope(project, scope)
        click.secho(f"Removed {host} from included scope", dim=True)
    elif host in scope['exclude']:
        scope['exclude'].remove(host)
        helpers.write_scope(project, scope)
        click.secho(f"Removed {host} from excluded scope", dim=True)
    else:
        click.secho(f"ERROR: {host} is not is scope", dim=True)

def clear(project, args):
    helpers.write_scope(project, defaults.DEFAULT_SCOPE)
    click.secho("Cleared project scope", dim=True)