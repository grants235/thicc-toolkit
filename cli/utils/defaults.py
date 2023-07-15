# Default JSON
INITIAL_STATE = {
    "project": None,
    "version": None,
    "state_info": {
        "selected_host": None,
        "automated_enumeration": False
    }
}

DEFAULT_TOOL_CONFIG = {
    "port_scanning": {
        "rustscan": {
            "pritority": 1,
            "flags": " -a ",
            "binary_path": None
        },
        "nmap": {
            "priority": 50,
            "flags": " -sC -sV -p- -Pn ",
            "binary_path": None
        }
    },
    "web_fuzzing": {
        "gobuster": {
            "priority": 1, 
            "flags": None,
            "binary_path": None
        }
    }
}

DEFAULT_SCOPE = {
    "include": [],
    "exclude": []
}

DEFAULT_HOSTS = {
    "include": [],
    "exclude": []
}