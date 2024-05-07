"""
@author: Chris Freilich
@title: Virtuoso Pack - Blend Modes
@nickname: Virtuoso Pack - Blend Nodes
@description: This extension provides a blend modes node with 30 blend modes.
"""
import numpy as np
import torch
import torch.nn.functional as F
from blend_modes import grain_extract, grain_merge
from .resize import match_sizes
from .hsv import rgb_to_hsv, hsv_to_rgb

modes_8bit = ["grain extract", "grain merge"]

class BlendModes:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "backdrop": ("IMAGE",),
                "source": ("IMAGE",),
                "blend_mode": (["normal", "dissolve", "darken", "multiply", "color burn", "linear burn", "darker color", 
                                "lighten", "screen", "color dodge", "linear dodge (add)", "lighter color",
                                "overlay", "soft light", "hard light", "vivid light", "linear light", "pin light", "hard mix",
                                "difference", "exclusion", "subtract",  "divide",
                                "hue", "saturation", "color", "luminosity", 
                                "grain extract", "grain merge"],),
                "opacity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "source_adjust": (["crop", "stretch"],),
                "invert_mask": (["yes", "no"],),
            },
            "optional": {
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_blend"
    CATEGORY = "Virtuoso"
    
    def do_blend(self, backdrop, source, blend_mode, opacity, source_adjust, invert_mask, mask=None ):

            backdrop_prepped = handle_alpha(backdrop, False)
            source_prepped = handle_alpha(source, invert_mask, mask)
            source_prepped, _ = match_sizes(source_adjust, source_prepped, backdrop_prepped)
            if blend_mode in modes_8bit:
                source_prepped = source_prepped.squeeze(0)
                backdrop_prepped = backdrop_prepped.squeeze(0)
                source_prepped = source_prepped * 255
                backdrop_prepped = backdrop_prepped * 255
                final_tensor = torch.from_numpy(modes[blend_mode](backdrop_prepped.numpy(), source_prepped.numpy(), opacity)).unsqueeze(0)
            else:
                final_tensor = modes[blend_mode](backdrop_prepped, source_prepped, opacity)
            
            return (final_tensor,)
        
def handle_alpha(img, invert_mask="true", mask=None):

    alpha_img = img.clone()

    if mask is None:        
        if alpha_img.shape[3] == 4: # If img already has an alpha channel, use it
            alpha_channel = alpha_img[:, :, 3:4]
        else:
            alpha_channel = torch.full((1, alpha_img.shape[1], alpha_img.shape[2], 1), fill_value=1, dtype=img.dtype, device=img.device)
    else:
        alpha_channel = mask.clone()
        if invert_mask == "yes":
            alpha_channel = 1 - alpha_channel
        _, h, w, _ = alpha_img.shape
        alpha_channel = F.interpolate(alpha_channel[None, ...], size=(h, w), mode='bilinear', align_corners=False)[0]

    if len(alpha_channel.shape) < len(alpha_img.shape):
        alpha_channel = alpha_channel.unsqueeze(-1)

    if alpha_img.shape[3] == 4:    # If img already has an alpha channel, replace it
        alpha_img[:, :, 3:4] = alpha_channel
    else:
        batch_size = alpha_img.shape[0]
        alpha_channel_repeated = alpha_channel.repeat(batch_size, 1, 1, 1)
        alpha_img = torch.cat((alpha_img, alpha_channel_repeated), dim=3)

    return alpha_img

def dissolve(backdrop, source, opacity):

    transparency = opacity * source[..., 3]
    random_matrix = torch.rand_like(transparency)
    mask = random_matrix < transparency

    # Use the mask to select pixels from the source or backdrop
    blend = torch.where(mask[..., None], source[..., :3], backdrop[..., :3])

    # Apply the alpha channel of the source image to the blended image
    new_rgb = (1 - source[..., 3, None]) * backdrop[..., :3] + source[..., 3, None] * blend

    # Ensure the RGB values are within the valid range
    new_rgb = torch.clamp(new_rgb, 0, 1)

    # Calculate the new alpha value by taking the maximum of the backdrop and source alpha channels
    new_alpha = torch.max(backdrop[..., 3], source[..., 3])

    # Create a new RGBA image with the calculated RGB and alpha values
    result = torch.cat((new_rgb, new_alpha[..., None]), dim=-1)

    return result

def hsv(backdrop, source, opacity, channel):

    source_alpha = source[:, :, :, 3:4]

    # Convert RGB to HSV
    backdrop_hsv = rgb_to_hsv(backdrop)
    source_hsv = rgb_to_hsv(source)

    new_hsv = backdrop_hsv.clone()
    if channel == "saturation":
        new_hsv[:, :, :, 1:2] = (1 - opacity * source_alpha) * backdrop_hsv[:, :, :, 1:2] + opacity * source_alpha * source_hsv[:, :, :, 1:2]
    elif channel == "luminance":
        new_hsv[:, :, :, 2:3] = (1 - opacity * source_alpha) * backdrop_hsv[:, :, :, 2:3] + opacity * source_alpha * source_hsv[:, :, :, 2:3]
    elif channel == "hue":
        new_hue = source_hsv[:, :, :, 0:1]
        mask = (source_hsv[:, :, :, 1:2] == 0) # if sat == 0, sat = 0 in new image
        new_saturation = torch.where(mask, source_hsv[:, :, :, 1:2], backdrop_hsv[:, :, :, 1:2])
        new_hsv[:, :, :, 0:1] = new_hue
        new_hsv[:, :, :, 1:2] = new_saturation
    elif channel == "color":
        new_hsv[:, :, :, :2] = (1 - opacity * source_alpha) * backdrop_hsv[:, :, :, :2] + opacity * source_alpha * source_hsv[:, :, :, :2]
    
    new_rgb = hsv_to_rgb(new_hsv) 
    new_rgb = (1 - source_alpha * opacity) * backdrop + source_alpha * opacity * new_rgb  
    new_rgb = torch.clamp(new_rgb, 0, 1)
    rgb_channels = new_rgb[:, :, :, :3]
    backdrop_alpha = backdrop[:, :, :, 3:4]
    new_img = torch.cat((rgb_channels, backdrop_alpha), dim=-1)
    return new_img

def saturation(backdrop, source, opacity):   
    return hsv(backdrop, source, opacity, "saturation")

def luminance(backdrop, source, opacity):
    return hsv(backdrop, source, opacity, "luminance")

def hue(backdrop, source, opacity):
    return hsv(backdrop, source, opacity, "hue")

def color(backdrop, source, opacity):
    return hsv(backdrop, source, opacity, "color")

def darker_lighter_color(backdrop, source, opacity, type):

    # Convert RGB to HSV
    backdrop_hsv = rgb_to_hsv(backdrop)
    source_hsv = rgb_to_hsv(source)

    # Create a mask where the value (brightness) of the source image is less than the value of the backdrop image
    if type == "dark":
        mask = source_hsv[:, :, :, 2] < backdrop_hsv[:, :, :, 2]
    else:
        mask = source_hsv[:, :, :, 2] > backdrop_hsv[:, :, :, 2]

    # Use the mask to select pixels from the source or backdrop
    blend = torch.where(mask.unsqueeze(-1), source, backdrop)

    source_alpha = source[:, :, :, 3:4]
    new_rgb = (1 - source_alpha * opacity) * backdrop + source_alpha * opacity * blend
    rgb_channels = new_rgb[:, :, :, :3]
    backdrop_alpha = backdrop[:, :, :, 3:4]
    new_img = torch.cat((rgb_channels, backdrop_alpha), dim=-1)
    return new_img

def darker_color(backdrop, source, opacity):
    return darker_lighter_color(backdrop, source, opacity, "dark")

def lighter_color(backdrop, source, opacity):
    return darker_lighter_color(backdrop, source, opacity, "light")

def simple_mode(backdrop, source, opacity, mode):
    
    if mode == "linear_burn":
        blend = backdrop + source - 1  
    elif mode == "darken_only":
        rgb_min = torch.min(backdrop[..., :3], source[..., :3]) 
        alpha = backdrop[..., 3:]
        blend = torch.cat([rgb_min, alpha], dim=-1) 
    elif mode == "lighten_only":
        rgb_min = torch.max(backdrop[..., :3], source[..., :3]) 
        alpha = backdrop[..., 3:]
        blend = torch.cat([rgb_min, alpha], dim=-1) 
    elif mode == "difference":
        blend = abs(backdrop - source)
    elif mode == "normal":
        blend = source
    elif mode == "addition":
        blend = source + backdrop
    elif mode == "multiply":
        blend = source * backdrop
    elif mode == "divide":
        blend = backdrop / source
    elif mode == "screen":
        blend = 1 - (1-source)*(1-backdrop)
    elif mode == "linear_light":
        blend = backdrop + (2 * source) - 1
    elif mode == "color_dodge":
        blend = backdrop / (1 - source)  
    elif mode == "color_burn":
        blend = 1 - ((1 - backdrop) / source)   
    elif mode == "exclusion":
        blend = backdrop + source - (2 * backdrop * source)
    elif mode == "subtract":
        blend = backdrop - source
    elif mode == "soft_light":
        blend = torch.where(source <= 0.5, 2 * backdrop * source + backdrop * backdrop * (1 - 2 * source), 2 * backdrop * (1 - source) + torch.sqrt(backdrop) * ((2 * source) - 1))        
    elif mode == "overlay":
        blend = torch.where(backdrop <= 0.5, 2 * backdrop * source, 1 - 2 * (1 - backdrop) * (1 - source))
    elif mode == "hard_light":
        blend = torch.where(source <= 0.5, 2 * source * backdrop, 1 - 2 * (1 - backdrop) * (1 - source))
    elif mode == "vivid_light":
        blend = torch.where(source <= 0.5, backdrop / (1 - 2 * source), 1 - (1 -backdrop) / (2 * source - 0.5) ) 
    elif mode == "pin_light":
        blend = torch.where(source <= 0.5, torch.minimum(backdrop, 2 * source), torch.maximum(backdrop, 2 * (source - 0.5)))  
    elif mode == "hard_mix":
        blend = simple_mode(backdrop, source, opacity, "linear_light")
        rgb_channels = torch.round(blend[:, :, :, :3])
        alpha_channel = blend[:, :, :, 3:4]
        blend = torch.cat((rgb_channels, alpha_channel), dim=-1)

    blend = torch.clamp(blend, 0, 1) 

    source_alpha = source[:, :, :, 3:4]
    new_rgb = (1 - source_alpha * opacity) * backdrop + source_alpha * opacity * blend
    rgb_channels = new_rgb[:, :, :, :3]
    backdrop_alpha = backdrop[:, :, :, 3:4]
    new_img = torch.cat((rgb_channels, backdrop_alpha), dim=-1)
    return new_img

def normal(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "normal")
def difference(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "difference")
def multiply(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "multiply")
def divide(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "divide")
def addition(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "addition")
def linear_light(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "linear_light")
def vivid_light(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "vivid_light")
def pin_light(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "pin_light")
def hard_mix(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "hard_mix")
def linear_burn(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "linear_burn")
def color_dodge(backdrop, source, opacity): 
    return simple_mode(backdrop, source, opacity, "color_dodge") 
def color_burn(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "color_burn")
def exclusion(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "exclusion")
def subtract(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "subtract")
def screen(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "screen")
def soft_light(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "soft_light")
def hard_light(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "hard_light")
def overlay(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "overlay")
def darken_only(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "darken_only")
def lighten_only(backdrop, source, opacity):
    return simple_mode(backdrop, source, opacity, "lighten_only")

modes = {
    "difference": difference, 
    "exclusion": exclusion,
    "dissolve": dissolve,
    "normal": normal, 
    "screen": screen,
    "soft light": soft_light, 
    "lighten": lighten_only, 
    "lighter color": lighter_color,
    "dodge": color_dodge,
    "color dodge": color_dodge,
    "linear burn": linear_burn,
    "linear dodge (add)": addition,
    "linear light": linear_light,
    "vivid light": vivid_light,
    "pin light": pin_light,
    "hard mix": hard_mix,
    "darken": darken_only,
    "darker color": darker_color,
    "multiply": multiply,
    "color burn": color_burn,
    "hard light": hard_light,
    "subtract": subtract, 
    "grain extract": grain_extract,
    "grain merge": grain_merge, 
    "divide": divide, 
    "overlay": overlay,
    "hue": hue,
    "saturation": saturation,
    "color": color,
    "luminosity": luminance
}