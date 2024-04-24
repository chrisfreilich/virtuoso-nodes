from PIL import Image
import numpy as np
import torch
import torch.nn.functional as F
from colorsys import rgb_to_hsv, hsv_to_rgb
from blend_modes import difference, normal, screen, soft_light, lighten_only, dodge,   \
                        addition, darken_only, multiply, hard_light,  \
                        grain_extract, grain_merge, divide, overlay

def subtract(backdrop, source, opacity):
    # Normalize the RGB and alpha values to 0-1
    backdrop_norm = backdrop[:, :, :3] / 255
    source_norm = source[:, :, :3] / 255
    source_alpha_norm = source[:, :, 3:4] / 255

    # Calculate the new RGB values by subtracting the source from the backdrop, weighted by the opacity
    # The source RGB values are also weighted by the normalized source alpha channel
    new_rgb = backdrop_norm - (source_norm * source_alpha_norm * opacity)

    # Ensure the RGB values are within the valid range
    new_rgb = np.clip(new_rgb, 0, 1)

    # Convert the RGB values back to 0-255
    new_rgb = new_rgb * 255

    # Calculate the new alpha value by taking the maximum of the backdrop and source alpha channels
    new_alpha = np.maximum(backdrop[:, :, 3], source[:, :, 3])

    # Create a new RGBA image with the calculated RGB and alpha values
    result = np.dstack((new_rgb, new_alpha))

    return result

def exclusion(backdrop, source, opacity):
    # Normalize the RGB and alpha values to 0-1
    backdrop_norm = backdrop[:, :, :3] / 255
    source_norm = source[:, :, :3] / 255
    source_alpha_norm = source[:, :, 3:4] / 255

    # Calculate the blend without any transparency considerations
    blend = backdrop_norm + source_norm - (2 * backdrop_norm * source_norm)

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

def dissolve(backdrop, source, opacity):

    # Calculate the probability based on the opacity value
    probability = 0.1 + (opacity * 0.8)

    # Create a random mask to determine which pixels to take from the source image
    mask = np.random.rand(*backdrop.shape[:2]) < probability

    # Create the output image, initially a copy of the backdrop
    output = backdrop.copy()

    # Where the mask is True, replace the pixel with the corresponding pixel from the source image
    output[mask] = source[mask]

    return output


def saturation(backdrop, source, opacity):
    # Convert RGBA to RGB
    backdrop_rgb = backdrop[:, :, :3] / 255.0
    source_rgb = source[:, :, :3] / 255.0

    # Convert RGB to HSV
    backdrop_hsv = np.array([rgb_to_hsv(*rgb) for row in backdrop_rgb for rgb in row]).reshape(backdrop.shape[:2] + (3,))
    source_hsv = np.array([rgb_to_hsv(*rgb) for row in source_rgb for rgb in row]).reshape(source.shape[:2] + (3,))

    # Combine HSV values
    new_hsv = backdrop_hsv.copy()
    new_hsv[:, :, 1] = (1 - opacity) * backdrop_hsv[:, :, 1] + opacity * source_hsv[:, :, 1]

    # Convert HSV back to RGB
    new_rgb = np.array([hsv_to_rgb(*hsv) for row in new_hsv for hsv in row]).reshape(backdrop.shape[:2] + (3,))

    # Convert RGB back to RGBA and scale to 0-255 range
    new_rgba = np.dstack((new_rgb * 255, backdrop[:, :, 3]))

    return new_rgba.astype(np.uint8)

def luminance(backdrop, source, opacity):
    # Convert RGBA to RGB
    backdrop_rgb = backdrop[:, :, :3] / 255.0
    source_rgb = source[:, :, :3] / 255.0

    # Convert RGB to HSV
    backdrop_hsv = np.array([rgb_to_hsv(*rgb) for row in backdrop_rgb for rgb in row]).reshape(backdrop.shape[:2] + (3,))
    source_hsv = np.array([rgb_to_hsv(*rgb) for row in source_rgb for rgb in row]).reshape(source.shape[:2] + (3,))

    # Combine HSV values
    new_hsv = backdrop_hsv.copy()
    new_hsv[:, :, 2] = (1 - opacity) * backdrop_hsv[:, :, 2] + opacity * source_hsv[:, :, 2]

    # Convert HSV back to RGB
    new_rgb = np.array([hsv_to_rgb(*hsv) for row in new_hsv for hsv in row]).reshape(backdrop.shape[:2] + (3,))

    # Convert RGB back to RGBA and scale to 0-255 range
    new_rgba = np.dstack((new_rgb * 255, backdrop[:, :, 3]))

    return new_rgba.astype(np.uint8)

def hue(backdrop, source, opacity):
    # Convert RGBA to RGB
    backdrop_rgb = backdrop[:, :, :3] / 255.0
    source_rgb = source[:, :, :3] / 255.0

    # Convert RGB to HSV
    backdrop_hsv = np.array([rgb_to_hsv(*rgb) for row in backdrop_rgb for rgb in row]).reshape(backdrop.shape[:2] + (3,))
    source_hsv = np.array([rgb_to_hsv(*rgb) for row in source_rgb for rgb in row]).reshape(source.shape[:2] + (3,))

    # Combine HSV values
    new_hsv = backdrop_hsv.copy()
    new_hsv[:, :, 0] = (1 - opacity) * backdrop_hsv[:, :, 0] + opacity * source_hsv[:, :, 0]

    # Convert HSV back to RGB
    new_rgb = np.array([hsv_to_rgb(*hsv) for row in new_hsv for hsv in row]).reshape(backdrop.shape[:2] + (3,))

    # Convert RGB back to RGBA and scale to 0-255 range
    new_rgba = np.dstack((new_rgb * 255, backdrop[:, :, 3]))

    return new_rgba.astype(np.uint8)

def color(backdrop, source, opacity):
    # Convert RGBA to RGB
    backdrop_rgb = backdrop[:, :, :3] / 255.0
    source_rgb = source[:, :, :3] / 255.0

    # Convert RGB to HSV
    backdrop_hsv = np.array([rgb_to_hsv(*rgb) for row in backdrop_rgb for rgb in row]).reshape(backdrop.shape[:2] + (3,))
    source_hsv = np.array([rgb_to_hsv(*rgb) for row in source_rgb for rgb in row]).reshape(source.shape[:2] + (3,))

    # Combine HSV values
    new_hsv = backdrop_hsv.copy()
    new_hsv[:, :, 0] = (1 - opacity) * backdrop_hsv[:, :, 0] + opacity * source_hsv[:, :, 0]
    new_hsv[:, :, 1] = (1 - opacity) * backdrop_hsv[:, :, 1] + opacity * source_hsv[:, :, 1]

    # Convert HSV back to RGB
    new_rgb = np.array([hsv_to_rgb(*hsv) for row in new_hsv for hsv in row]).reshape(backdrop.shape[:2] + (3,))

    # Convert RGB back to RGBA and scale to 0-255 range
    new_rgba = np.dstack((new_rgb * 255, backdrop[:, :, 3]))

    return new_rgba.astype(np.uint8)

# Map human readable blend mode names to functions.
modes = {
    "difference": difference, 
    "exclusion": exclusion,
    "dissolve": dissolve,
    "normal": normal, 
    "screen": screen,
    "soft light": soft_light, 
    "lighten": lighten_only, 
    "dodge": dodge,
    "linear dodge (add)": addition,
    "darken": darken_only,
    "multiply": multiply,
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

class Blend:
    
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

    # Concatenate the input image with the alpha channel along the channel dimension
    img_with_alpha = torch.cat((img, alpha_channel), dim=2)

    return img_with_alpha.numpy()
    
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
        # Calculate the aspect ratio of the source and background images
        src_ratio = source.width / source.height
        bg_ratio = bg_width / bg_height

        if src_ratio > bg_ratio:
            # If source aspect ratio is greater than background aspect ratio,
            # resize source height to match background height and adjust width
            # to maintain aspect ratio
            new_height = bg_height
            new_width = int(new_height * src_ratio)
        else:
            # If source aspect ratio is less than or equal to background aspect ratio,
            # resize source width to match background width and adjust height
            # to maintain aspect ratio
            new_width = bg_width
            new_height = int(new_width / src_ratio)

        # Resize the source image
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
