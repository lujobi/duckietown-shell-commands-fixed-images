from dt_shell import DTCommandAbs, DTShell


class DTCommand(DTCommandAbs):
    @staticmethod
    def command(shell: DTShell, args):
        print("Bye bye!")
        exit()



"""import argparse
import io
import os
import subprocess

from dt_shell import DTCommandAbs, dtslogger

DEFAULT_ARCH = "arm32v7"
DEFAULT_MACHINE = "unix:///var/run/docker.sock"
SUPPORTED_BENCHMARKS = ["master19","daffy"]

from dt_shell import DTShell




class DTCommand(DTCommandAbs):
    help = "Removes the Docker images relative to the current project"

    @staticmethod
    def command(shell: DTShell, args):
        # configure arguments
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-sv",
            "--set-version",
            default="daffy",
            help="Software Version of benchmark eg. daffy",
        )
        parsed, _ = parser.parse_known_args(args=args)
        # ---
        dtslogger.info("Project workspace: {}".format(parsed.workdir))
        # show info about project
        shell.include.devel.info.command(shell, args)
        
        print(parsed)
"""