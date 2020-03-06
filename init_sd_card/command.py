from utils.config import load_config

from dt_shell import DTCommandAbs, DTShell 
from .ente._command import command as ente
from .daffy._command import command as daffy

class DTCommand(DTCommandAbs):
    help = "Sets the benchmark version to the correct versiong"

    @staticmethod
    def command(shell: DTShell, args):
        config = load_config()
        
        print(config)
        
        benchmark_version = config["benchmark_version"]
        if benchmark_version == 'ente':
            ente(shell, args)
        elif benchmark_version == 'daffy':
            daffy(shell, args)
        else:
            print("error")
