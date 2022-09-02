import json
import re

import petl as etl
from cleo import Command
from tabulate import tabulate

from taskcluster_inspect.pool import get_images, get_pools


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


class ListImagesCommand(Command):
    """
    Display images and the pools associated with them.

    images
        {--filter= : Only display images associated with pools matching the given regular expression.}
        {--json : Display images in JSON format.}
    """
    def handle(self):
        images = get_images()

        pattern = self.option("filter")
        if pattern:
            for k, v in images.items():
                images[k] = {pool for pool in v if re.search(pattern, pool)}

        images = {k: sorted(images[k]) for k in sorted(images.keys()) if images[k]}
        if self.option("json"):
            print(json.dumps(images, indent=2))
            return

        images = [(k, "\n".join(sorted(images[k]))) for k in sorted(images)]
        print(tabulate(images, headers=["Image", "Pools"]))


class WorkerManagerCommands(Command):
    """
    Contains commands that operate directly on worker-manager.

    wm
    """

    commands = [ListPoolsCommand(), ListImagesCommand()]

    def handle(self):
        return self.call("help", self._config.name)
