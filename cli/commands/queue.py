import click


def list(state, args):
    list_running(state, args)
    list_succeeded(state, args)
    list_failed(state, args)

def list_running(state, args):
    running = state.queue_state["running"]
    if len(running) != 0:
        click.secho("""Running processes
-----------------""", bold=True)
        for process in running:
            click.secho(process)
    else:
        click.secho("No running processes", dim=True)

def list_succeeded(state, args):
    succeeded = state.queue_state["succeeded"]
    if len(succeeded) != 0:
        click.secho("""Succeeded processes
-------------------""", bold=True)
        for process in succeeded:
            click.secho(process)
    else:
        click.secho("No succeeded processes", dim=True)


def list_failed(state, args):
    failed = state.queue_state["failed"]
    if len(failed) != 0:
        click.secho("""Failed processes
----------------""", bold=True)
        for process in failed:
            click.secho(process)
    else:
        click.secho("No succeeded processes", dim=True)