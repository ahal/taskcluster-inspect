import re

import petl as etl
from cleo import Command
from tabulate import tabulate

from taskcluster_inspect.pool import get_pools


class ListPoolsCommand(Command):
    """
    Display available pools.

    pools
        {--filter= : Only display pools that match the given regular expression.}
        {--json : Display pools in JSON format.}
    """

    def handle(self):
        pools = etl.fromdicts(get_pools())
        pattern = self.option("filter")
        if pattern:
            pools = pools.select(lambda row: re.search(pattern, row.workerPoolId))

        if self.option("json"):
            sink = etl.StdoutSource()
            pools = pools.cutout("config")
            pools.tojson(sink, indent=2)
            return

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
        pools = pools.cutout(*keys_to_remove)
        print(tabulate(pools, headers="firstrow"))


class WorkerManagerCommands(Command):
    """
    Contains commands that operate directly on worker-manager.

    wm
    """

    commands = [ListPoolsCommand()]

    def handle(self):
        return self.call("help", self._config.name)
