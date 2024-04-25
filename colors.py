'''
    COLORS.PY
    class SolidColor is a ComfyUI node to create solid color images.
    class SplitRGB is a ComfyUI node to split an image into three images with just one color channel.
    https://github.com/chrisfreilich/virtuoso-nodes/blob/main/README.md
'''
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
    FUNCTION = "do_split"
    CATEGORY = "Virtuoso"
    
    def do_split(self, img):
        # Create tensors for red, green, and blue channels
        red = torch.zeros_like(img)
        green = torch.zeros_like(img)
        blue = torch.zeros_like(img)

        # Assign the corresponding color channels from the input image
        red[:, :, 0] = img[:, :, 0]
        green[:, :, 1] = img[:, :, 1]
        blue[:, :, 2] = img[:, :, 2]

        return (red, green, blue)
        
        
