# taskcluster-inspect

A command line utility for inspecting the state of Taskcluster.

## Installation

It's recommended to use [pipx][0] to install:
```
pipx install taskcluster-inspect
```

## Usage

```
tc-inspect --help
```

### Examples

* List available worker pools:
```
$ tc-inspect wm pools
```

* List running workers for a pool with id `gecko-t/t-linux-large`:
```
$ tc-inspect pool list gecko-t/t-linux-large
```

* List running tasks for a pool with id `gecko-t/t-linux-metal`:
```
$ tc-inspect pool running gecko-t/t-linux-metal
```

[0]: https://pypa.github.io/pipx/
