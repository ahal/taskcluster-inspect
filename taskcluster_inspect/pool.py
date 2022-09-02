from collections import defaultdict

import taskcluster
from taskcluster.exceptions import TaskclusterRestFailure

queue = taskcluster.Queue(taskcluster.optionsFromEnvironment())
wm = taskcluster.WorkerManager(taskcluster.optionsFromEnvironment())


def get_pools(only_pools=None):
    pools = wm.listWorkerPools()["workerPools"]
    return [p for p in pools if not only_pools or p["workerPoolId"] in only_pools]


def get_images(**pool_args):
    pools_by_image = defaultdict(set)
    for pool in get_pools(**pool_args):
        if not pool["config"]:
            continue

        images = set()
        for launch_config in pool["config"]["launchConfigs"]:
            if pool["providerId"] == "aws":
                images.add(launch_config["launchConfig"]["ImageId"])

            elif pool["providerId"].endswith("gcp"):
                for launch_config in pool["config"]["launchConfigs"]:
                    for disk in launch_config["disks"]:
                        if not disk.get("boot"):
                            continue
                        images.add(disk["initializeParams"]["sourceImage"])

        for image in images:
            pools_by_image[image].add(pool["workerPoolId"])

    return pools_by_image


def get_workers(state=None, **pool_args):
    pools = [p["workerPoolId"] for p in get_pools(**pool_args)]
    workers = []

    for pool in pools:
        continuation = None
        while True:
            response = wm.listWorkersForWorkerPool(pool, continuationToken=continuation)
            assert response

            _workers = response["workers"]
            continuation = response.get("continuationToken")
            if not continuation:
                break
        workers.extend(_workers)

    return sorted(
        [w for w in workers if not state or w["state"] == state],
        key=lambda w: w["workerPoolId"],
    )


def get_worker_tasks(worker: dict):
    """Get most recent tasks (up to 20) for each worker in a specified pool.

    Args:
        worker (dict): A worker definition.

    Returns:
        list: A list of taskId's.
    """
    provisioner, worker_type = worker["workerPoolId"].split("/")

    tasks = queue.getWorker(
        provisioner, worker_type, worker["workerGroup"], worker["workerId"]
    )["recentTasks"]
    return [t["taskId"] for t in tasks]
