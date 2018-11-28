import argparse
import getpass
import os
import threading
import time

from dt_shell import DTCommandAbs, dtslogger
from dt_shell.env_checks import check_docker_environment

from utils.docker_utils import push_image_to_duckiebot, run_image_on_duckiebot, run_image_on_localhost, record_bag, \
    start_slimremote_duckiebot_container, start_rqt_image_view, RPI_ROS_KINETIC_ROSCORE, stop_container, \
    continuously_monitor, get_remote_client
from utils.networking_utils import get_duckiebot_ip

usage = """

## Basic usage

    Evaluates the current submission on the Duckiebot:

        $ dts duckiebot evaluate

"""


class DTCommand(DTCommandAbs):

    @staticmethod
    def command(shell, args):
        prog = 'dts duckiebot evaluate'
        parser = argparse.ArgumentParser(prog=prog, usage=usage)

        group = parser.add_argument_group('Basic')

        parser.add_argument('hostname', default=None,
                            help="Name of the Duckiebot on which to perform evaluation")

        group.add_argument('--image', help="Image to evaluate",
                           default="duckietown/challenge-aido1_lf1-template-ros:v3")

        group.add_argument('--duration', help="Duration of time to run evaluation", default=30)

        group.add_argument('--remotely', action='store_true', default=False,
                           help="Run the image on the laptop without pushing to Duckiebot")

        parsed = parser.parse_args(args)

        run_image_on_duckiebot(RPI_ROS_KINETIC_ROSCORE, parsed.hostname)

        dtslogger.info('Waiting a few moments for roscore to start up...')
        time.sleep(5)

        slimremote_conatiner = start_slimremote_duckiebot_container(parsed.hostname)

        dtslogger.info('Waiting a few moments for slimremote to start up...')
        time.sleep(5)

        start_rqt_image_view(parsed.hostname)

        bag_container = record_bag(parsed.hostname, parsed.duration)
        env = {'username': 'root',
               'challenge_step_name': 'step1-simulation',
               'uid': 0,
               'challenge_name': 'aido1_LF1_r3-v3'}

        volumes = setup_expected_volumes()

        if parsed.remotely:
            evaluate_remotely(parsed.hostname, parsed.image, env, volumes)
        else:
            evaluate_locally(parsed.hostname, parsed.image, env, volumes)

        stop_container(bag_container)
        stop_container(slimremote_conatiner)


def setup_expected_volumes():
    tmpdir = '/tmp'

    USERNAME = getpass.getuser()
    dir_home_guest = os.path.expanduser('~')
    dir_fake_home_host = os.path.join(tmpdir, 'fake-%s-home' % USERNAME)
    if not os.path.exists(dir_fake_home_host):
        os.makedirs(dir_fake_home_host)

    dir_fake_home_guest = dir_home_guest
    dir_dtshell_host = os.path.join(dir_home_guest, '.dt-shell')
    dir_dtshell_guest = os.path.join(dir_fake_home_guest, '.dt-shell')
    dir_tmpdir_host = '/tmp'
    dir_tmpdir_guest = '/tmp'

    return {'/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'},
            os.getcwd(): {'bind': os.getcwd(), 'mode': 'ro'},
            dir_tmpdir_host: {'bind': dir_tmpdir_guest, 'mode': 'rw'},
            dir_dtshell_host: {'bind': dir_dtshell_guest, 'mode': 'ro'},
            dir_fake_home_host: {'bind': dir_fake_home_guest, 'mode': 'rw'},
            '/etc/group': {'bind': '/etc/group', 'mode': 'ro'}}


# Runs everything on the Duckiebot

def evaluate_locally(duckiebot_name, image_name, env, volumes):
    dtslogger.info("Running %s on %s" % (image_name, duckiebot_name))
    push_image_to_duckiebot(image_name, duckiebot_name)
    evaluation_container = run_image_on_duckiebot(image_name, duckiebot_name, env, volumes)
    duckiebot_ip = get_duckiebot_ip(duckiebot_name)
    duckiebot_client = get_remote_client(duckiebot_ip)
    monitor_thread = threading.Thread(target=continuously_monitor, args=(duckiebot_client, evaluation_container.name))
    monitor_thread.start()
    dtslogger.info("Letting %s run for 30s..." % image_name)
    time.sleep(30)
    stop_container(evaluation_container)


# Sends actions over the local network

def evaluate_remotely(duckiebot_name, image_name, env, volumes):
    dtslogger.info("Running %s on localhost" % image_name)
    evaluation_container = run_image_on_localhost(image_name, duckiebot_name, env, volumes)
    local_client = check_docker_environment()
    monitor_thread = threading.Thread(target=continuously_monitor, args=(local_client, evaluation_container.name))
    monitor_thread.start()
    dtslogger.info("Letting %s run for 30s..." % image_name)
    time.sleep(30)
    stop_container(evaluation_container)
