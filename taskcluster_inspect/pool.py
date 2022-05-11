import taskcluster

wm = taskcluster.WorkerManager(taskcluster.optionsFromEnvironment())


def list_worker_pools(only_pools=None):
    pools = wm.listWorkerPools()["workerPools"]
    return [
        p["workerPoolId"]
        for p in pools
        if not only_pools or p["workerPoolId"] in only_pools
    ]


def list_workers(state=None, **pool_args):
    pools = list_worker_pools(**pool_args)
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
