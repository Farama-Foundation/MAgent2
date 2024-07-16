import magent2
from magent2.environments import (
    adversarial_pursuit_v4,
    battle_v4,
    battlefield_v5,
    combined_arms_v6,
    gather_v5,
    magent_env,
    tiger_deer_v4
)

def test_version():
    assert magent2.__version__ is not None, "Version should not be None"
    assert isinstance(magent2.__version__, str), "Version should be a string"

def test_import_environments():
    assert adversarial_pursuit_v4 is not None, "adversarial_pursuit_v4 should be importable"
    assert battle_v4 is not None, "battle_v4 should be importable"
    assert battlefield_v5 is not None, "battlefield_v5 should be importable"
    assert combined_arms_v6 is not None, "combined_arms_v6 should be importable"
    assert gather_v5 is not None, "gather_v5 should be importable"
    assert magent_env is not None, "magent_env should be importable"
    assert tiger_deer_v4 is not None, "tiger_deer_v4 should be importable"
