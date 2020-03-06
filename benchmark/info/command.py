from utils.config import load_config, save_to_config

from dt_shell import DTCommandAbs, DTShell 

class DTCommand(DTCommandAbs):
    help = "Sets the benchmark version to the correct versiong"

    @staticmethod
    def command(shell: DTShell, args):
        msg = 'this is the current config of the benchmark: \n %s' % load_config()
        print(msg)
