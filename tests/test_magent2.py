import importlib

from pettingzoo import aec_registry, make, parallel_registry
from pettingzoo.utils.env import AECEnv, ParallelEnv

import magent2


ENVIRONMENT_IDS = (
    "adversarial_pursuit-v4",
    "battle-v4",
    "battlefield-v5",
    "combined_arms-v6",
    "gather-v5",
    "tiger_deer-v4",
)


def test_version():
    assert hasattr(magent2, "__version__"), "Version should not be None"
    assert isinstance(magent2.__version__, str), "Version should be a string"


def test_import_environments():
    envs = [
        "adversarial_pursuit_v4",
        "battle_v4",
        "battlefield_v5",
        "combined_arms_v6",
        "gather_v5",
        "magent_env",
        "tiger_deer_v4",
    ]

    for env in envs:
        try:
            # Dynamically import the environment module
            importlib.import_module(f"magent2.environments.{env}")
        except ImportError:
            assert False, f"{env} should be importable"


def test_environments_registered():
    for environment_id in ENVIRONMENT_IDS:
        namespaced_id = f"magent2/{environment_id}"
        assert namespaced_id in aec_registry
        assert namespaced_id in parallel_registry


def test_make_environments():
    aec_env = make("aec", "magent2/battle-v4", map_size=16)
    parallel_env = make("parallel", "magent2/battle-v4", map_size=16)

    assert isinstance(aec_env, AECEnv)
    assert isinstance(parallel_env, ParallelEnv)

    aec_env.close()
    parallel_env.close()
