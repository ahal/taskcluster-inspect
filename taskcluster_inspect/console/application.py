import sys

from cleo import Application

from .commands.pool import WorkerPoolCommands
from .commands.worker_manager import WorkerManagerCommands


def cli():
    application = Application()
    application.add(WorkerManagerCommands())
    application.add(WorkerPoolCommands())
    application.run()


if __name__ == "__main__":
    sys.exit(cli())
