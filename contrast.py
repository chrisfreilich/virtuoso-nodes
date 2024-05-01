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
    CATEGORY = "Virtuoso"

    def do_levels(self, image, channel, input_black_point, input_gamma, input_white_point, output_black_point, output_white_point):
        """
        Applies levels adjustment to an input image tensor.

        Args:
            image (torch.Tensor): Input image tensor with shape [batch size, height, width, num color channels].
            input_black_point (float): Black point value (lower bound of input range).
            input_white_point (float): White point value (upper bound of input range).
            input_gamma (float): Gamma value (controls contrast).
            output_black_point (float): New black point value (lower bound of output range).
            output_white_point (float): New white point value (upper bound of output range).

        Returns:
            torch.Tensor: Output tensor with the adjusted pixel values.
        """
        # Determine if there is an alpha channel
        has_alpha = image.shape[-1] in [2, 4]

        # Extract the color channels (excluding alpha if present)
        color_channels = image[..., :-1] if has_alpha else image

        # Apply the levels adjustment curve to color channels
        adjusted_color = ((color_channels - input_black_point) / (input_white_point - input_black_point)) ** input_gamma
        adjusted_color = torch.clamp(adjusted_color, 0.0, 1.0)

        # Linearly remap the adjusted pixel values to the specified output range
        remapped_color = output_black_point + (adjusted_color * (output_white_point - output_black_point))

        # If there is an alpha channel, combine the remapped color channels with the original alpha channel
        if has_alpha:
            alpha_channel = image[..., -1:]
            adjusted_image = torch.cat([remapped_color, alpha_channel], dim=-1)
        else:
            adjusted_image = remapped_color



        # MUST BE A TUPLE!
        return (adjusted_image, )