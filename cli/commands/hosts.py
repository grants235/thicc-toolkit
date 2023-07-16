import click
import copy

from ..utils import helpers
from ..utils import networking
from ..utils import defaults

def list(project, args): 
    hosts = helpers.get_hosts(project)
    if len(hosts['include']) != 0:
        click.secho("""Live Hosts (in-scope and live)
---------------------""", bold=True)
        for host in hosts['include']:
            if host['live'] and host['in_scope']:
                click.secho(host['host'])
    else:
        click.secho("No hosts found! Run `hosts update` if you believe this is not correct based on the scope", dim=True)

def list_all(project, args):
    hosts = helpers.get_hosts(project)
    if len(hosts['include']) != 0:

        click.secho("""Live Hosts (in-scope and live)
---------------------""", bold=True)
        for host in hosts['include']:
            if host['live'] and host['in_scope']:
                click.secho(host['host'])

        click.secho("""Live Hosts (in-scope and dead)
---------------------""", bold=True)
        for host in hosts['include']:
            if not host['live'] and host['in_scope']:
                click.secho(host['host'])      
    else:
        click.secho("No hosts found! Run `hosts update` if you believe this is not correct based on the scope", dim=True)

def update(project, args):
    scope = helpers.get_scope(project)
    hosts = copy.deepcopy(defaults.DEFAULT_HOSTS)
    click.secho("Updating the host list based on scope ...", dim=True)
    for host in scope['exclude']:
        ips = networking.ipv4_or_subnet_listing(host)
        if len(ips) != 0:
            for ip in ips:
                hosts["exclude"].append({"host": ip})
        else:
            hosts["exclude"].append({"host": host})
    helpers.write_hosts(project, hosts)
    for host in scope['include']:
        if "*" in host:
            continue
        obj = add_host_obj(project, host)
        if obj is not None:
            hosts["include"].append(obj)
    helpers.write_hosts(project, hosts)
    click.secho("Host update complete", dim=True)


def update_scope(project, host, type):
    hosts = helpers.get_hosts(project)
    if type == 'include':
        if "*" not in host and host not in [data["host"] for data in hosts["include"]]:
            obj = add_host_obj(project, host)
            if obj is not None:
                hosts['include'].append(obj)
    else:
        if host not in [data["host"] for data in hosts["exclude"]]:
            obj = add_host_obj(project, host)
            if obj is not None:
                hosts['exclude'].append(obj)
    helpers.write_hosts(project, hosts)


def clear(project, args): 
    helpers.write_hosts(project, defaults.DEFAULT_HOSTS)
    click.secho("Cleared hosts file. Run `hosts update` to re-add hosts based on the scope", dim=True)

def set_active(project, args):
    host = args[0]
    state = helpers.get_state(project)
    hosts = helpers.get_hosts(project)
    if host in [data["host"] for data in hosts["include"]]:
        state["state_info"]["active_host"] = args[0]
        helpers.write_state(project, state)
        click.secho("Successfully set active host", dim=True)
    else:
        click.secho(f"ERROR: Cannot find host {host} in host list. Please update scope or hosts lists to resolve this", fg='yellow')

# internal function
def add_host_obj(project, host) -> object:
    ips = networking.ipv4_or_subnet_listing(host)
    if len(ips) != 0:
        ping_res = networking.multi_ping(ips)
        for ip in ping_res['success']:
            return {"host": ip, "type": "ip", "live": True, "in_scope": helpers.is_in_scope(project, ip)}
        for ip in ping_res['fail']:
            return {"host": ip, "type": "ip", "live": False, "in_scope": helpers.is_in_scope(project, ip)}
    else:
        return {"host": host, "type": "domain", "live": networking.can_resolve_domain(host), "in_scope": helpers.is_in_scope(project, host)}
