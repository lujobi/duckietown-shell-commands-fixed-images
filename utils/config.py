
import os
import json
from os import makedirs
from os.path import basename, dirname, isdir, exists, join

SUPPORTED_BENCHMARKS = ["master19","daffy"]
ROOT = '~/.dt-shell/benchmark'
config_path = os.path.expanduser(ROOT)
config_file = join(config_path, 'config')


def load_config():
    with open(config_file, 'r') as fp:
        try:
            config = json.load(fp)
            return config
        except:
            return None

def save_to_config(key, value):
    if not exists(config_path):
        makedirs(config_path)
    with open(config_file, 'w') as fp:
        config = load_config()
        if config is not None:
            config[key] = value
            json.dump(config, fp)
        else:
            json.dump({key:value}, fp)