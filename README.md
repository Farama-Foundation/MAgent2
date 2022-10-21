<p align="center">
    <img src="https://raw.githubusercontent.com/Farama-Foundation/MAgent2/main/MAgent2-text.png" width="500px"/>
</p>

MAgent2 is a library for creating 2D environments with very large numbers of agents for conducting research in Multi-Agent Reinforcement Learning. These can look like this:

<img src="magent-graph-1.gif" width="200"><img src="magent-graph-2.gif" width="200">

This is a maintained fork from the original repo- https://github.com/geek-ai/MAgent. The code is significantly cleaned up in many aspects and some unfortunate names have been fixed, but there are no major differences. These environments used to be included in the PettingZoo itself, but have been moved here to exist independently. These environments are being regularly maintained and will recieve bug fixes, new versions of Python, and so on.

## Requirements
MAgent2 supports Linux and macOS and Python 3.7+


## Install instructions
You can simply use `pip install magent2`


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
  author = {Terry, Jordan K and Black, Benjamin and Jayakumar, Mario},
  title = {MAgent},
  year = {2020},
  publisher = {GitHub},
  note = {GitHub repository},
  howpublished = {\url{https://github.com/Farama-Foundation/MAgent}}
}
```
