import argparse
import io
import os
from os.path import basename, isfile, isdir, exists, join, getmtime
import json
from os import makedirs
import subprocess

from utils.config import SUPPORTED_BENCHMARKS, load_config, save_to_config

from dt_shell import DTCommandAbs, DTShell 

class DTCommand(DTCommandAbs):
    help = "Sets the benchmark version to the correct versiong"

    @staticmethod
    def command(shell: DTShell, args):
        # configure arguments
        if len(args) == 0:
            msg = 'missing the argument, try one of those %s' % (SUPPORTED_BENCHMARKS)
            shell.sprint(msg)
            return
        if len(args) > 1:
            msg = 'The string "%s" is too many args\n' % (args)
            shell.sprint(msg)
            return
        if args[0] not in SUPPORTED_BENCHMARKS:
            msg = '"%s" is not a supported benchmark \n try one of those %s' % (args[0], SUPPORTED_BENCHMARKS)
            shell.sprint(msg)
            return
        
        save_to_config("benchmark_version",args[0])
        
        msg = 'set benchmark version to %s' % args[0]
        print(msg)
    

            

