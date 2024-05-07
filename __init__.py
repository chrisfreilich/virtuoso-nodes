from .blendmodes import BlendModes
from .selectivecolor import SelectiveColor
from .contrast import Levels
from .blendif import BlendIf
from .colors import SplitRGB, MergeRGB
from .colors import ColorBalance, ColorBalanceAdvanced
from .colors import BlackAndWhite
from .colors import HueSatAdvanced, HueSat
from .colors import SolidColorRGB, SolidColorHSV, SolidColor
from .blur import MotionBlur, LensBlur, GaussianBlur, MotionBlurDepth, LensBlurDepth, GaussianBlurDepth

NODE_CLASS_MAPPINGS = {
    "BlackAndWhite": BlackAndWhite,
    "BlendIf": BlendIf,
    "BlendModes": BlendModes,
    "ColorBalance": ColorBalance,
    "ColorBalanceAdvanced": ColorBalanceAdvanced,
    "HueSat": HueSat,
    "HueSatAdvanced": HueSatAdvanced,
    "Levels": Levels,
    "LensBlur": LensBlur,
    "MotionBlur": MotionBlur,
    "GaussianBlur": GaussianBlur,
    "LensBlurDepth": LensBlurDepth,
    "MotionBlurDepth": MotionBlurDepth,
    "GaussianBlurDepth": GaussianBlurDepth,
    "MergeRGB": MergeRGB,
    "SplitRGB": SplitRGB,
    "SelectiveColor": SelectiveColor,
    "SolidColor": SolidColor,
    "SolidColorRGB": SolidColorRGB,
    "SolidColorHSV": SolidColorHSV
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BlackAndWhite": "Black and White",
    "BlendIf": "Blend If",
    "BlendModes": "Blend Modes",
    "ColorBalance": "Color Balance",
    "ColorBalanceAdvanced": "Color Balance Advanced",
    "HueSat": "Hue/Saturation",
    "HueSatAdvanced": "Hue/Saturation Advanced",
    "Levels": "Levels",
    "LensBlur": "Lens Blur",
    "MotionBlur":"Motion Blur",
    "GaussianBlur": "Gaussian Blur",
    "LensBlurDepth": "Lens Blur with Depth Map",
    "MotionBlurDepth":"Motion Blur with Depth Map",
    "GaussianBlurDepth": "Gaussian Blur with Depth Map",
    "MergeRGB": "Merge RGB",
    "SplitRGB": "Split RGB",
    "SelectiveColor": "Selective Color",
    "SolidColor": "Solid Color",
    "SolidColorRGB": "Solid Color RGB",
    "SolidColorHSV": "Solid Color HSV"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']