# todo-extractor

Extracts TODO comments from code.

The purpose of this project is to serve as an example of going from a script to a full-fledged project and to be used with the presentation [Modern Python development](https://github.com/vikahl/modern-python-development) at [Omegapoints conference OpKoKo 19.2](https://opkoko.omegapoint.se).

It might be turned into something useful, but currently it's main purpose is to give examples to the presentation.

## Usage

Run it from the command line like:

```
$ todo_extractor <optional directory>
```

if no directory is specified the current directory will be used.

todo-extrator prints a JSON output with match, line number and filename.


## Development

Development should preferable always be done in a virtualenv.

Installation is done with flit, which needs to be first be installed in the virtualenv (`pip3 install flit`).

The package can be installed in development mode with

```
flit install --symlink
```

or on Windows

```
flit install --pth
```

This will install the package in editable mode and also install the dev-dependencies.

## Testing

Testing can be done with pytest: `pytest --cov=todo_extractor` which will also measure test coverage.

To test the installed package, use tox (`tox`). This will test the installed package on all supported Python versions.
