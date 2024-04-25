from .blend import Blend
from .colors import SolidColor
from .colors import SplitRGB
from .colors import MergeRGB

NODE_CLASS_MAPPINGS = {
    "Blend": Blend,
    "SolidColor": SolidColor,
    "SplitRGB": SplitRGB,
    "MergeRGB": MergeRGB
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Blend": "Blend Modes",
    "SolidColor": "Solid Color Image",
    "SplitRGB": "Split RGB",
    "MergeRGB": "Merge RGB"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']