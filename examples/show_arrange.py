"""
Show arrange, pygame are required.
Type messages and let agents to arrange themselves to form these characters
"""

import sys
import argparse

from magent.renderer import PyGameRenderer
from magent.server import ArrangeServer as Server

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python show_arrange.py messages...")
        exit()
    PyGameRenderer().start(Server(messages=sys.argv[1:]), grid_size=5, add_counter=0)
