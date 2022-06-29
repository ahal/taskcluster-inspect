import petl as etl
from cleo import Command
from tabulate import tabulate
from taskcluster.exceptions import TaskclusterRestFailure

from taskcluster_inspect.pool import get_workers, get_worker_tasks
from taskcluster_inspect.task import get_status


class ListWorkersCommand(Command):
    """
    Display workers in the given pool.

    list
        {--state=running : Only list workers with the given state (default:
                           running). Use "all" to list all states.}
    """

    def handle(self):
        pool = self.argument("id")
        state = self.option("state")
        if state == "all":
            state = None
        workers = get_workers(state=state, only_pools=pool)
        print(tabulate(workers, headers="keys"))


class ListRunningTasksCommand(Command):
    """
    Display running tasks by worker in the given pool.

    running
    """

    @classmethod
    def is_running(cls, task):
        return get_status(task)["state"] == "running"

    def handle(self):
        pool = self.argument("id")
        workers = get_workers(state="running", only_pools=pool)

        table = [["Worker", "Capacity", "Running Tasks"]]
        for worker in workers:
            try:
                tasks = get_worker_tasks(worker)
            except TaskclusterRestFailure:
                print(f"warning: error processing worker {worker['workerId']}")
                continue

            num_running = str(len(list(filter(self.is_running, tasks))))
            if num_running == "20":
                num_running = "20+"

            table.append([
                worker["workerId"],
                worker["capacity"],
                num_running,
            ])

        print(tabulate(table, headers="firstrow"))


class WorkerPoolCommands(Command):
    """
    Contains commands that operate on a specific worker pool.

    pool
        {id : Identifier of the worker pool.}
    """

    commands = [ListWorkersCommand(), ListRunningTasksCommand()]

    def handle(self):
        return self.call("help", self._config.name)
