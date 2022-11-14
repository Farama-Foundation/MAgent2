# Basic Usage

## Initializing Environments

The reference environments in MAgent2 are implemented using [PettingZoo](https://github.com/Farama-Foundation/PettingZoo). They can be initialized by calling their `env()` method and passing desired parameters:

```python
from magent2.environments import battle_v4
env = battle_v4.env(map_size=16, render_mode='human')
```

Interacting with the environment then involves iterating through the agents, pulling environment information with the `last()` method, and sending actions through the `step()` method:

```python
env.reset()
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()
    action = policy(observation, agent)
    env.step(action)
```

For more details on the API components, see the [PettingZoo basic usage page](https://pettingzoo.farama.org/content/basic_usage/).


## Creating New Environments
It is recommended to create MAgent2-based environments using the PettingZoo API in order to take advantage of the general multi-agent processing infrastructure and standardization available there. `magent2/environments/magent_env.py` contains classes to facilitate this integration. See the [reference environments](https://github.com/Farama-Foundation/MAgent2/tree/main/magent2/environments) included in MAgent2 for some examples. See the MAgent2 API documentation for further details about what functionalities MAgent2 exposes for environment creation.
