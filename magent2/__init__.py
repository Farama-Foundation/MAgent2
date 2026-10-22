from pettingzoo import register as _register

from magent2 import gridworld, utility
from magent2.render import Renderer


# some alias
GridWorld = gridworld.GridWorld

__version__ = "0.3.5"


_ENVIRONMENTS = (
    "adversarial_pursuit-v4",
    "battle-v4",
    "battlefield-v5",
    "combined_arms-v6",
    "gather-v5",
    "tiger_deer-v4",
)

for _environment_id in _ENVIRONMENTS:
    _module_name = _environment_id.rsplit("-v", maxsplit=1)[0]
    _entry_point = f"magent2.environments.{_module_name}.{_module_name}"
    _register("aec", f"magent2/{_environment_id}", entry_point=_entry_point + ":env")
    _register(
        "parallel",
        f"magent2/{_environment_id}",
        entry_point=_entry_point + ":parallel_env",
    )
