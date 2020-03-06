from utils.config import load_config

from dt_shell import DTCommandAbs, DTShell 
from .ente._command import command as ente
from .daffy._command import command as daffy
from .master19._command import command as master19

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
        elif benchmark_version == 'master19':
            master19(shell, args)
        elif benchmark_version is None:
            print("benchmark version not set please do so using: \n$ dts benchmark set [daffy, master19, ente] ")
            return
        else:
            print("error unknown benchmark version ")
