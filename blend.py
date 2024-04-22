from PIL import Image
import numpy as np
from blend_modes import difference

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
        backdrop_rgba = Image.fromarray(backdrop).convert('RGBA')
        source_rgba = Image.fromarray(source).convert('RGBA')

        # Size source image
        width, height = backdrop_rgba.size
        source_rgba = source_rgba.resize((width, height))
        
        # Convert images back to numpy arrays
        backdrop = np.array(backdrop_rgba).astype(float)
        source = np.array(source_rgba).astype(float)

        # Apply the blend mode
        blended_array = difference(backdrop, source, opacity=1)

        # Convert the result to an 8-bit array and make an image from it
        blended_image = Image.fromarray(blended_array.astype(np.uint8))

        # Save the manipulated image
        blended_image.save("output.png")

        #do some processing on the image, in this example I just invert it
        image = 1.0 - image
        return (image,)

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

NODE_CLASS_MAPPINGS = {
    "Blend": Blend
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Blend": "Blend Modes Node"
}