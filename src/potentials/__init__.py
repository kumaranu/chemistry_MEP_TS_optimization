import os
import yaml

from .wolfe_schlegel import wolfe_schlegel
from .muller_brown import muller_brown
from .constant import Constant

potential_dict = {
    "wolfe_schlegel" : wolfe_schlegel,
    "muller_brown" : muller_brown,
    "constant" : Constant
}

def import_potential_config(
        name,
        tag="",
        dir="./src/potentials/configs/",
        is_expected=False
    ):
    filename = name
    filename += f"_{tag}.yaml" if tag != "" else ".yaml"
    address = os.path.join(dir, filename)

    if os.path.exists(address):
        with open(address, 'r') as file:
            loaded_yaml = yaml.safe_load(file)
        return loaded_yaml
    elif is_expected:
        raise ImportError(f"Cannot find required file {address}")
    else:
        ImportWarning(f"Cannot find file {address}, running without it")
        return {}

def get_potential(
        potential,
        tag="",
        config_dir="./src/potentials/configs/",
        expect_config=False
    ):
    assert potential.lower() in potential_dict
    config_filename = potential
    config_filename += f"_{tag}.yaml" if tag != "" else ".yaml"
    print(potential)
    config = import_potential_config(
        potential, tag, dir=config_dir, is_expected=expect_config
    )
    return potential_dict[potential](**config)