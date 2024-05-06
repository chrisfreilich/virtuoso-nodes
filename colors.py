"""
@author: Chris Freilich
@title: Virtuoso Pack - Color Nodes
@nickname: Virtuoso Pack - Color Nodes
@description: This extension provides a solid color node, Color Balance Node, Color Balance Advanced Node,
SplitRGB and MergeRGB nodes, Hue/Saturation, Hue/Saturation Advanced, 
SolidColorRGB, SolidColorHSV, and Black and White nodes.
"""
import torch
from scipy.interpolate import CubicSpline
import colorsys
from .hsv import rgb_to_hsv, hsv_to_rgb

class SolidColorRGB():
    NAME = "Solid Color RGB"
    CATEGORY = "Virtuoso/Solid Color"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ('solid color image',)
    FUNCTION = "get_solid_color"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "red": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 255.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "green": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 255.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "blue": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 255.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "height": ("INT", {
                    "default": 1024,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "width": ("INT", {
                    "default": 1024,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "round": 1,  
                    "display": "number"}),
            },
            "optional":{
                "hex": ("STRING", {
                    "default": ""
                }),
            }
        }

    def get_solid_color(self, red, green, blue, height, width, hex=""):

        validated_hex = validate_hex_code(hex)

        if validated_hex == "":
            return (create_solid_rgb(red, green, blue, height, width), )
        else:
            return (create_solid_hex(validated_hex, height, width), )

class SolidColorHSV():
    NAME = "Solid Color HSV"
    CATEGORY = "Virtuoso/Solid Color"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ('solid color image',)
    FUNCTION = "get_solid_color"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "hue": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 360.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "saturation": ("FLOAT", {
                    "default": 50,
                    "min": 0,
                    "max": 100.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "value": ("FLOAT", {
                    "default": 100,
                    "min": 0,
                    "max": 100.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "height": ("INT", {
                    "default": 1024,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "width": ("INT", {
                    "default": 1024,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "round": 1,  
                    "display": "number"}),
            }
        }

    def get_solid_color(self, hue, saturation, value, height, width):
            return (create_solid_hsv(hue, saturation, value, height, width), )

class SolidColor():
    NAME = "Solid Color"
    CATEGORY = "Virtuoso/Solid Color"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ('solid color image',)
    FUNCTION = "get_solid_color"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "color": (["black", "silver", "gray", "white","maroon","red",	
                           "purple", "fuchsia",	"green", "lime", "olive",
                           "yellow", "navy", "blue", "teal", "aqua"],),
                "height": ("INT", {
                    "default": 1024,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "width": ("INT", {
                    "default": 1024,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "round": 1,  
                    "display": "number"}),
            }
        }

    def get_solid_color(self, color, height, width):
            
        colors = {"black":	    "#000000", 	
                  "silver":	    "#c0c0c0",	
                  "gray":	    "#808080",	
                  "white":	    "#ffffff",	
                  "maroon":	    "#800000",	
                  "red":	    "#ff0000",	
                  "purple":	    "#800080",	
                  "fuchsia":	"#ff00ff",	
                  "green":	    "#008000",	
                  "lime":	    "#00ff00",	
                  "olive":	    "#808000",	
                  "yellow":	    "#ffff00",	
                  "navy":	    "#000080",	
                  "blue":	    "#0000ff",	
                  "teal":	    "#008080",	
                  "aqua":	    "#00ffff",
                }

        return (create_solid_hex(colors[color], height, width), )

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
    CATEGORY = "Virtuoso/Channels"
    
    def do_split(self, image):
        # Create tensors for red, green, and blue channels
        red = torch.zeros_like(image)
        green = torch.zeros_like(image)
        blue = torch.zeros_like(image)

        # Assign the corresponding color channels from the input image to all images in the batch
        red[:, :, :, 0] = image[:, :, :, 0]
        green[:, :, :, 1] = image[:, :, :, 1]
        blue[:, :, :, 2] = image[:, :, :, 2]

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
    CATEGORY = "Virtuoso/Channels"
    
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
    CATEGORY = "Virtuoso/Adjustment"
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
    CATEGORY = "Virtuoso/Adjustment"
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

class BlackAndWhite():
    NAME = "Black and White"
    CATEGORY = "Virtuoso/Adjustment"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_black_and_white"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "image": ("IMAGE",),
                "red": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "green": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "blue": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}), 
                "cyan": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "magenta": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "yellow": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),                 
            }
        }

    def do_black_and_white(self, image, red, green, blue, cyan, magenta, yellow):
        """
        Convert a color image to black and white with adjustable color weights.

        Parameters:
        img (torch.Tensor): Input image tensor with shape [batch size, height, width, number of channels]
        red (float): Weight for red, range -1.0 to 1.0
        green (float): Weight for green, range -1.0 to 1.0
        blue (float): Weight for blue, range -1.0 to 1.0
        cyan (float): Weight for cyan, range -1.0 to 1.0
        magenta (float): Weight for magenta, range -1.0 to 1.0
        yellow (float): Weight for yellow, range -1.0 to 1.0

        Returns:
        torch.Tensor: Black and white image tensor with values in range 0-1
        """
        # Calculate minimum color value across all color channels for each pixel
        min_c, _ = image.min(dim=-1)

        # Calculate differences between color channels and minimum color value
        diff = image - min_c.unsqueeze(-1)

        # Create masks for red, green, and blue pixels
        red_mask = (diff[:, :, :, 0] == 0)
        green_mask = torch.logical_and((diff[:, :, :, 1] == 0), ~red_mask)
        blue_mask = ~torch.logical_or(red_mask, green_mask)

        # Calculate c, m, and yel values
        c, _ = diff[:, :, :, 1:].min(dim=-1)
        m, _ = diff[:, :, :, [0, 2]].min(dim=-1)
        yel, _ = diff[:, :, :, :2].min(dim=-1)

        # Calculate luminance using vectorized operations
        luminance = min_c + red_mask * (c * cyan + (diff[:, :, :, 1] - c) * green + (diff[:, :, :, 2] - c) * blue)
        luminance += green_mask * (m * magenta + (diff[:, :, :, 0] - m) * red + (diff[:, :, :, 2] - m) * blue)
        luminance += blue_mask * (yel * yellow + (diff[:, :, :, 0] - yel) * red + (diff[:, :, :, 1] - yel) * green)

        # Clip luminance values to be between 0 and 1
        luminance = luminance.clamp(0, 1)

        # Add an extra dimension for color channels
        luminance = luminance.unsqueeze(-1)

        # Convert grayscale to RGB by duplicating the grayscale channel
        rgb_image = luminance.expand(-1, -1, -1, 3)

        # If the original image had an alpha channel, append it back
        if image.shape[-1] == 4:
            alpha_channel = image[:, :, :, 3:]
            rgb_image = torch.cat((rgb_image, alpha_channel), dim=-1)

        return (rgb_image,)
    

class HueSatAdvanced():
    NAME = "Hue/Saturation Advanced"
    CATEGORY = "Virtuoso/Adjustment"
    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "do_hue_sat"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "image": ("IMAGE",),
                "hue_low": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 360.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "hue_low_feather": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 180,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "hue_high": ("FLOAT", {
                    "default": 360,
                    "min": 0,
                    "max": 360.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "hue_high_feather": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 180,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "hue_offset": ("FLOAT", {
                    "default": 0,
                    "min": -180.0,
                    "max": 180.0,
                    "step": 0.1,
                    "round": 0.01, 
                    "display": "number"}),
                "sat_offset": ("FLOAT", {
                    "default": 0,
                    "min": -100,
                    "max": 100,
                    "step": 0.1,
                    "round": 0.01, 
                    "display": "number"}),
                "lightness_offset": ("FLOAT", {
                    "default": 0,
                    "min": -100.0,
                    "max": 100.0,
                    "step": 0.1,
                    "round": 0.01, 
                    "display": "number"}),
            }
        }

    def do_hue_sat(self, image, hue_low, hue_low_feather, hue_high, hue_high_feather, hue_offset, sat_offset, lightness_offset):
        
        # Convert image to HSV and build mask
        image_hsv = rgb_to_hsv(image)
        mask = create_mask(image_hsv[..., 0], image_hsv[..., 1], hue_low, hue_high, hue_low_feather, hue_high_feather)
        # Adjust hue
        image_hsv[..., 0] = adjust_hue(image_hsv[..., 0], hue_offset)

        # Adjust saturation
        image_hsv[..., 1] = adjust_saturation(image_hsv[..., 1], sat_offset)

        # Adjust lightness
        image_hsv = adjust_lightness(image_hsv, lightness_offset)

        # Convert back to RGB
        adjusted_image_rgb = hsv_to_rgb(image_hsv[..., :3])

        # Blend the original and adjusted images based on the mask
        blended_rgb = (adjusted_image_rgb * mask.unsqueeze(-1)) + (image[..., :3] * (1 - mask.unsqueeze(-1)))

        # Include the alpha channel if present
        if image.shape[-1] == 4:
            blended_rgba = torch.cat((blended_rgb, image[..., 3:4]), dim=-1)
        else:
            blended_rgba = blended_rgb

        return (blended_rgba, mask)


class HueSat():
    NAME = "Hue/Saturation"
    CATEGORY = "Virtuoso/Adjustment"
    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "do_hue_sat"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "image": ("IMAGE",),
                "hue": (["red", "yellow", "green", "cyan", "blue", "magenta"],),
                "hue_width": (["normal","narrow", "wide"],),
                "feather": (["normal", "none", "wide"],),
                "hue_offset": ("FLOAT", {
                    "default": 0,
                    "min": -180.0,
                    "max": 180.0,
                    "step": 0.1,
                    "round": 0.01, 
                    "display": "number"}),
                "sat_offset": ("FLOAT", {
                    "default": 0,
                    "min": -100,
                    "max": 100,
                    "step": 0.1,
                    "round": 0.01, 
                    "display": "number"}),
                "lightness_offset": ("FLOAT", {
                    "default": 0,
                    "min": -100.0,
                    "max": 100.0,
                    "step": 0.1,
                    "round": 0.01, 
                    "display": "number"}),
            }
        }

    def do_hue_sat(self, image, hue, hue_width, feather, hue_offset, sat_offset, lightness_offset):
        
        # Convert image to HSV 
        image_hsv = rgb_to_hsv(image)

        # Calculate ranges from parameters
        hues = {"red": 0, "yellow": 60, "green": 120, "cyan": 180, "blue": 240, "magenta": 300}
        widths = {"narrow": 15, "normal": 30, "wide": 60}
        feathers = {"none": 0, "normal": 25, "wide": 50}
        base_hue = hues[hue]
        hue_low = base_hue - (widths[hue_width]/2)
        if hue_low < 0:
            hue_low = 360 + hue_low
        hue_high = base_hue + (widths[hue_width]/2)

        mask = create_mask(image_hsv[..., 0], image_hsv[..., 1], hue_low, hue_high, feathers[feather]/2, feathers[feather]/2)
        
        # Adjust hue
        image_hsv[..., 0] = adjust_hue(image_hsv[..., 0], hue_offset)

        # Adjust saturation
        image_hsv[..., 1] = adjust_saturation(image_hsv[..., 1], sat_offset)

        # Adjust lightness
        image_hsv = adjust_lightness(image_hsv, lightness_offset)

        # Convert back to RGB
        adjusted_image_rgb = hsv_to_rgb(image_hsv[..., :3])

        # Blend the original and adjusted images based on the mask
        blended_rgb = (adjusted_image_rgb * mask.unsqueeze(-1)) + (image[..., :3] * (1 - mask.unsqueeze(-1)))

        # Include the alpha channel if present
        if image.shape[-1] == 4:
            blended_rgba = torch.cat((blended_rgb, image[..., 3:4]), dim=-1)
        else:
            blended_rgba = blended_rgb

        return (blended_rgba, mask)

## Support functions
def create_solid_rgb(r, g, b, h, w):
    return torch.zeros(1, h, w, 3) + torch.tensor([r/255.0, g/255.0, b/255.0])

def create_solid_hsv(h, s, v, h_img, w_img):
    r, g, b = colorsys.hsv_to_rgb(h/360.0, s/100.0, v/100.0)
    return torch.zeros(1, h_img, w_img, 3) + torch.tensor([r, g, b])

def create_solid_hex(hex, h, w):
    if hex[0] == '#':
        hex = hex[1:]
    r, g, b = tuple(int(hex[i:i+2], 16)/255.0 for i in (0, 2, 4))
    return torch.zeros(1, h, w, 3) + torch.tensor([r, g, b])

def validate_hex_code(hex_code):
    hex_code = hex_code.lstrip('#')
    
    if len(hex_code) == 3 and all(c in '0123456789ABCDEFabcdef' for c in hex_code):
        return ''.join([c*2 for c in hex_code]).upper()
    elif len(hex_code) == 6 and all(c in '0123456789ABCDEFabcdef' for c in hex_code):
        return hex_code.upper()
    else:
        return ""

def create_mask(hue, saturation, hue_low, hue_high, hue_low_feather, hue_high_feather):
    # Normalize the values to the range [0, 1]
    hue_low_norm = hue_low / 360.0
    hue_high_norm = hue_high / 360.0
    hue_low_feather_norm = hue_low_feather / 360.0
    hue_high_feather_norm = hue_high_feather / 360.0

    # Calculate the mask
    mask_low = linearstep(hue_low_norm - hue_low_feather_norm, hue_low_norm, hue, increasing=True)
    mask_high = linearstep(hue_high_norm, hue_high_norm + hue_high_feather_norm, hue, increasing=False)
    
    if hue_low_norm < hue_high_norm:
        mask_middle = torch.where((hue >= hue_low_norm) & (hue <= hue_high_norm), torch.tensor(1.0), torch.tensor(0.0))
    else:
        mask_middle = torch.where((hue <= hue_low_norm) & (hue >= hue_high_norm), torch.tensor(0.0), torch.tensor(1.0))

    # Calculate the final mask by taking the maximum value among the three masks
    mask = torch.max(torch.max(mask_low, mask_middle), mask_high)

    # Only select pixels with a saturation greater than 0
    mask = torch.where(saturation > 0, mask, torch.tensor(0.0))

    return mask

def linearstep(low_edge, high_edge, x, increasing=True):
    # Handle the case where the gradient overflows past 0
    if low_edge < 0:
        # Define gradient function for low gradient
        overflow_mask_low = torch.where((x >= 0) & (x <= high_edge), (x - low_edge) / (high_edge - low_edge), torch.tensor(0.0))
        overflow_mask_high = torch.where((x >= (1 + low_edge)) & (x <= 1), (x - 1 - low_edge) / (high_edge - low_edge), torch.tensor(0.0))
        mask = torch.max(overflow_mask_low, overflow_mask_high)
    elif high_edge > 1:
        overflow_mask_high = torch.where((x >= low_edge) & (x <= 1), 1 - ((x - low_edge) / (high_edge - low_edge)), torch.tensor(0.0))
        overflow_mask_low = torch.where((x >= 0) & (x <= (high_edge - 1)), 1 - ((x + 1 - low_edge) / (high_edge - low_edge)), torch.tensor(0.0))
        mask = torch.max(overflow_mask_low, overflow_mask_high)
    else:
        # Create a mask where values within the range are set to abs( (hue value - low_edge)/(high_edge - low_edge))
        gradient = torch.abs((x - low_edge) / (high_edge - low_edge))
        if not increasing:
            gradient = 1 - gradient
        # Return the mask where values within the range are set to the gradient, and 0 otherwise
        mask = torch.where((x >= low_edge) & (x <= high_edge), gradient, torch.tensor(0.0))

    return mask

def adjust_saturation(saturation, sat_offset):
    # Calculate the change in saturation
    if sat_offset < 0:
        delta_saturation = (sat_offset / 100.0) * saturation
    else:
        delta_saturation = (sat_offset / 100.0) * (1 - saturation)
    # Apply the change to the saturation channel
    new_saturation = torch.clamp(saturation + delta_saturation, 0, 1)
    return new_saturation

def adjust_hue(hue, hue_offset):
    # Normalize hue_offset to the range [0, 1]
    hue_offset_normalized = hue_offset / 360.0
    # Apply the normalized hue_offset and ensure the result is within [0, 1]
    new_hue = (hue + hue_offset_normalized) % 1.0
    return new_hue

def adjust_lightness(image, lightness_offset):
    
    image_hsv = image.clone()

    # Map lightness_offset to [-1, 1]
    offset = lightness_offset / 100.0

    # If lightness_offset < 0, interpolate between the image and a black image
    if lightness_offset < 0:
        image_hsv[..., 2] = image_hsv[..., 2] * (1 + offset)
    # If lightness_offset > 0, interpolate between the image and a white image
    elif lightness_offset > 0:
        image_hsv[..., 2] = image_hsv[..., 2] * (1 - offset) + offset
        # Also reduce the saturation as the lightness increases
        image_hsv[..., 1] = image_hsv[..., 1] * ((1 - offset) ** 0.45)

    return image_hsv