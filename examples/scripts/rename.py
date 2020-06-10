"""rename tensorflow models"""

import sys

import magent
from models.tf_model import DeepQNetwork

env = magent.GridWorld("battle", map_size=125)

handles = env.get_handles()

rounds = eval(sys.argv[1])

for i in [rounds]:
    model = DeepQNetwork(env, handles[0], "battle")
    print("load %d" % i)
    model.load("data/", i, "selfplay")
    print("save %d" % i)
    model.save("data/battle_model", i)
