import sys

from cleo import Application

from .commands.pool import WorkerPoolCommands


def cli():
    application = Application()
    application.add(WorkerPoolCommands())
    application.run()


if __name__ == "__main__":
    sys.exit(cli())
