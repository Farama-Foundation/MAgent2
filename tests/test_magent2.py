import magent2
import pettingzoo
import importlib

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
        module = importlib.import_module(f"magent2.environments.{env}")
    except ImportError:
        assert False, f"{env} should be importable"


def test_version():
    assert hasattr(magent2, '__version__'), "Version should not be None"
    assert isinstance(magent2.__version__, str), "Version should be a string"


def test_import_environments():
    # These assert statements check if the imported modules are not None
    assert importlib.import_module("magent2.environments.adversarial_pursuit_v4") is not None, "adversarial_pursuit_v4 should be importable"
    assert importlib.import_module("magent2.environments.battle_v4") is not None, "battle_v4 should be importable"
    assert importlib.import_module("magent2.environments.battlefield_v5") is not None, "battlefield_v5 should be importable"
    assert importlib.import_module("magent2.environments.combined_arms_v6") is not None, "combined_arms_v6 should be importable"
    assert importlib.import_module("magent2.environments.gather_v5") is not None, "gather_v5 should be importable"
    assert importlib.import_module("magent2.environments.magent_env") is not None, "magent_env should be importable"
    assert importlib.import_module("magent2.environments.tiger_deer_v4") is not None, "tiger_deer_v4 should be importable"
