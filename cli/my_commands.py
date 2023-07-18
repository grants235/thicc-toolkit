from .commands import scope
from .commands import hosts
from .commands import queue
from .commands import enum_subdomain

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

    'queue': {
        'meta': 'Queue is used to monitor the status of threaded processes',
        'commands': {
            'list': {
                'meta': 'List the state of the queue',
                'commands': {
                    'all': {
                        'meta': 'View all the processes',
                        'exec': queue.list
                    },
                    'running': {
                        'meta': 'View the running processes',
                        'exec': queue.list_running
                    }, 
                    'succeeded': {
                        'meta': 'View the succeeded processes',
                        'exec': queue.list_succeeded
                    },
                    'failed': {
                        'meta': 'View the failed processes',
                        'exec': queue.list_failed
                    }
                }
            }
        }
    },

    'enum': {
        'meta': 'Enumerate hosts within your scope',
        'commands': {
            'subdomains': {
                'meta': 'Find more subdomains for domains with wildcards in the project scope',
                'commands': {
                    'all-tools': {
                        'meta': '(Recommended) Run all subdomain enumeration tools loaded and get unique results',
                        'exec': enum_subdomain.all
                    },
                    'sublist3r': {
                        'meta': 'Run Sublist3r with the configured parameters in your configuration',
                        'exec': enum_subdomain.sublister
                    }
                }
            }
        }
    },

    '!': {
        'meta': 'Execute an Operating System command',
        'exec': None,  # handled in the Repl class itself
    }
}