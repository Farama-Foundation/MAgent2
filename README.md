MAgent
==============================================

![Build Status](http://112.74.109.55:8080/buildStatus/icon?job=magent)
![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg)

MAgent is a research platform for many-agent reinforcement learning.
Unlike previous research platforms that focus on reinforcement learning research with a single agent or only few agents, 
MAgent aims at supporting reinforcement learning research that scales up from hundreds to millions agents.
[see video](https://www.youtube.com/watch?v=HCSm0kVolqI)

## Requirement
MAgent currently supports Linux and OS X running Python 2.7 or python 3.
We make no assumptions about the structure of your agents.
You can write rule-based algorithms or use deep learning frameworks.

## Install on Linux

```bash
git clone git@github.com:geek-ai/magent.git
cd MAgent

sudo apt-get install cmake libboost-system-dev libjsoncpp-dev libwebsocketpp-dev

bash build.sh
export PYTHONPATH=$(pwd)/python:$PYTHONPATH
```

## Install on OSX
```bash
git clone git@github.com:geek-ai/magent.git
cd MAgent

brew install cmake llvm boost
brew install jsoncpp argp-standalone
brew tap david-icracked/homebrew-websocketpp
brew install --HEAD david-icracked/websocketpp/websocketpp

bash build.sh
export PYTHONPATH=$(pwd)/python:$PYTHONPATH
```

## Docs
[Get started](/doc/get_started.md)


## Examples
The training time of following tasks is about 1 day on a GTX1080-Ti card.
If out-of-memory errors occur, you can tune the map_size smaller or tune infer_batch_size smaller in models.

**Note** : You should run following examples in the root directory of this repo. Do not cd to `examples/`.

#### train
Three examples shown in the above video.
video files will be saved every 10 rounds. You can use render to see them.

* **pursuit**

	```
	python examples/train_pursuit.py --train
	```

* **gathering**

	```
	python examples/train_gather.py --train
	```

* **battle**

	```
	python examples/train_battle.py --train
	```
### play
An interactive game to play with battle agents.

* **battle game**
    ```
    python examples/show_battle_game.py
    ```

## Baseline Algorithms
The baseline algorithms are implemented both in Tensorflow and MXNet.
