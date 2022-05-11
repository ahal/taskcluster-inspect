from cleo import Command
from tabulate import tabulate

from taskcluster_inspect.pool import list_workers


class ListWorkersCommand(Command):
    """
    Display workers in the given pool.

    list
        {--state= : Only list workers with the given state.}
    """

    def handle(self):
        pool = self.argument("id")
        state = self.option("state")
        workers = list_workers(state=state, only_pools=pool)
        print(tabulate(workers, headers="keys"))


class WorkerPoolCommands(Command):
    """
    Contains commands that operate on a specific worker pool.

    pool
        {id : Identifier of the worker pool.}
    """

    commands = [ListWorkersCommand()]

    def handle(self):
        return self.call("help", self._config.name)
