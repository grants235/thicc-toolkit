import click
import copy

from ..utils import networking
from ..utils import defaults
from ..utils import helpers

def list(state, args): 
    hosts = state.get_hosts()
    if len(hosts['include']) != 0:
        click.secho("""Live Hosts (in-scope)
---------------------""", bold=True)
        for host in hosts['include']:
            if host['live'] and host['in_scope']:
                click.secho(host['host'])
    else:
        click.secho("No hosts found! Run `hosts update` if you believe this is not correct based on the scope", dim=True)

def list_all(state, args):
    hosts = state.get_hosts()
    if len(hosts['include']) != 0:

        click.secho("""Live Hosts (in-scope)
---------------------""", bold=True)
        for host in hosts['include']:
            if host['live'] and host['in_scope']:
                click.secho(host['host'])

        click.secho("""Dead Hosts (in-scope)
---------------------""", bold=True)
        for host in hosts['include']:
            if not host['live'] and host['in_scope']:
                click.secho(host['host'])      
    else:
        click.secho("No hosts found! Run `hosts update` if you believe this is not correct based on the scope", dim=True)

def update(state, args):
    scope = state.get_scope()
    hosts = copy.deepcopy(defaults.DEFAULT_HOSTS)
    click.secho("Updating the host list based on scope ...", dim=True)
    for host in scope['exclude']:
        ips = networking.ipv4_or_subnet_listing(host)
        if len(ips) != 0:
            for ip in ips:
                hosts["exclude"].append({"host": ip})
        else:
            hosts["exclude"].append({"host": host})
    state.write_hosts(hosts)
    for host in scope['include']:
        if "*" in host:
            continue
        obj = add_host_obj(state, host)
        if obj is not None:
            hosts["include"].append(obj)
    state.write_hosts(hosts)
    click.secho("Host update complete", dim=True)


def update_scope(state, host, type):
    hosts = state.get_hosts()
    if type == 'include':
        if "*" not in host and host not in [data["host"] for data in hosts["include"]]:
            obj = add_host_obj(state, host)
            if obj is not None:
                hosts['include'].append(obj)
    else:
        if host not in [data["host"] for data in hosts["exclude"]]:
            obj = add_host_obj(state, host)
            if obj is not None:
                hosts['exclude'].append(obj)
    state.write_hosts(hosts)


def clear(state, args): 
    state.write_hosts(defaults.DEFAULT_HOSTS)
    click.secho("Cleared hosts file. Run `hosts update` to re-add hosts based on the scope", dim=True)

def set_active(state_obj, args):
    host = args[0]
    state = state_obj.get_state()
    hosts = state_obj.get_hosts()
    if host in [data["host"] for data in hosts["include"]]:
        state["state_info"]["active_host"] = args[0]
        state_obj.write_state(state)
        click.secho("Successfully set active host", dim=True)
    else:
        click.secho(f"ERROR: Cannot find host {host} in host list. Please update scope or hosts lists to resolve this", fg='yellow')

# internal function (Used only to get object and create dir for included hosts)
def add_host_obj(state, host) -> object:
    ips = networking.ipv4_or_subnet_listing(host)
    if len(ips) != 0:
        ping_res = networking.multi_ping(ips)
        for ip in ping_res['success']:
            host_obj = {"host": ip, "type": "ip", "live": True, "in_scope": helpers.is_in_scope(state, ip)}
        for ip in ping_res['fail']:
            host_obj =  {"host": ip, "type": "ip", "live": False, "in_scope": helpers.is_in_scope(state, ip)}
    else:
        host_obj =  {"host": host, "type": "domain", "live": networking.can_resolve_domain(host), "in_scope": helpers.is_in_scope(state, host)}
    if host_obj["live"] and host_obj["in_scope"]:
        helpers.create_dir(f"{state.project}/{host_obj['host']}")
    return host_obj
