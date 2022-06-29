import taskcluster

queue = taskcluster.Queue(taskcluster.optionsFromEnvironment())


def get_status(task_id):
    return queue.status(task_id)["status"]
