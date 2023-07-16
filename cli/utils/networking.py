import ipaddress
import socket
import click
from multiping import MultiPing

def ipv4_or_subnet_listing(possible_ip) -> list:
    try:
        return [str(ip) for ip in ipaddress.IPv4Network(possible_ip)]
    except ValueError:
        return []
    
def multi_ping(hosts: list, timeout=1):
    try:
        mp = MultiPing(hosts)
        mp.send()
        responses, no_responses = mp.receive(timeout)
        results = {"success": [], "fail": no_responses}
        for addr in responses:
            results["success"].append(addr)
        return results
    except:
        click.secho(f"ERROR: Cannot attempt to ping {hosts}. Make sure you're running as sudo!", fg='yellow')
        return {"success": [], "fail": []}

def can_resolve_domain(domain) -> bool:
    try:
        socket.gethostbyname(domain)
        return True
    except:
        return False