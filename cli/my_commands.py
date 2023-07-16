from .commands import scope
from .commands import hosts

COMMANDS = {

    'scope': {
        'meta': 'Define scope for enumeration',
        'commands': {
            'list': {
                'meta': 'List the details of the current scope',
                'exec': scope.list
            },
            'add': {
                'meta': 'Add an IP, Subnet, Domain, or Subdomin to the project scope',
                'commands': {
                    'include': {
                        'meta': 'Include an IP, Subnet, Domain, or Subdomain to the project scope',
                        'exec': scope.add_included
                    },
                    'exclude': {
                        'meta': 'Include an IP, Subnet, Domain, or Subdomain to the project scope',
                        'exec': scope.add_excluded
                    }
                }
            },
            'remove': {
                'meta': 'Remove an IP, Subnet, Domain, or Subdomain from the porject scope',
                'exec': scope.remove
            },
            'clear': {
                'meta': 'Clear the scope',
                'exec': scope.clear
            }
        }
    },
    
    'hosts': {
        'meta': 'Discovered hosts based on the defined scope',
        'commands': {
            'list': {
                'meta': 'List the discovered hosts',
                'exec': hosts.list
            },
            'update': {
                'meta': 'Update the hosts list based on the defined scope',
                'exec': hosts.update
            },
            'clear': {
                'meta': 'Clear the hosts',
                'exec': hosts.clear
            },
            'set-active-host': {
                'meta': 'Set the current active host',
                'exec': hosts.set_active
            }
        }
    },

    '!': {
        'meta': 'Execute an Operating System command',
        'exec': None,  # handled in the Repl class itself
    }
}