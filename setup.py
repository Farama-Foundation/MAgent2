import setuptools

"""MAgent is a library for creating Multi-Agent Reinforcement Learning environments with very large numbers of agents

For details and documentation, please see:

https://github.com/PettingZoo-Team/MAgent/
"""

setuptools.setup(
    name="rlcard",
    version="0.1.0",
    author="PettingZoo Team",
    author_email="justinkterry@gmail.com",
    
    description="A Toolkit for Reinforcement Learning in Card Games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/datamllab/rlcard",
    keywords=["Reinforcement Learning", "game", "RL", "AI"],
    packages=setuptools.find_packages(exclude=('tests',)),
    package_data={
        'rlcard': ['models/pretrained/leduc_holdem_nfsp/*',
                   'models/pretrained/leduc_holdem_cfr/*',
                   'models/pretrained/leduc_holdem_nfsp_pytorch/*',
                   'games/uno/jsondata/action_space.json',
                   'games/limitholdem/card2index.json',
                   'games/leducholdem/card2index.json',
                   'games/doudizhu/jsondata/*',
                   'games/uno/jsondata/*',
                   'games/simpledoudizhu/jsondata/*'
                   ]},
    install_requires=[
        'numpy>=1.16.3',
        'matplotlib>=3.0',
        'termcolor',
    ],
    extras_require=extras,
    requires_python='>=3.5',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
