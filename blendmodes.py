"""
@author: Chris Freilich
@title: Virtuoso Pack - Blend Modes
@nickname: Virtuoso Pack - Blend Nodes
@description: This extension provides a blend modes node with 30 blend modes.
"""
from PIL import Image
import numpy as np
import torch
import torch.nn.functional as F
from colorsys import rgb_to_hsv, hsv_to_rgb
from blend_modes import difference, normal, screen, soft_light, lighten_only, dodge,   \
                        addition, darken_only, multiply, hard_light,  \
                        grain_extract, grain_merge, divide, overlay

def dissolve(backdrop, source, opacity):
    # Normalize the RGB and alpha values to 0-1
    backdrop_norm = backdrop[:, :, :3] / 255
    source_norm = source[:, :, :3] / 255
    source_alpha_norm = source[:, :, 3] / 255

    # Calculate the transparency of each pixel in the source image
    transparency = opacity * source_alpha_norm

    # Generate a random matrix with the same shape as the source image
    random_matrix = np.random.random(source.shape[:2])

    # Create a mask where the random values are less than the transparency
    mask = random_matrix < transparency

    # Use the mask to select pixels from the source or backdrop
    blend = np.where(mask[..., None], source_norm, backdrop_norm)

    # Apply the alpha channel of the source image to the blended image
    new_rgb = (1 - source_alpha_norm[..., None]) * backdrop_norm + source_alpha_norm[..., None] * blend

    # Ensure the RGB values are within the valid range
    new_rgb = np.clip(new_rgb, 0, 1)

    # Convert the RGB values back to 0-255
    new_rgb = new_rgb * 255

    # Calculate the new alpha value by taking the maximum of the backdrop and source alpha channels
    new_alpha = np.maximum(backdrop[:, :, 3], source[:, :, 3])

    # Create a new RGBA image with the calculated RGB and alpha values
    result = np.dstack((new_rgb, new_alpha))

    return result

def hsv(backdrop, source, opacity, channel):
    # Convert RGBA to RGB, normalized
    backdrop_rgb = backdrop[:, :, :3] / 255.0
    source_rgb = source[:, :, :3] / 255.0
    source_alpha = source[:, :, 3] / 255.0

    # Convert RGB to HSV
    backdrop_hsv = np.array([rgb_to_hsv(*rgb) for row in backdrop_rgb for rgb in row]).reshape(backdrop.shape[:2] + (3,))
    source_hsv = np.array([rgb_to_hsv(*rgb) for row in source_rgb for rgb in row]).reshape(source.shape[:2] + (3,))

    # Combine HSV values
    new_hsv = backdrop_hsv.copy()
    
    # Determine which channel to operate on
    if channel == "saturation":
        new_hsv[:, :, 1] = (1 - opacity * source_alpha) * backdrop_hsv[:, :, 1] + opacity * source_alpha * source_hsv[:, :, 1]
    elif channel == "luminance":
        new_hsv[:, :, 2] = (1 - opacity * source_alpha) * backdrop_hsv[:, :, 2] + opacity * source_alpha * source_hsv[:, :, 2]
    elif channel == "hue":
        new_hsv[:, :, 0] = (1 - opacity * source_alpha) * backdrop_hsv[:, :, 0] + opacity * source_alpha * source_hsv[:, :, 0]
    elif channel == "color":
        new_hsv[:, :, :2] = (1 - opacity * source_alpha[..., None]) * backdrop_hsv[:, :, :2] + opacity * source_alpha[..., None] * source_hsv[:, :, :2]

    # Convert HSV back to RGB
    new_rgb = np.array([hsv_to_rgb(*hsv) for row in new_hsv for hsv in row]).reshape(backdrop.shape[:2] + (3,))

    # Apply the alpha channel of the source image to the new RGB image
    new_rgb = (1 - source_alpha[..., None]) * backdrop_rgb + source_alpha[..., None] * new_rgb

    # Ensure the RGB values are within the valid range
    new_rgb = np.clip(new_rgb, 0, 1)

    # Convert RGB back to RGBA and scale to 0-255 range
    new_rgba = np.dstack((new_rgb * 255, backdrop[:, :, 3]))

    return new_rgba.astype(np.uint8)

def saturation(backdrop, source, opacity):   
    return hsv(backdrop, source, opacity, "saturation")

def luminance(backdrop, source, opacity):
    return hsv(backdrop, source, opacity, "luminance")

def hue(backdrop, source, opacity):
    return hsv(backdrop, source, opacity, "hue")

def color(backdrop, source, opacity):
    return hsv(backdrop, source, opacity, "color")

def darker_lighter_color(backdrop, source, opacity, type):
    # Normalize the RGB and alpha values to 0-1
    backdrop_norm = backdrop[:, :, :3] / 255
    source_norm = source[:, :, :3] / 255
    source_alpha_norm = source[:, :, 3] / 255

    # Convert RGB to HSV
    backdrop_hsv = np.array([rgb_to_hsv(*rgb) for row in backdrop_norm for rgb in row]).reshape(backdrop.shape[:2] + (3,))
    source_hsv = np.array([rgb_to_hsv(*rgb) for row in source_norm for rgb in row]).reshape(source.shape[:2] + (3,))

    # Create a mask where the value (brightness) of the source image is less than the value of the backdrop image
    if type == "dark":
        mask = source_hsv[:, :, 2] < backdrop_hsv[:, :, 2]
    else:
        mask = source_hsv[:, :, 2] > backdrop_hsv[:, :, 2]

    # Use the mask to select pixels from the source or backdrop
    blend = np.where(mask[..., None], source_norm, backdrop_norm)

    # Apply the alpha channel of the source image to the blended image
    new_rgb = (1 - source_alpha_norm[..., None] * opacity) * backdrop_norm + source_alpha_norm[..., None] * opacity * blend

    # Ensure the RGB values are within the valid range
    new_rgb = np.clip(new_rgb, 0, 1)

    # Convert the RGB values back to 0-255
    new_rgb = new_rgb * 255

    # Calculate the new alpha value by taking the maximum of the backdrop and source alpha channels
    new_alpha = np.maximum(backdrop[:, :, 3], source[:, :, 3])

    # Create a new RGBA image with the calculated RGB and alpha values
    result = np.dstack((new_rgb, new_alpha))

    return result

def darker_color(backdrop, source, opacity):
    return darker_lighter_color(backdrop, source, opacity, "dark")

def lighter_color(backdrop, source, opacity):
    return darker_lighter_color(backdrop, source, opacity, "light")

def simple_mode(backdrop, source, opacity, mode):
    # Normalize the RGB and alpha values to 0-1
    backdrop_norm = backdrop[:, :, :3] / 255
    source_norm = source[:, :, :3] / 255
    source_alpha_norm = source[:, :, 3:4] / 255

    # Calculate the blend without any transparency considerations
    if mode == "linear_burn":
        blend = backdrop_norm + source_norm - 1   
    elif mode == "linear_light":
        blend = backdrop_norm + (2 * source_norm) - 1
    elif mode == "color_dodge":
        blend = backdrop_norm / (1 - source_norm)  
        blend = np.clip(blend, 0, 1) 
    elif mode == "color_burn":
        blend = 1 - ((1 - backdrop_norm) / source_norm)  
        blend = np.clip(blend, 0, 1)   
    elif mode == "exclusion":
        blend = backdrop_norm + source_norm - (2 * backdrop_norm * source_norm)
    elif mode == "subtract":
        blend = backdrop_norm - source_norm
    elif mode == "vivid_light":
        blend = np.where(source_norm <= 0.5, backdrop_norm / (1 - 2 * source_norm), 1 - (1 -backdrop_norm) / (2 * source_norm - 0.5) )
        blend = np.clip(blend, 0, 1)   
    elif mode == "pin_light":
        blend = np.where(source_norm <= 0.5, np.minimum(backdrop_norm, 2 * source_norm), np.maximum(backdrop_norm, 2 * (source_norm - 0.5)))  
    elif mode == "hard_mix":
        blend = simple_mode(backdrop, source, opacity, "linear_light")
        blend = np.round(blend[:, :, :3] / 255)

    # Apply the blended layer back onto the backdrop layer while utilizing the alpha channel and opacity information
    new_rgb = (1 - source_alpha_norm * opacity) * backdrop_norm + source_alpha_norm * opacity * blend

    # Ensure the RGB values are within the valid range
    new_rgb = np.clip(new_rgb, 0, 1)

    # Convert the RGB values back to 0-255
    new_rgb = new_rgb * 255

    # Calculate the new alpha value by taking the maximum of the backdrop and source alpha channels
    new_alpha = np.maximum(backdrop[:, :, 3], source[:, :, 3])

    # Create a new RGBA image with the calculated RGB and alpha values
    result = np.dstack((new_rgb, new_alpha))

    return result

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

modes = {
    "difference": difference, 
    "exclusion": exclusion,
    "dissolve": dissolve,
    "normal": normal, 
    "screen": screen,
    "soft light": soft_light, 
    "lighten": lighten_only, 
    "lighter color": lighter_color,
    "dodge": dodge,
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
                                "lighten", "screen", "dodge","color dodge", "linear dodge (add)", "lighter color",
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

        # Ensure images are in the correct form and data type
        backdrop_prepped = prep_image(backdrop)
        source_prepped = prep_image(source, invert_mask, mask)

        # Size source image to backdrop image, according to preference
        source_prepped = resize_image(backdrop_prepped, source_prepped, source_adjust)

        # Apply the blend mode
        blended_np = modes[blend_mode](backdrop_prepped, source_prepped, opacity)

        # return the image to Pytorch with proper shape
        final_tensor = (torch.from_numpy(blended_np / 255)).unsqueeze(0)
        
        return (final_tensor,)

def prep_image(img, invert_mask="true", mask=None):
    # Remove batch dimension if it exists
    if len(img.shape) == 4:
        img = img.squeeze(0)

    # Convert image from 0-1 to 0-255 data
    img = img * 255

    # Create or process mask
    if mask is None:
        # If img already has an alpha channel, use it
        if img.shape[2] == 4:
            alpha_channel = img[:, :, 3:4]
        else:
            # Create a new tensor with the same height and width as the input image
            # and a single channel filled with the maximum value (representing full opacity)
            alpha_channel = torch.full((img.shape[0], img.shape[1], 1), fill_value=255, dtype=img.dtype, device=img.device)
    else:
        # Add channel dimension if it doesn't exist
        if len(mask.shape) == 2:
            mask = mask.unsqueeze(-1)

        # Convert mask from 0-1 to 0-255 data
        mask = mask * 255

        # Invert mask if necessary
        if invert_mask == "yes":
            mask = 255 - mask

        # Resize mask to match image dimensions
        h, w = img.shape[:2]
        mask = F.interpolate(mask[None, ...], size=(h, w), mode='bilinear', align_corners=False)[0]

        # Squeeze the mask tensor to remove the extra dimension at the beginning
        mask = mask.squeeze(0)
        alpha_channel = mask

    # Ensure alpha_channel has the same number of dimensions as img
    if len(alpha_channel.shape) < len(img.shape):
        alpha_channel = alpha_channel.unsqueeze(-1)

    # If img already has an alpha channel, replace it
    if img.shape[2] == 4:
        img[:, :, 3:4] = alpha_channel
    else:
        # Concatenate the input image with the alpha channel along the channel dimension
        img = torch.cat((img, alpha_channel), dim=2)

    return img.numpy()
    
def resize_image(background, source, method):
    # Convert numpy arrays to PIL Images
    # Convert the data type to uint8 before converting to PIL Image
    background = Image.fromarray(background.astype(np.uint8))
    source = Image.fromarray(source.astype(np.uint8))

    # Get the size of the background image
    bg_width, bg_height = background.size

    if method == 'stretch':
        # Resize the source image to match the size of the background image
        resized_source = source.resize((bg_width, bg_height))

    elif method == 'crop':
        src_ratio = source.width / source.height
        bg_ratio = bg_width / bg_height
        if src_ratio > bg_ratio:
            new_height = bg_height
            new_width = int(new_height * src_ratio)
        else:
            new_width = bg_width
            new_height = int(new_width / src_ratio)
        resized_source = source.resize((new_width, new_height))

        # Calculate the area to crop
        left = (resized_source.width - bg_width) / 2
        top = (resized_source.height - bg_height) / 2
        right = (resized_source.width + bg_width) / 2
        bottom = (resized_source.height + bg_height) / 2

        # Crop the resized source image
        resized_source = resized_source.crop((left, top, right, bottom))

    else:
        raise ValueError("Invalid method. Choose either 'stretch' or 'crop'.")

    # Convert the resized source image back to a numpy array
    # Convert the data type back to float before returning
    resized_source = np.array(resized_source, dtype=np.float32)

    return resized_source
