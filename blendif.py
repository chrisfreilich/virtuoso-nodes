"""
@author: Chris Freilich
@title: Virtuoso Pack - Blend If
@nickname: Virtuoso Pack - Blend If
@description: This extension provides a "Blend If (BlendIf)" node.
"""
import torch
import torch.nn.functional as F

def calculate_opacity(t, start_rise, end_rise, start_fall, end_fall):
    # Values to the left of start_rise and to the right of end_fall return 0
    opacity = torch.zeros_like(t)
    # Apply cubic-bezier curve between start_rise and end_rise
    rise_mask = (t > start_rise) & (t < end_rise)
    t_normalized = (t[rise_mask] - start_rise) / (end_rise - start_rise)
    opacity[rise_mask] = 3 * t_normalized**2 - 2 * t_normalized**3
    # Values between end_rise and start_fall return 1
    opacity[(t >= end_rise) & (t <= start_fall)] = 1.0
    # Apply cubic-bezier curve between start_fall and end_fall
    fall_mask = (t > start_fall) & (t < end_fall)
    t_normalized = (t[fall_mask] - start_fall) / (end_fall - start_fall)
    opacity[fall_mask] = 1 - (3 * t_normalized**2 - 2 * t_normalized**3)
    return opacity

class BlendIf:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "top_layer": ("IMAGE",),
                "bottom_layer": ("IMAGE",),
                "blend_if_channel": (["gray", "red", "green", "blue"],),
                "start_rise": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "end_rise": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "start_fall": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "end_fall": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "opacity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "match_size": (["crop", "stretch"],),
                "invert_mask": (["yes", "no"],),
            },
            "optional": {
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE","MASK")
    FUNCTION = "do_blendif"
    CATEGORY = "Virtuoso"

    def do_blendif(self, top_layer, bottom_layer, blend_if_channel, start_rise, end_rise, start_fall, end_fall, opacity, match_size, invert_mask, mask=None):
        # Ensure the parameters are in order
        parameters = [end_fall, start_fall, end_rise, start_rise]
        for i in range(len(parameters) - 1):
            for j in range(i + 1, len(parameters)):
                if parameters[i] < parameters[j]:
                    parameters[i] = parameters[j]
        end_fall, start_fall, end_rise, start_rise = parameters

        # Resize top_layer and mask to match bottom_layer
        if match_size == 'stretch':
            top_layer = F.interpolate(top_layer, size=bottom_layer.shape[2:], mode='bilinear', align_corners=False)
            if mask is not None:
                mask = F.interpolate(mask, size=bottom_layer.shape[2:], mode='nearest')
        else:
            # Resize while keeping aspect ratio constant
            scale_factor = max(bottom_layer.shape[2] / top_layer.shape[2], bottom_layer.shape[3] / top_layer.shape[3])
            top_layer = F.interpolate(top_layer, scale_factor=scale_factor, mode='bilinear', align_corners=False)
            if mask is not None:
                mask = F.interpolate(mask, scale_factor=scale_factor, mode='nearest')
            # Crop to match bottom_layer
            top_layer = top_layer[..., :bottom_layer.shape[2], :bottom_layer.shape[3]]
            if mask is not None:
                mask = mask[..., :bottom_layer.shape[2], :bottom_layer.shape[3]]

        # Invert the mask if required
        if invert_mask == 'yes' and mask is not None:
            mask = 1 - mask

        # Calculate the base opacity
        if blend_if_channel == 'gray':
            luminosity = 0.2126 * top_layer[..., 0] + 0.7152 * top_layer[..., 1] + 0.0722 * top_layer[..., 2]
            base_opacity = calculate_opacity(luminosity, start_rise, end_rise, start_fall, end_fall)
        else:
            channel_index = {'red': 0, 'green': 1, 'blue': 2}[blend_if_channel]
            base_opacity = calculate_opacity(top_layer[..., channel_index], start_rise, end_rise, start_fall, end_fall)

        # Apply the mask and the opacity parameter
        if mask is not None:
            final_opacity = base_opacity * mask * opacity
        else:
            final_opacity = base_opacity * opacity

        # Composite the top_layer onto the bottom_layer
        new_image = final_opacity[..., None] * top_layer + (1.0 - final_opacity[..., None]) * bottom_layer

        return (new_image, base_opacity)