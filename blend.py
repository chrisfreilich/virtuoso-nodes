from PIL import Image
import numpy as np
from blend_modes import difference, normal, screen, soft_light, lighten_only, dodge,   \
                        addition, darken_only, multiply, hard_light, subtract, \
                        grain_extract, grain_merge, divide, overlay
import torch

modes = {
    "difference": difference, 
    "normal": normal, 
    "screen": screen,
    "soft_light": soft_light, 
    "lighten_only": lighten_only, 
    "dodge": dodge,
    "addition": addition,
    "darken_only": darken_only,
    "multiply": multiply,
    "hard_light": hard_light,
    "subtract": subtract, 
    "grain_extract": grain_extract,
    "grain_merge": grain_merge, 
    "divide": divide, 
    "overlay": overlay
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
                "opacity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "source_adjust": (["crop", "stretch"],),
                "blend_mode": (["difference", "normal", "soft_light", "lighten_only", "dodge","addition",
                                "darken_only", "multiply","hard_light","subtract", "grain_extract",
                                "grain_merge", "divide", "overlay"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_blend"
    CATEGORY = "Virtuoso"
    
    def do_blend(self, backdrop, source, opacity, source_adjust, blend_mode):

        # Ensure images are in the correct form and data type
        backdrop_prepped = prep_image(backdrop)
        source_prepped = prep_image(source)

        # Size source image to backdrop image, according to preference
        source_prepped = resize_image(backdrop_prepped, source_prepped, source_adjust)

        # Apply the blend mode
        blended_np = modes[blend_mode](backdrop_prepped, source_prepped, opacity)

        # return the image to Pytorch with proper shape
        final_tensor = (torch.from_numpy(blended_np / 255)).unsqueeze(0)

        return (final_tensor,)

def prep_image(img):
    # Check if the image has a batch dimension and if so, remove it
    if img.shape[0] == 1:
        img = img.squeeze(0)

    # Convert image from 0-1 to 0-255 data
    img = img * 255

    # Make sure the image has an alpha channel
    if img.shape[2] == 4:
        return img
    elif img.shape[2] == 3:
        # Create a new tensor with the same height and width as the input image
        # and a single channel filled with the maximum value (representing full opacity)
        alpha_channel = torch.full((img.shape[0], img.shape[1], 1), fill_value=255, dtype=img.dtype, device=img.device)
        
        # Concatenate the input image with the new alpha channel along the channel dimension
        img_with_alpha = torch.cat((img, alpha_channel), dim=2)
        
        return img_with_alpha.numpy()
    else:
        raise ValueError("Input image must have either 3 (RGB) or 4 (RGBA) channels")
    
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