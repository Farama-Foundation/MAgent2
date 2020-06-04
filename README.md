# MAgent

MAgent is a library for creating 2D environments with very large numbers of agents for conducting research in Multi-Agent Reinforcement Learning. These can look like this:

<img src="https://kipsora.github.io/resources/magent-graph-1.gif" width="200"><img src="https://kipsora.github.io/resources/magent-graph-2.gif" width="200">

This is a maintained fork from the original repo- https://github.com/geek-ai/MAgent. 

## Requirements
MAgent supports Linux and macOS and Python 3.5+


## Install instructions
Note that the library is built during pip installation (it doesn't take to long).

Linux:

```bash
sudo apt-get install cmake libboost-system-dev libjsoncpp-dev libwebsocketpp-dev

pip3 install magent
```

macOS:

```bash

brew install cmake llvm boost@1.55
brew install jsoncpp argp-standalone
brew tap davidzhen0/homebrew-websocketpp
brew install --HEAD davidzhen0/websocketpp/websocketpp
brew link --force boost@1.55

pip3 install magent
```

If you use this in your research, please cite the original paper:

```
@inproceedings{zheng2018magent,
  title={MAgent: A many-agent reinforcement learning platform for artificial collective intelligence},
  author={Zheng, Lianmin and Yang, Jiacheng and Cai, Han and Zhou, Ming and Zhang, Weinan and Wang, Jun and Yu, Yong},
  booktitle={Thirty-Second AAAI Conference on Artificial Intelligence},
  year={2018}
}
```
