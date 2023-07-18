import json
import click
from concurrent.futures import ThreadPoolExecutor
from functools import partial


class StateManager(object):

    def __init__(self, project, threads=10) -> None:
        self.project = project
        self.threads = threads
        self.thread_pool = ThreadPoolExecutor(threads)
        self.queue_state = {"running": [], "succeeded": [], "failed": []}


    def push_to_queue(self, func, args, custom_callback, name):
        click.secho(f"Process running: {name}", dim=True)
        self.queue_state["running"].append(name)
        future = self.thread_pool.submit(func, args)
        future.add_done_callback(partial(self.main_callback, custom_callback, name))

    def main_callback(self, custom_callback, name, fut):
        self.queue_state["running"].remove(name)
        if self.future_succeeded(fut):
            click.secho(f"\nProcess succeeded: {name}", dim=True)
            self.queue_state["succeeded"].append(name)
        else:
            click.secho(f"\nProcess failed: {name}", fg='yellow')
            self.queue_state["failed"].append(name)
        custom_callback(self, fut, self.future_succeeded(fut))

    def future_succeeded(self, future):
        return future.done() and not future.cancelled() and future.exception() is None

    # state ops
    def get_state(self) -> dict:
        with open(f"{self.project}/.thicc-state.json", "r") as thicc_state:
            state = json.loads(thicc_state.read())
        return state

    def write_state(self, state: dict):
        with open(f"{self.project}/.thicc-state.json", "w") as thicc_state:
            thicc_state.write(json.dumps(state, indent=2))

    # scope ops
    def get_scope(self) -> dict:
        with open(f"{self.project}/scope.json", "r") as thicc_scope:
            scope = json.loads(thicc_scope.read())
        return scope

    def write_scope(self, scope: dict): 
        with open(f"{self.project}/scope.json", "w") as thicc_scope:
            thicc_scope.write(json.dumps(scope, indent=2))

    # host ops
    def get_hosts(self) -> dict:
        with open(f"{self.project}/.hosts.json", "r") as host_file:
            hosts = json.loads(host_file.read())
        return hosts

    def write_hosts(self, hosts):
        with open(f"{self.project}/.hosts.json", "w") as host_file:
            host_file.write(json.dumps(hosts, indent=2))
