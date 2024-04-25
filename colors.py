import torch

class SolidColor():
    NAME = "Solid Color"
    CATEGORY = "Virtuoso"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image")
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
        color = [kw['RGB']['0'], kw['RGB']['1'], kw['RGB']['2']]
        dimension = [kw['size']['0'], kw['size']['1']]

        # Normalize the color to 0-1
        color = [value / 255 for value in color]

        # Create a 4D image tensor filled with the specified color
        image = [[[color + [1.0]] * dimension[0]] * dimension[1]]

        return (image, )

