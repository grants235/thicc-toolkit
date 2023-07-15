import click
import copy

from ..utils import helpers
from ..utils import networking
from ..utils import defaults

def list(project, args): 
    hosts = helpers.get_hosts(project)
    if len(hosts['include']) != 0:
        click.secho("""Live Hosts (in-scope)
---------------------""", bold=True)
        for host in hosts['include']:
            if host['live'] and host['in_scope']:
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
        ips = networking.ipv4_or_subnet_listing(host)
        if len(ips) != 0:
            ping_res = networking.multi_ping(ips)
            for ip in ping_res['success']:
                hosts["include"].append({"host": ip, "type": "ip", "live": True, "in_scope": helpers.is_in_scope(project, ip)})
            for ip in ping_res['fail']:
                hosts["include"].append({"host": ip, "type": "ip", "live": False, "in_scope": helpers.is_in_scope(project, ip)})
        else:
            if networking.can_resolve_domain(host):
                hosts["include"].append({"host": host, "type": "domain", "live": True, "in_scope": helpers.is_in_scope(project, host)})
            else:
                hosts["include"].append({"host": host, "type": "domain", "live": False, "in_scope": helpers.is_in_scope(project, host)})
    helpers.write_hosts(project, hosts)
    click.secho("Host update complete", dim=True)

def clear(project, args): 
    helpers.write_hosts(project, defaults.DEFAULT_HOSTS)
    click.secho("Cleared hosts file. Run `hosts update` to re-add hosts based on the scope", dim=True)

# def update_hosts(project, host):
 #    hosts_old = helpers.get_hosts(project)