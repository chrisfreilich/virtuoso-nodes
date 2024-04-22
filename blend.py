from PIL import Image
import numpy as np
from blend_modes import difference
import torch

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
                    "round": 0.001, #The value represeting the precision to round to, will be set to the step value by default. Can be set to False to disable rounding.
                    "display": "number"}),
                "source_adjust": (["crop", "squeeze"],),
                "blend_mode": (["difference"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_blend"
    CATEGORY = "Virtuoso"
    
    def do_blend(self, backdrop, source, opacity, source_adjust, blend_mode):

        # Ensure images are RGBA
        backdrop_prepped = prep_image(backdrop)
        source_prepped = prep_image(source)

        # Size source image
        # width, height = backdrop_rgba.size
        # source_rgba = source_rgba.resize((width, height))

        # Apply the blend mode
        blended_np = difference(backdrop_prepped, source_prepped, opacity=1)

        final_tensor = (torch.from_numpy(blended_np / 255)).unsqueeze(0)

        return (final_tensor,)

    """
        The node will always be re executed if any of the inputs change but
        this method can be used to force the node to execute again even when the inputs don't change.
        You can make this node return a number or a string. This value will be compared to the one returned the last time the node was
        executed, if it is different the node will be executed again.
        This method is used in the core repo for the LoadImage node where they return the image hash as a string, if the image hash
        changes between executions the LoadImage node is executed again.
    """
    #@classmethod
    #def IS_CHANGED(s, image, string_field, int_field, float_field, print_to_screen):
    #    return ""

def prep_image(img):
    # Check if the image has a batch dimension and if so, remove it
    if img.shape[0] == 1:
        img = img.squeeze(0)

    # Convert image from 0-1 to 0-255 data
    img = img * 255

    # Check if the image has an alpha channel
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