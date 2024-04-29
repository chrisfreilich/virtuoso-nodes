"""
@author: Chris Freilich
@title: Virtuoso Pack - Color Nodes
@nickname: Virtuoso Pack -Color Nodes
@description: This extension provides a solid color node, SplitRGB and MergeRGB nodes.
"""
import torch
from scipy.interpolate import CubicSpline

class SolidColor():
    NAME = "Solid Color"
    CATEGORY = "Virtuoso"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ('solid color image',)
    FUNCTION = "get_solid_color"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
        "required": {},
        "optional": {
            "RGB": ("VEC3", {"default": (128, 128, 128), "step": 1,
                                      "label": ["Red", "Green", "Blue"],
                                      "rgb": True, "tooltip": "Color to Output"}),
            "size": ("VEC2", {"default": (512, 512), "step": 1,
                                  "label": ["width", "height"],
                                  "tooltip": "dimensions of the solid color image"})
        }}

    def get_solid_color(self, **kw):
        # Extract the color and dimension from the keyword arguments
        color = torch.tensor([kw['RGB']['0'], kw['RGB']['1'], kw['RGB']['2']], dtype=torch.float32) / 255  # Normalize to 0-1
        dimension = torch.tensor([kw['size']['0'], kw['size']['1']], dtype=torch.int)

        # Create a 4D image tensor filled with the specified color
        image = torch.ones((1, dimension[1], dimension[0], 4), dtype=torch.float32)

        # Assign the RGB channels
        image[:, :, :, :3] = color.view(1, 1, 1, 3)
        return (image, )
    
class SplitRGB():
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE","IMAGE","IMAGE")
    RETURN_NAMES = ('red', 'green', 'blue',)
    FUNCTION = "do_split"
    CATEGORY = "Virtuoso"
    
    def do_split(self, image):
        # Create tensors for red, green, and blue channels
        red = torch.zeros_like(image)
        green = torch.zeros_like(image)
        blue = torch.zeros_like(image)

        # Assign the corresponding color channels from the input image
        red[0, :, :, 0] = image[0, :, :, 0]
        green[0, :, :, 1] = image[0, :, :, 1]
        blue[0, :, :, 2] = image[0, :, :, 2]

        return (red, green, blue)
    

class MergeRGB():
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "red": ("IMAGE",),
                "green": ("IMAGE",),
                "blue": ("IMAGE",)
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_merge"
    CATEGORY = "Virtuoso"
    
    def do_merge(self, red, green, blue):
       
        # Create a tensor for the new image
        img = torch.zeros_like(red)

        # Assign the corresponding color channels from the input images
        img[0, :, :, 0] = red[0, :, :, 0]
        img[0, :, :, 1] = green[0, :, :, 1]
        img[0, :, :, 2] = blue[0, :, :, 2]

        return (img,)
      

class ColorBalance():
    NAME = "Color Balance"
    CATEGORY = "Virtuoso"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_color_balance"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "image": ("IMAGE",),
                "lows_cyan_red": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "lows_magenta_green": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "lows_yellow_blue": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                 "mids_cyan_red": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "mids_magenta_green": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "mids_yellow_blue": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}), 
                "highs_cyan_red": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "highs_magenta_green": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "highs_yellow_blue": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "preserve_luminosity": ("BOOLEAN", {"default": True})
            }
        }

    def do_color_balance(self, image, lows_cyan_red, lows_magenta_green, lows_yellow_blue, 
                                      mids_cyan_red, mids_magenta_green, mids_yellow_blue,
                                      highs_cyan_red, highs_magenta_green, highs_yellow_blue, preserve_luminosity):
        return (color_balance(image, 
                              [lows_cyan_red, lows_magenta_green, lows_yellow_blue], 
                              [mids_cyan_red, mids_magenta_green, mids_yellow_blue], 
                              [highs_cyan_red, highs_magenta_green, highs_yellow_blue], preserve_luminosity=preserve_luminosity), )

class ColorBalanceAdvanced():
    NAME = "Color Balance Advanced"
    CATEGORY = "Virtuoso"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_color_balance"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "image": ("IMAGE",),
                "brightness_target": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.001,
                    "max": 0.999,
                    "step": 0.001,
                    "round": 0.001, 
                    "display": "number"}),
                "cyan_red": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "magenta_green": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "yellow_blue": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),  
                "preserve_luminosity": ("BOOLEAN", {"default": True})
            }
        }

    def do_color_balance(self, image, brightness_target, cyan_red, magenta_green, yellow_blue, preserve_luminosity):
        return (color_balance(image, 
                              [0, 0, 0], 
                              [cyan_red, magenta_green,yellow_blue], 
                              [0, 0, 0], 0.15, brightness_target, midtone_max=1, preserve_luminosity=preserve_luminosity), )


def color_balance(img, shadows, midtones, highlights, shadow_center=0.15, midtone_center=0.5, highlight_center=0.8, shadow_max=0.1, midtone_max=0.3, highlight_max=0.2, preserve_luminosity=False):
    # Create a copy of the img tensor
    img_copy = img.clone()

    # Calculate the original luminance if preserve_luminosity is True
    if preserve_luminosity:
        original_luminance = 0.2126 * img_copy[..., 0] + 0.7152 * img_copy[..., 1] + 0.0722 * img_copy[..., 2]

    # Define the adjustment curves
    def adjust(x, center, value, max_adjustment):
        # Scale the adjustment value
        value = value * max_adjustment
        
        # Define control points
        points = torch.tensor([[0, 0], [center, center + value], [1, 1]])
        
        # Create cubic spline
        cs = CubicSpline(points[:, 0], points[:, 1])
        
        # Apply the cubic spline to the color channel
        return torch.clamp(torch.from_numpy(cs(x)), 0, 1)

    # Apply the adjustments to each color channel
    # shadows, midtones, highlights are lists of length 3 (for R, G, B channels) with values between -1 and 1
    for i, (s, m, h) in enumerate(zip(shadows, midtones, highlights)):
        img_copy[..., i] = adjust(img_copy[..., i], shadow_center, s, shadow_max)
        img_copy[..., i] = adjust(img_copy[..., i], midtone_center, m, midtone_max)
        img_copy[..., i] = adjust(img_copy[..., i], highlight_center, h, highlight_max)

    # If preserve_luminosity is True, adjust the RGB values to match the original luminance
    if preserve_luminosity:
        current_luminance = 0.2126 * img_copy[..., 0] + 0.7152 * img_copy[..., 1] + 0.0722 * img_copy[..., 2]
        img_copy *= (original_luminance / current_luminance).unsqueeze(-1)

    return img_copy