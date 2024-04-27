"""
@author: Chris Freilich
@title: Virtuoso Pack - Color Nodes
@nickname: Virtuoso Pack -Color Nodes
@description: This extension provides a solid color node, SplitRGB and MergeRGB nodes.
"""
import torch

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
      