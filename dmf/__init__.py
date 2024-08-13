"""dmf utils package"""
from typing import TYPE_CHECKING
import lazy_loader as lazy

from .__version__ import __version__

subpackages = ["alerts"]

__getattr__, __dir__, __all__ = lazy.attach(__name__, subpackages)

if TYPE_CHECKING:
    from . import alerts

__all__ = ["alerts", "__version__"]

