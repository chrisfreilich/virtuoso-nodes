from .blendmodes import BlendModes
from .selectivecolor import SelectiveColor
from .blendif import BlendIf
from .colors import SolidColor
from .colors import SplitRGB
from .colors import MergeRGB
from .colors import ColorBalance
from .colors import ColorBalanceAdvanced

NODE_CLASS_MAPPINGS = {
    "BlendModes": BlendModes,
    "SelectiveColor": SelectiveColor,
    "BlendIf": BlendIf,
    "ColorBalance": ColorBalance,
    "ColorBalanceAdvanced": ColorBalanceAdvanced,
    "SolidColor": SolidColor,
    "SplitRGB": SplitRGB,
    "MergeRGB": MergeRGB
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BlendModes": "Blend Modes",
    "SelectiveColor": "Selective Color",
    "BlendIf": "Blend If",
    "ColorBalance": "Color Balance",
    "ColorBalanceAdvanced": "Color Balance Advanced",
    "SolidColor": "Solid Color Image",
    "SplitRGB": "Split RGB",
    "MergeRGB": "Merge RGB"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']