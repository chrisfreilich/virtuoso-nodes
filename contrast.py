"""
@author: Chris Freilich
@title: Virtuoso Pack - Contrast
@nickname: Virtuoso Pack - Contrast
@description: This extension provides a "Levels" node.
"""
import torch

class Levels:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "image": ("IMAGE",),
                "channel": (["RGB", "red", "green", "blue"],),
                "input_black_point": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.00,
                    "max": 0.98,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "input_gamma": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.01,
                    "max": 9.99,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "input_white_point": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "output_black_point": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "output_white_point": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_levels"
    CATEGORY = "Virtuoso/Adjustment"

    def do_levels(self, image, channel, input_black_point, input_gamma, input_white_point, output_black_point, output_white_point):
        """
        Applies levels adjustment to an input image tensor.

        Args:
            image (torch.Tensor): Input image tensor with shape [batch size, height, width, num color channels].
            channel (str): The color channel to adjust ('RGB', 'red', 'green', 'blue').
            input_black_point (float): Black point value (lower bound of input range).
            input_white_point (float): White point value (upper bound of input range).
            input_gamma (float): Gamma value (controls contrast).
            output_black_point (float): New black point value (lower bound of output range).
            output_white_point (float): New white point value (upper bound of output range).

        Returns:
            Tuple[torch.Tensor]: Output tensor with the adjusted pixel values in a tuple.
        """
        # Determine if there is an alpha channel
        has_alpha = image.shape[-1] in [2, 4]
        alpha_channel = image[..., -1:] if has_alpha else None

        # Extract the color channels (excluding alpha if present)
        color_channels = image[..., :-1] if has_alpha else image

        # Initialize a tensor to hold the adjusted color channels
        adjusted_color = torch.zeros_like(color_channels)

        # Apply the levels adjustment curve to the specified channel(s)
        for i, color in enumerate(['red', 'green', 'blue']):
            if channel == 'RGB' or channel == color:
                adjusted_channel = ((color_channels[..., i] - input_black_point) / (input_white_point - input_black_point)) ** input_gamma
                adjusted_channel = torch.clamp(adjusted_channel, 0.0, 1.0)
                adjusted_channel = output_black_point + (adjusted_channel * (output_white_point - output_black_point))
                adjusted_color[..., i] = adjusted_channel
            else:
                adjusted_color[..., i] = color_channels[..., i]

        # If there is an alpha channel, combine the adjusted color channels with the original alpha channel
        if has_alpha:
            adjusted_image = torch.cat([adjusted_color, alpha_channel], dim=-1)
        else:
            adjusted_image = adjusted_color

        # Return the adjusted image in a tuple
        return (adjusted_image,)