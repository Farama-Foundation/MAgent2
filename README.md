# MAgent

MAgent is a library for creating 2D environments with very large numbers of agents for conducting research in Multi-Agent Reinforcement Learning. These can look like this:

<img src="magent-graph-1.gif" width="200"><img src="magent-graph-2.gif" width="200">

This is a maintained fork from the original repo- https://github.com/geek-ai/MAgent. The code is signifigantly cleaned up in many aspects and some unfortunate names have been fixed, but there are no major differences.

This maintainenace was primarily done in the service of the [PettingZoo library](https://github.com/PettingZoo-Team/PettingZoo). PettingZoo is the easiest way to use environments in this library, and has comprehensive documentation of them.

## Requirements
MAgent supports Linux and macOS and Python 3.6+


## Install instructions
The library is built during pip installation (it doesn't take to long), requiring cmake (i.e. `sudo apt install cmake`)

Then you can simply use `pip install magent`


If you use this in your research, please cite the original paper:

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
  author = {Terry, Justin K and Black, Benjamin and Jayakumar, Mario},
  title = {MAgent},
  year = {2020},
  publisher = {GitHub},
  note = {GitHub repository},
  howpublished = {\url{https://github.com/PettingZoo-Team/MAgent}}
}
```
