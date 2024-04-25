from .blend import Blend
from .colors import SolidColor

NODE_CLASS_MAPPINGS = {
    "Blend": Blend,
    "SolidColor": SolidColor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Blend": "Blend Modes",
    "SolidColor": "Solid Color Image"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']