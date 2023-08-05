"""Nexus 3 CLI.

Usage:
  nexus3 --help  # run this to see full list of commands/subcommands
  nexus3 --version
  nexus3 login
  nexus3 (list|ls) <repository_path>
  nexus3 (upload|up) <from_src> <to_repository> [--flatten] [--norecurse]
  nexus3 (download|dl) <from_repository> <to_dst> [--flatten] [--nocache]
  nexus3 (delete|del) <repository_path>
  nexus3 <subcommand> [<arguments>...]

Options:
  -h --help             This screen. For help with sub-commands, run
                        `nexus3 <subcommand> -h`
  --version             Show the Nexus3 CLI version and exit
  --flatten             Flatten directory structure on `nexus3` transfers
                        [default: False]
  --nocache             Force download even if local copy is up-to-date
                        [default: False]
  --norecurse           Don't process subdirectories on `nexus3 up` transfers
                        [default: False]

Commands:
  login         Test login and save credentials to ~/.nexus-cli
  list          List all files within a path in the repository
  upload        Upload file(s) to designated repository
  download      Download an artefact or a directory to local file system
  delete        Delete artefact(s) from repository

Sub-commands:
  cleanup_policy  Cleanup Policy management.
  repository      Repository management.
  script          Script management.
"""
import pkg_resources
import sys
from docopt import docopt, DocoptExit

from nexuscli import exception
from nexuscli.cli import util


def _is_root_command(maybe):
    if maybe.startswith('-') or maybe.startswith('<'):
        return False
    return True


def _find_root_command(arguments):
    for command, value in arguments.items():
        if _is_root_command(command):
            if value is True:
                return f'cmd_{command}'

    # docopt shouldn't allow this to happen
    raise NotImplementedError(f'Command not found in arguments: {arguments}')


def _run_root_commands(arguments):
    # root commands are handled by methods named `root_commands.cmd_COMMAND`,
    # where COMMAND is the first argument given by the user
    from nexuscli.cli import root_commands
    command_method = getattr(root_commands, _find_root_command(arguments))

    # don't show "missing config" error when the user is creating a config
    client = None
    if not arguments['login']:
        client = util.get_client()

    return command_method(client, arguments)


def _run_subcommand(arguments, subcommand):
    # subcommands are handled by methods named `subcommand_MODULE.cmd_COMMAND`,
    # where MODULE is subcommand name and COMMAND is the first argument given
    # by the user
    from nexuscli.cli import (subcommand_cleanup_policy,
                              subcommand_repository,
                              subcommand_script)

    argv = [arguments['<subcommand>']] + arguments['<arguments>']

    try:
        subcommand_module = globals()[f'subcommand_{subcommand}']
        subcommand_method = getattr(subcommand_module, 'main')
    except KeyError:
        print(__doc__)
        sys.exit(exception.CliReturnCode.INVALID_SUBCOMMAND.value)

    try:
        return subcommand_method(argv)
    except DocoptExit:
        # Show help for the subcommand. The exception instance also has the
        # the help but we can't use it because it won't have the `-h` details.
        # This is because `-h` is handled by the first call to docopt, in main.
        # FIXME: docopt is now more work than it's worth it
        print(subcommand_module.__doc__)
        return exception.CliReturnCode.SUBCOMMAND_ERROR.value


def main(argv=None):
    """Entrypoint for the setuptools CLI console script"""
    try:
        arguments = docopt(__doc__, argv=argv)
    except DocoptExit:
        # FIXME: it's time to ditch docopt for something that supports
        #   subcommands natively
        arguments = docopt(__doc__, argv=argv, options_first=True)

    if arguments.get('--version'):
        print(pkg_resources.get_distribution('nexus3-cli').version)
        return 0

    maybe_subcommand = arguments.get('<subcommand>')

    exit_code = exception.CliReturnCode.UNKNOWN_ERROR.value
    try:
        # "root" commands (ie not a subcommand)
        if maybe_subcommand is None:
            exit_code = _run_root_commands(arguments)
        else:
            # subcommands
            exit_code = _run_subcommand(arguments, maybe_subcommand)

    except exception.NexusClientBaseError as e:
        print(f'{e.cli_return_code.name}: {e}')
        exit_code = e.cli_return_code.value

    finally:
        return exit_code
