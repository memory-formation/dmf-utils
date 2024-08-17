from typing import TYPE_CHECKING

import lazy_loader as lazy

submod_attrs={
    "compress": ["compress"],
    "decompress": ["decompress"],
    "load": ["load"],
    "save": ["save"],
    "video": ["VideoWriter"],
}

__getattr__, __dir__, __all__ = lazy.attach(__name__, submod_attrs=submod_attrs)

if TYPE_CHECKING:
    from .compress import compress
    from .decompress import decompress
    from .load import load
    from .save import save
    from .video import VideoWriter


__all__ = ["compress", "decompress", "load", "save", "VideoWriter"]