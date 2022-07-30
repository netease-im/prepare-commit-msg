prepare-commit-msg
==================

Yet another tool for the `prepare-commit-msg` git hook. To use with **pre-commit**

For pre-commit: see https://github.com/pre-commit/pre-commit

## What's all about

In many projects some sort of ticket system is used. The commit messages are used for updating the status of the ticket by "linking" the ticket name, which it is nothing more than mentioning the ticket name, in the commit message.

This allows for using a jinja2 template for formatting your commit message.

You can configure this with the following commandline options:
- `-t` / `--template ` - absolute path to the template. Default value:
  name of bundled template: `prepare_commit_msg_append.j2` file
- `-b` / `--branch` - may be specified multiple times to exclude branches
  from formatting the commit message. Default values: `main, master`
- `-p` / `--pattern` - may be specified multiple times to include branches
  for formatting the commit message. Default value: `(?<=feature/).*`

## Usage

```yaml
# .pre-commit-config.yaml file
default_install_hook_types:
  - pre-commit
  - prepare-commit-msg
repos:
  - repo: https://github.com/davidmpaz/prepare-commit-msg
    rev: v0.0.1
    hooks:
      - id: prepare-commit-msg
        stages: [ prepare-commit-msg ]
        args: [
          -t, prepare_commit_msg_prepend.j2,
          -b, main, -b, master, -b, test, -b develop,
          -p, '(?<=feature/).*', -p, '(?<=release/).*'
        ]
```
