<p align="center">
    <img src="https://raw.githubusercontent.com/Farama-Foundation/MAgent2/main/MAgent2-text.png" width="500px"/>
</p>

MAgent2 is a library for the creation of environments where large numbers of pixel agents in a gridworld interact in battles or other competitive scenarios.

<p align="center">
  <img src="https://github.com/Farama-Foundation/MAgent2/blob/main/docs/environments/adversarial_pursuit.gif" width="200">
</p>

This is a maintained fork of the original [MAgent](https://github.com/geek-ai/MAgent) codebase and contains some reference [environments](https://github.com/Farama-Foundation/MAgent2/tree/main/magent2/environments) implemented using the [PettingZoo](https://github.com/Farama-Foundation/PettingZoo) API. These environments used to be included in PettingZoo itself, but have been moved here to exist independently. They are being regularly maintained and will receive bug fixes, support new versions of Python, etc. We used to develop this repo at https://github.com/Farama-Foundation/MAgent, but moved development here so that the distinction from the original MAgent package is clear to users.

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
