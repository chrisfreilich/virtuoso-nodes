from .blendmodes import BlendModes
from .selectivecolor import SelectiveColor
from .contrast import Levels
from .blendif import BlendIf
from .colors import SplitRGB, MergeRGB
from .colors import ColorBalance, ColorBalanceAdvanced
from .colors import BlackAndWhite
from .colors import HueSatAdvanced, HueSat
from .colors import SolidColorRGB

NODE_CLASS_MAPPINGS = {
    "Levels": Levels,
    "BlendModes": BlendModes,
    "SelectiveColor": SelectiveColor,
    "BlendIf": BlendIf,
    "ColorBalance": ColorBalance,
    "ColorBalanceAdvanced": ColorBalanceAdvanced,
    "SplitRGB": SplitRGB,
    "MergeRGB": MergeRGB,
    "BlackAndWhite": BlackAndWhite,
    "HueSat": HueSat,
    "HueSatAdvanced": HueSatAdvanced,
    "SolidColorRGB": SolidColorRGB
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Levels": "Levels",
    "BlendModes": "Blend Modes",
    "SelectiveColor": "Selective Color",
    "BlendIf": "Blend If",
    "ColorBalance": "Color Balance",
    "ColorBalanceAdvanced": "Color Balance Advanced",
    "SplitRGB": "Split RGB",
    "MergeRGB": "Merge RGB",
    "BlackAndWhite": "Black and White",
    "HueSat": "Hue/Saturation",
    "HueSatAdvanced": "Hue/Saturation Advanced",
    "SolidColorRGB": "Solid Color RGB"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']