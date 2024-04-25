from .blend import Blend
from .colors import SolidColor
from .colors import SplitRGB

NODE_CLASS_MAPPINGS = {
    "Blend": Blend,
    "SolidColor": SolidColor,
    "SplitRGB": SplitRGB
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Blend": "Blend Modes",
    "SolidColor": "Solid Color Image",
    "SplitRGB": "Split RGB"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']