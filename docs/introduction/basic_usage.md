# Basic Usage

## Initializing Environments

The environments in MAgent2 are implemented using [PettingZoo](https://github.com/Farama-Foundation/PettingZoo). They can be initialized by calling their `env()` method and passing desired parameters:

```python
from magent2.environments import battle_v4
env = battle_v4.env(map_size=45, render_mode='human')
```

## Interaction Workflow

### AEC API (agents take turns)

Interacting with the environment involves iterating through the agents, pulling environment information with the `last()` method, and sending actions through the `step()` method:

```python
from magent2.environments import battle_v4

env = battle_v4.env(map_size=45, max_cycles=300)
env.reset()

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()
    if termination or truncation:
        action = None
    else:
        action = policy(observation, agent)
    env.step(action)

env.close()
```

### Parallel API (all agents act simultaneously)

The Parallel API is faster because all agents choose actions at the same time:

```python
from magent2.environments.battle.battle import parallel_env

env = parallel_env(map_size=45, max_cycles=300)
observations, infos = env.reset()

while env.agents:
    actions = {agent: env.action_space(agent).sample() for agent in env.agents}
    observations, rewards, terminations, truncations, infos = env.step(actions)

env.close()
```

## Rendering

### Human mode (pygame window)

```python
env = battle_v4.env(render_mode='human')
```

### Video generation (no display needed)

You can render frames programmatically and encode them into a video with ffmpeg. See `battle_video.py` in the project root for a complete example that:

1. Runs the battle simulation using the Parallel API
2. Renders each frame as a grid image using numpy (red = red team, blue = blue team)
3. Saves frames as BMP files and encodes them into MP4 with ffmpeg

```bash
python battle_video.py
```

Note: pygame's `rgb_array` render mode may hang on headless Windows environments. The `battle_video.py` script avoids this by rendering directly from the environment's internal state using numpy, without initializing pygame.

## Creating New Environments

It is recommended to create MAgent2-based environments using the PettingZoo API in order to take advantage of the general multi-agent processing infrastructure and standardization available there. `magent2/environments/magent_env.py` contains classes to facilitate this integration. See the [reference environments](https://github.com/Farama-Foundation/MAgent2/tree/main/magent2/environments) included in MAgent2 for some examples. See the MAgent2 API documentation for further details about what functionalities MAgent2 exposes for environment creation.
