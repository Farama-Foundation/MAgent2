"""Tests for :mod:`magent2.render`."""

import os


# Run headless so the renderer can be constructed in CI without a real
# display or audio device. SDL reads these variables when its subsystems are
# initialized, so they must be set before pygame initializes anything.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "hide")

import pygame  # noqa: E402

from magent2.render import Renderer  # noqa: E402


class _FakeEnv:
    """Minimal stand-in for a GridWorld env, enough to build a Renderer."""

    def get_handles(self):
        return []


def test_human_mode_only_initializes_needed_subsystems():
    """The human render path must init only the display and font subsystems.

    ``pygame.init()`` eagerly starts every subsystem (audio/mixer, joystick,
    etc.), which MAgent2 never uses and which is slow to enumerate on some
    platforms. The renderer only needs ``display`` (for the window) and
    ``font`` (for the ``SysFont`` banners), so those are the only subsystems
    that should be initialized. See issue #68.
    """
    # Reset any global pygame state left over by other tests so the assertions
    # reflect exactly what constructing the Renderer initializes.
    pygame.quit()

    renderer = Renderer(_FakeEnv(), map_size=10, mode="human")
    try:
        assert pygame.display.get_init(), "display subsystem should be initialized"
        assert pygame.font.get_init(), "font subsystem should be initialized"
        assert (
            pygame.mixer.get_init() is None
        ), "audio/mixer subsystem should NOT be initialized on the render path"
    finally:
        renderer.close()
        pygame.quit()
