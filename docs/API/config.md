# Config

```{eval-rst}
.. autoclass:: magent2.gridworld.Config
```

## Methods

```{eval-rst}
.. autofunction:: magent2.gridworld.Config.set
.. autofunction:: magent2.gridworld.Config.register_agent_type
.. autofunction:: magent2.gridworld.Config.add_group
.. autofunction:: magent2.gridworld.Config.add_reward_rule
```

## Helper classes

### AgentSymbol and Event
`AgentSymbol` and `Event` are helper classes used to design rewards that go into the Config.

`AgentSymbol`s are used to represent some set of agents. They are instantiated with a group handle and the relevant agents within that group. The index can be a single number or "any" or "all".

Here is an example of creating two symbols, one for each of two groups:

```
import magent2.gridworld.AgentSymbol

as1 = AgentSymbol(group_1, index="any")
as2 = AgentSymbol(group_2, index="any")
```

`Event`s establish what must occur to trigger a reward disbursement. They are called with a subject (`AgentSymbol`), predicate, and relevant args.

Here are the available predicates and corresponding args:
| Predicate | Args                  |
|-----------|-----------------------|
| kill      | AgentSymbol           |
| at        | (x, y)                |
| in        | ((x1, y1), (x2, y2))  |
| attack    | AgentSymbol           |
| collide   | AgentSymbol           |
| die       | (empty)               |
| in_a_line | (empty)               |
| align     | (empty)               |

Here is an example creating reward rules for the two groups to attack each other:

```
from magent2.gridworld import Config, Event

config = Config()

e1 = Event(as1, "attack", as2)
config.add_reward_rule(e1, receiver=as1, value=attack_opponent_reward)

e2 = Event(as2, "attack", as1)
config.add_reward_rule(e2, receiver=as2, value=attack_opponent_reward)
```

More examples can be found in the [reference environments](https://github.com/Farama-Foundation/MAgent2/tree/main/magent2/environments).

### View Range
When using `register_agent_type()`, the attribute `view_range` is defined using one of the following classes:
```{eval-rst}
.. autoclass:: magent2.gridworld.CircleRange
.. autoclass:: magent2.gridworld.SectorRange
```
