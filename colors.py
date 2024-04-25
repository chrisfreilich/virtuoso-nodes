import torch

class SolidColor():
    NAME = "Solid Color"
    CATEGORY = "Colors"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Lexicon.IMAGE, Lexicon.RGB, Lexicon.MASK")
    FUNCTION = "get_solid_color"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
        "required": {},
        "optional": {
            "RGB color": ("VEC3", {"default": (128, 128, 128), "step": 1,
                                      "label": ["Red", "Green", "Blue"],
                                      "rgb": True, "tooltip": "Color to Output"}),
            "Image dimension": ("VEC2", {"default": (512, 512), "step": 1,
                                  "label": ["width", "height"],
                                  "tooltip": "dimensions of the solid color image"})
        }}

    def get_solid_color(self, color, dimension): 
        color = torch.tensor(color, dtype=torch.float32) / 255  # Normalize to 0-1
        dimension = torch.tensor(dimension, dtype=torch.int)

        # Create a 4D image tensor filled with the specified color
        image = torch.ones((1, 4, dimension[1], dimension[0]), dtype=torch.float32)

        # Assign the RGB channels
        image[:, :3, :, :] = color.view(1, 3, 1, 1)

        return image

