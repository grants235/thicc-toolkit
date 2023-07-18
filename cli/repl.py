import logging
import os
import click
import json
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import FuzzyCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style

from .my_commands import COMMANDS
from .completer import CommandCompleter
from .utils import helpers
from .utils import defaults
from . import state_manager


class Repl(object):
    """
        The exploration REPL for objection
    """

    def __init__(self, project_arg, threads=10) -> None:
        self.version = "0.0.1"

        self.completer = FuzzyCompleter(CommandCompleter())
        self.commands_repository = COMMANDS
        self.project = self.project_init(project_arg)
        self.state = state_manager.StateManager(self.project, threads)

    def get_prompt_session(self) -> PromptSession:
        """
            Starts a new prompt session.

            :return:
        """

        return PromptSession(
            history=FileHistory(os.path.expanduser(f"{self.project}/.thicc-history")),
            completer=self.completer,
            style=self.get_prompt_style(),
            auto_suggest=AutoSuggestFromHistory(),
            reserve_space_for_menu=4,
            complete_in_thread=True,
        )

    @staticmethod
    def get_prompt_style() -> Style:
        """
            Get the style to use for our prompt

            :return:
        """

        return Style.from_dict({
            # completions menu
            'completion-menu.completion.current': 'bg:#00aaaa #000000',
            'completion-menu.completion': 'bg:#008888 #ffffff',

            # fuzzy match outside
            'completion-menu.completion fuzzymatch.outside': 'fg:#000000',

            # Prompt.
            'applicationname': '#007cff',
            'project': '#717171',
            'host': '#00ff48',
            'prompt': '#717171'
        })

    def get_prompt_message(self) -> list:

        state = self.state.get_state()
        if state["state_info"]["active_host"] is not None:
            state_str = state["state_info"]["active_host"]
        else:
            state_str = ""

        return [
            ('class:applicationname', 'thicc-console '),
            ('class:project', self.project),
            ('class:host', f' [{state_str}]'),
            ('class:prompt', ' > ')
        ]

    def run_command(self, document: str) -> None:

        logging.info(document)
        if document.strip() == '':
            return

        # handle os commands
        if document.strip().startswith('!'):

            # strip the leading !
            os_cmd = document[1:]

            click.secho('Running OS command: {0}\n'.format(os_cmd), dim=True)
            o = os.system(os_cmd)
            return

        # a normal command is to be run, extract the tokens and
        # find which method we should be calling
        tokens = helpers.get_tokens(document)

        # check if we should be presenting help instead of executing
        # a command. this is indicated by the fact that the command
        # starts with the word 'help'
        if len(tokens) > 0 and 'help' == tokens[0]:

            # skip the 'help' entry from the tokens list so that
            # the following method can find the correct help
            tokens.remove('help')
            command_help = self._find_command_help(tokens)

            if not command_help:
                click.secho(('No help found for: {0}. Either the command '
                             'does not exist or contains subcommands with help.'
                             ).format(' '.join(tokens)), fg='yellow')
                return

            # output the help and leave
            click.secho(command_help, fg='blue', bold=True)
            return

        # find an execution method to run
        token_matches, exec_method = self._find_command_exec_method(tokens)

        if exec_method is None:
            click.secho('Unknown or ambiguous command: `{0}`. Try `help {0}`.'.format(document), fg='yellow')
            return

        # strip the command matching tokens and leave
        # the rest as arguments
        arguments = tokens[token_matches:]

        # run the method for the command itself!
        exec_method(self.state, arguments)

        # app_state.add_command_to_history(command=document)

    def _find_command_exec_method(self, tokens: list) -> tuple:
        """
            Attempt to find the actual python method to run
            for the command tokens we have.

            This is done by 'walking' the command dictionary,
            looking for the deepest 'exec' method definition. We are
            interested in the number of tokens walked as well, so
            that the calling command can know how many tokens to
            strip, sending the rest as arguments to the exec method.

            :param tokens:
            :return:
        """

        # start with all of the commands we have
        dict_to_walk = self.commands_repository

        # ... and an empty method to execute
        exec_method = None

        # keep count of the number of tokens
        # used in this walk. this will help indicate to
        # the caller how many tokens should be stripped to
        # get to the arguments for the command
        walked_tokens = 0

        for token in tokens:

            # increment the walked tokens
            walked_tokens += 1

            # check if the token matches a command
            if token in dict_to_walk:

                # matched a dict for the token we have. we need
                # to have *all* of the tokens match a nested dict
                # so that we can extract the final 'exec' key.
                # if we encounter a key that does not have nested commands,
                # chances are we are where we need to be to exec a command.
                if 'commands' not in dict_to_walk[token]:

                    if 'exec' in dict_to_walk[token]:
                        exec_method = dict_to_walk[token]['exec']
                        break

                else:
                    dict_to_walk = dict_to_walk[token]['commands']

            # stop if there is nothing that matches
            else:
                break

        return walked_tokens, exec_method

    def _find_command_help(self, tokens: list) -> str:
        """
            Attempt to find help for a command.

            Just like how the _find_command_exec_method works, this
            method also walks the command dictionary, searching for
            the deepest key. The tokens that match form part of a
            new list, later joined together to pickup the correct
            help.txt.

            :param tokens:
            :return:
        """

        # start with all of the commands we have
        dict_to_walk = self.commands_repository
        helpfile_name = []
        user_help = ''

        for token in tokens:

            # check if the token matches a command
            if token in dict_to_walk:

                # add this token to the helpfile
                helpfile_name.append(token)

                # if there are subcommands, continue with the walk
                if 'commands' in dict_to_walk[token]:
                    dict_to_walk = dict_to_walk[token]['commands']

            # stop if we don't have a token that matches anything
            else:
                break

        # once we have the help, load its .txt contents
        if len(helpfile_name) > 0:

            help_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                     'helpfiles', '.'.join(helpfile_name) + '.txt')

            # no helpfile... warn.
            if not os.path.exists(help_file):
                click.secho('Unable to find helpfile {0}'.format(' '.join(helpfile_name)), dim=True)

                return user_help

            # read the helpfile
            with open(help_file, 'r') as f:
                user_help = f.read()

        return user_help
    
    def project_init(self, project):
    
        if project is not None:
            if os.path.exists(project):
                click.secho('Loading existing project', fg='white', dim=True)
            else:
                click.secho('Initializing a new project', fg='white', dim=True)
                os.mkdir(project)
                with open(f"{project}/.thicc-state.json", "w") as state_file:
                    thicc_state = defaults.INITIAL_STATE
                    thicc_state["project"] = project
                    thicc_state["version"] = self.version
                    state_file.write(json.dumps(thicc_state, indent=2))
                with open(f"{project}/thicc-config.json", "w") as config_file:
                    thicc_config = defaults.DEFAULT_TOOL_CONFIG
                    config_file.write(json.dumps(thicc_config, indent=2))
                with open(f"{project}/scope.json", "w") as scope_file:
                    thicc_scope = defaults.DEFAULT_SCOPE
                    scope_file.write(json.dumps(thicc_scope, indent=2))
                with open(f"{project}/.hosts.json", "w") as host_file:
                    hosts = defaults.DEFAULT_HOSTS
                    host_file.write(json.dumps(hosts, indent=2))
                click.secho('Succesfully created a new project', fg='white', dim=True)

            return project

        else:
            click.secho('Error! Project arguement is required. Use the -h flag in order to get help', fg='white', dim=True)
            sys.exit()


    def run(self) -> None:
        helpers.clear()

        banner = ("""
 _______________         ____                  _____           _ _    _ _   
|          |    |       (____)                |_   _|         | | |  (_) |  
|___    ___|    |______  ____  ______ ______    | | ___   ___ | | | ___| |_ 
   |    |  |           \|    |/     |/     |    | |/ _ \ / _ \| | |/ / | __|
   |    |  |     __     |    |    __|    __|    | | (_) | (_) | | | <| | |_|
   |    |  |    |  |    |    |   (__|   (__     \_/\___/ \___/|_|_|\_\_|\__|
   |    |  |    |  |    |    |      |      |       The hacker's information 
   \____/  |____|  |____|____|\______\_____|    collection and collaboration
            created by @grants235                         toolkit                            
""")

        click.secho(banner, bold=True)
        self.session = self.get_prompt_session()
        click.secho('[tab] for command suggestions', fg='white', dim=True)

        while True:

            try:

                document = self.session.prompt(self.get_prompt_message())

                if document.strip() in ('quit', 'exit', 'bye', 'quit()', '.quit', 'exit()'):
                    click.secho('Exiting...', dim=True)
                    break

                if document.strip() in ('clear', 'cls'):
                    helpers.clear()
                    continue

                self.run_command(document)

            except KeyboardInterrupt:
                pass
