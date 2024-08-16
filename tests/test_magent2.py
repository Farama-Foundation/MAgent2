import importlib

import magent2


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
