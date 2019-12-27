import argparse

import os
import docker
from dt_shell import DTCommandAbs, dtslogger
from utils.docker_utils import check_docker_environment, remove_if_running, pull_if_not_exist
from utils.cli_utils import start_command_in_subprocess

usage = """

## Basic usage

    Runs a virtual Raspberry Pi with a virtual SD card initialized using `dts init_sd_card`.

    To find out more, use `dts duckiebot simulate -h`.

        $ dts duckiebot simulate --disk [IMG_FILE]

"""


class InvalidUserInput(Exception):
    pass


from dt_shell import DTShell


class DTCommand(DTCommandAbs):
    @staticmethod
    def command(shell: DTShell, args):
        prog = "dts duckiebot demo"
        parser = argparse.ArgumentParser(prog=prog, usage=usage)

        parser.add_argument(
            "--disk", '-f',
            dest="disk",
            required=True,
            help="Path to a virtual SD card (.img file)",
        )

        parsed = parser.parse_args(args)

        parsed.disk = os.path.abspath(parsed.disk)
        if not os.path.exists(parsed.disk):
            dtslogger.error(f'The disk file "{parsed.disk}" does not exist.')
            exit(1)

        client = check_docker_environment()
        container_name = "dt_simulated_duckiebot"
        remove_if_running(client, container_name)

        simulator_image = "lukechilds/dockerpi:vm"

        pull_if_not_exist(client, simulator_image)

        cmd = ['docker', 'run', '-it', '--rm', '-v', f'{parsed.disk}:/sdcard/filesystem.img', '--name', container_name, simulator_image]
        start_command_in_subprocess(cmd, shell=False)
