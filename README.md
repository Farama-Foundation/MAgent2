<p align="center">
    <img src="https://raw.githubusercontent.com/Farama-Foundation/MAgent2/main/MAgent2-text.png" width="500px"/>
</p>

MAgent2 is a library for the creation of environments where large numbers of pixel agents in a gridworld interact in battles or other competitive scenarios.

<p align="center">
  <img src="https://raw.githubusercontent.com/Farama-Foundation/MAgent2/main/docs/environments/adversarial_pursuit.gif" width="200">
</p>

MAgent2 is a maintained fork of the original [MAgent](https://github.com/geek-ai/MAgent) codebase. It contains some [reference environments](https://github.com/Farama-Foundation/MAgent2/tree/main/magent2/environments) implemented using the [PettingZoo](https://github.com/Farama-Foundation/PettingZoo) API. These environments used to be included in PettingZoo itself, but have been moved here to exist independently. They are being regularly maintained and will receive bug fixes, support new versions of Python, etc. Development used to take place at [github.com/Farama-Foundation/MAgent](https://github.com/Farama-Foundation/MAgent) but was moved to [github.com/Farama-Foundation/MAgent2](https://github.com/Farama-Foundation/MAgent2) so that the distinction from the original MAgent library is clear to users.

## Installation

Install using pip:
```bash
pip install magent2
```

See [docs](https://magent2.farama.org/) for usage information.

### Build from source

MAgent2 includes a C++ native extension that requires CMake to build:

```bash
# Prerequisites: Python 3.10+, CMake, C++ compiler (GCC/Clang on Linux, MSVC on Windows)
git clone https://github.com/Farama-Foundation/MAgent2.git
cd MAgent2
pip install -e .
```

## Requirements

- Python 3.10+
- Linux or Windows
- Dependencies (installed automatically):
  - `numpy >= 1.21.0`
  - `pygame >= 2.1.0`
  - `pettingzoo >= 1.23.1` (which pulls in `gymnasium`)

### Tested with

| Package | Version |
|---------|---------|
| Python | 3.11 |
| numpy | 2.3.x |
| gymnasium | 1.2.3 |
| pettingzoo | 1.25.0 |
| pygame | 2.6.1 |

## Quick Start

### AEC API (agents take turns)

```python
from magent2.environments import battle_v4

env = battle_v4.env(map_size=45, max_cycles=300)
env.reset()

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()
    if termination or truncation:
        action = None
    else:
        action = env.action_space(agent).sample()  # random policy
    env.step(action)

env.close()
```

### Parallel API (all agents act simultaneously, faster)

```python
from magent2.environments.battle.battle import parallel_env

env = parallel_env(map_size=45, max_cycles=300)
observations, infos = env.reset()

while env.agents:
    actions = {agent: env.action_space(agent).sample() for agent in env.agents}
    observations, rewards, terminations, truncations, infos = env.step(actions)

env.close()
```

### Generate a battle video (requires ffmpeg)

```python
python battle_video.py
```

This renders each frame as a grid image (red = red team, blue = blue team) and encodes them into an MP4 video using ffmpeg. See `battle_video.py` for the full implementation.

## Available Environments

| Environment | Agents | Description |
|-------------|--------|-------------|
| `battle_v4` | 162 | Two teams battle on a 45x45 grid |
| `adversarial_pursuit_v4` | 75 | Predators chase prey agents |
| `battlefield_v5` | 162 | Large battlefield with obstacles |
| `combined_arms_v6` | 162 | Two unit types per team (melee + ranged) |
| `gather_v5` | 495 | Agents gather food while avoiding predators |
| `tiger_deer_v4` | 121 | Tigers hunt deer |

## References
```
@inproceedings{zheng2018magent,
  title={MAgent: A many-agent reinforcement learning platform for artificial collective intelligence},
  author={Zheng, Lianmin and Yang, Jiacheng and Cai, Han and Zhou, Ming and Zhang, Weinan and Wang, Jun and Yu, Yong},
  booktitle={Thirty-Second AAAI Conference on Artificial Intelligence},
  year={2018}
}
```

If you wish to cite this repo with it's modifications specifically, please cite:

```
@misc{magent2020,
  author = {Terry, Jordan K and Black, Benjamin and Jayakumar, Mario},
  title = {MAgent},
  year = {2020},
  publisher = {GitHub},
  note = {GitHub repository},
  howpublished = {\url{https://github.com/Farama-Foundation/MAgent}}
}
```

## Project Maintainers
- Project Manager: [Travis Virgil](https://github.com/virgilt) - `travis@farama.org`
- Maintenance for this project is also contributed by the broader Farama team: [farama.org/team](https://farama.org/team).
