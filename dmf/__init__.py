"""dmf utils package"""
from typing import TYPE_CHECKING
import lazy_loader as lazy

from .__version__ import __version__

subpackages = ["notify"]

__getattr__, __dir__, __all__ = lazy.attach(__name__, subpackages)

if TYPE_CHECKING:
    from . import notify

__all__ = ["notify", "__version__"]

