"""
Interactive game, Pygame are required.
Act like a general and dispatch your solders.
"""
from examples.renderer import PyGameRenderer
from examples.renderer.server import BattleServer
from magent import utility

if __name__ == "__main__":
    utility.check_model("battle-game")
    PyGameRenderer().start(BattleServer())
