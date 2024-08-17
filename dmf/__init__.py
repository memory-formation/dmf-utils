"""dmf utils package"""
from typing import TYPE_CHECKING
import lazy_loader as lazy

from .__version__ import __version__

subpackages = ["alerts", "io", "env"]
submod_attrs = {"env": ["env"]}

__getattr__, __dir__, __all__ = lazy.attach(__name__, subpackages, submod_attrs)

if TYPE_CHECKING:
    from . import alerts
    from . import io
    from .env import env

__all__ = ["__version__", "alerts", "io", "env"]

