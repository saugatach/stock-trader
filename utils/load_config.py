import os
import set_root
import yaml


def load_config(project_root, verbose=False):
    config_path = os.path.join(project_root, "config", "config.yaml")

    if verbose:
        print(f"Config path: {config_path}")

    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    return config
