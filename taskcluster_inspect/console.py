#!/usr/bin/env python
import sys
from argparse import ArgumentParser

from tabulate import tabulate

from taskcluster_inspect.pool import list_workers


def cli(args=sys.argv[1:]):
    parser = ArgumentParser()
    parser.add_argument(
        "--state", default=None, help="Only list workers with the given state."
    )
    parser.add_argument(
        "--pool",
        default=None,
        action="append",
        help="Only list workers with the given state.",
    )
    args = parser.parse_args()
    workers = list_workers(state=args.state, only_pools=args.pool)
    print(tabulate(workers, headers="keys"))


if __name__ == "__main__":
    sys.exit(cli())
