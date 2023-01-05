# Key Concepts

The following points detail some of the functionality found in the library:

* **Observation view**: All agents observe a box around themselves. They see whether the coordinates are empty, contain an obstacle, or contain an agent in any of the observation channels. If an agent is on a coordinate, that entry will contain the value (agent's HP / max agent HP).

* **Feature vector**: The feature vector contains information about the agent itself. In normal mode, it contains `<agent_id, action, last_reward>`. In minimap mode, it also contains the agent position on the map, normalized to 0-1.

* **Observation**: The observation is a 3D observation view concatenated with a 1D feature vector by repeating the value of the feature across an entire image channel.

* **Minimap mode**: For most of the games (Battle, Battlefield, Combined Arms, Gather), the agents have access to additional global information: two density maps of the teams' respective presences on the map that are binned and concatenated onto the agent's observation view (concatenated in the channel dimension, axis=2). Their own absolute positions on the global map are appended to the feature vector. This feature can be turned on or off with the `minimap_mode` environment argument.

* **Moving and attacking**: An agent can either move or attack each step, so the action space is the concatenation of all possible moves and all possible attacks.

* **State**: A global observation of the environment can be retrieved by calling `env.state()`. The state observation space is a 3D observation of the complete map with dimensions equal to the map size. The first channel shows the walls in the map, where each element represents whether the coordinate is empty or has an obstacle. Concatenated to this channel, there is another pair of channels for each agent type, which indicates whether the coordinates contain an agent of that type binned to the value (agent's HP/ max agent HP). If extra features are selected the respective feature vector is concatenated and binned to each agent in the observation state.

### Termination

The game terminates after all agents of either team have died. This means that in the battle environments, where HP heals over time, the game will go on for a very long time with random actions.
