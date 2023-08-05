"""
THIS SOFTWARE IS PROVIDED AS IS
and under GNU General Public License. <https://www.gnu.org/licenses/gpl-3.0.en.html>
USE IT AT YOUR OWN RISK.

PipHyperd cli interface.

The module is published on PyPi <https://pypi.org/project/piphyperd/>.

The code is available on GitLab <https://gitlab.com/hyperd/piphyperd>.
"""

import sys
import argparse
import os

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if not PATH in sys.path:
    sys.path.insert(1, PATH)
    from .piphyperd import PipHyperd
del PATH


def main(python_path=None, command=None):
    """
    This function is called when run as python3 -m ${MODULE}
    Parse any additional arguments and call required module functions.
    """

    if sys.argv:
        # called through CLI
        module_name = __loader__.name.split('.')[0]
        parser = argparse.ArgumentParser(
            prog=module_name,
            description="{} This is my new shiny pip package called".format(
                module_name),
        )

        parser.add_argument('--python_path', action='store', nargs=1, required=False, type=str,
                            default=[os.sys.executable],
                            help="Provide a valid python path")

        parser.add_argument('--command', action='store', nargs=1, required=True, type=str,
                            default=["list"],
                            help="Provide a valid pip command")

        parser.add_argument('--packages', action='store', nargs=1, required=False, type=str,
                            help="Provide a list of packages")

        # argparser provides us a list, even if only one argument
        args = parser.parse_args(sys.argv[1:])

        # check for alternative python path used to initialize the
        if args.python_path:
            if isinstance(args.python_path, list) and isinstance(args.python_path[0], str):
                python_path = args.python_path[0]

        # check for alternative python path
        if args.command:
            if isinstance(args.command, list) and isinstance(args.command[0], str):
                command = args.command[0]

        command_args = list()
        if args.packages:
            if isinstance(args.packages, list) and isinstance(args.packages[0], str):
                command_args.clear()
                for package in args.packages[0].split(','):
                    command_args.append(package)

        switcher = {
            "freeze": freeze,
            "list": list_packages,
            "check": check,
            "install": install,
            "uninstall": uninstall,
            "download": download,
        }
        # "list": lambda: 'nope'
        func = switcher.get(command, lambda: 'Invalid pip command')

    instance = PipHyperd(python_path=python_path)

    pip_command, _, exit_code = func(instance, command_args)

    sys.stdout.write(pip_command + "\n")
    return exit_code


def freeze(instance):
    """ return pip freeze """
    return instance.freeze()


def list_packages(instance):
    """ return pip list """
    return instance.list()


def check(instance):
    """ return pip check """
    return instance.check()


def install(instance, packages):
    """ return pip install ${packages} """
    return instance.install(*packages)


def uninstall(instance, packages):
    """ return pip uninstall ${packages} """
    return instance.uninstall(*packages)


def download(instance, packages):
    """ return pip download ${packages} """
    return instance.download(*packages)
