from typing import TYPE_CHECKING

import lazy_loader as lazy

submodules = ["video"]
submod_attrs={
    "compress": ["compress"],
    "decompress": ["decompress"],
    "load": ["load"],
    "save": ["save"],
}

__getattr__, __dir__, __all__ = lazy.attach(__name__, submodules, submod_attrs)

if TYPE_CHECKING:
    from .compress import compress
    from .decompress import decompress
    from .load import load
    from .save import save


__all__ = ["compress", "decompress", "load", "save", "video"]