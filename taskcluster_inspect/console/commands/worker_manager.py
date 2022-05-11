import re

import petl as etl
from cleo import Command
from tabulate import tabulate

from taskcluster_inspect.pool import list_pools


class ListPoolsCommand(Command):
    """
    Display available pools.

    pools
        {--filter= : Only display pools that match the given regular expression.}
    """

    def handle(self):
        pattern = self.option("filter")

        pools = etl.fromdicts(list_pools())
        keys_to_remove = [
            "config",
            "created",
            "description",
            "emailOnError",
            "owner",
            "requestedCapacity",
            "stoppingCapacity",
            "stoppingCount",
            "stoppedCount",
            "stoppedCapacity",
        ]
        pools = etl.cutout(pools, *keys_to_remove)
        if pattern:
            pools = etl.select(pools, lambda row: re.search(pattern, row.workerPoolId))

        print(tabulate(pools, headers="firstrow"))


class WorkerManagerCommands(Command):
    """
    Contains commands that operate directly on worker-manager.

    wm
    """

    commands = [ListPoolsCommand()]

    def handle(self):
        return self.call("help", self._config.name)
