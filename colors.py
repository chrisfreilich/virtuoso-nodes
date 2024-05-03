"""
@author: Chris Freilich
@title: Virtuoso Pack - Color Nodes
@nickname: Virtuoso Pack -Color Nodes
@description: This extension provides a solid color node, Color Balance Node, Color Balance Advanced Node,
SplitRGB and MergeRGB nodes, Hue/Saturation, and Black and White node.
"""
import torch
from torchvision.utils import save_image
from scipy.interpolate import CubicSpline

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
      

class ColorBalance():
    NAME = "Color Balance"
    CATEGORY = "Virtuoso"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_color_balance"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "image": ("IMAGE",),
                "lows_cyan_red": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "lows_magenta_green": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "lows_yellow_blue": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                 "mids_cyan_red": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "mids_magenta_green": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "mids_yellow_blue": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}), 
                "highs_cyan_red": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "highs_magenta_green": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "highs_yellow_blue": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "preserve_luminosity": ("BOOLEAN", {"default": True})
            }
        }

    def do_color_balance(self, image, lows_cyan_red, lows_magenta_green, lows_yellow_blue, 
                                      mids_cyan_red, mids_magenta_green, mids_yellow_blue,
                                      highs_cyan_red, highs_magenta_green, highs_yellow_blue, preserve_luminosity):
        return (color_balance(image, 
                              [lows_cyan_red, lows_magenta_green, lows_yellow_blue], 
                              [mids_cyan_red, mids_magenta_green, mids_yellow_blue], 
                              [highs_cyan_red, highs_magenta_green, highs_yellow_blue], preserve_luminosity=preserve_luminosity), )

class ColorBalanceAdvanced():
    NAME = "Color Balance Advanced"
    CATEGORY = "Virtuoso"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_color_balance"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "image": ("IMAGE",),
                "brightness_target": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.001,
                    "max": 0.999,
                    "step": 0.001,
                    "round": 0.001, 
                    "display": "number"}),
                "cyan_red": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "magenta_green": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "yellow_blue": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),  
                "preserve_luminosity": ("BOOLEAN", {"default": True})
            }
        }

    def do_color_balance(self, image, brightness_target, cyan_red, magenta_green, yellow_blue, preserve_luminosity):
        return (color_balance(image, 
                              [0, 0, 0], 
                              [cyan_red, magenta_green,yellow_blue], 
                              [0, 0, 0], 0.15, brightness_target, midtone_max=1, preserve_luminosity=preserve_luminosity), )


def color_balance(img, shadows, midtones, highlights, shadow_center=0.15, midtone_center=0.5, highlight_center=0.8, shadow_max=0.1, midtone_max=0.3, highlight_max=0.2, preserve_luminosity=False):
    # Create a copy of the img tensor
    img_copy = img.clone()

    # Calculate the original luminance if preserve_luminosity is True
    if preserve_luminosity:
        original_luminance = 0.2126 * img_copy[..., 0] + 0.7152 * img_copy[..., 1] + 0.0722 * img_copy[..., 2]

    # Define the adjustment curves
    def adjust(x, center, value, max_adjustment):
        # Scale the adjustment value
        value = value * max_adjustment
        
        # Define control points
        points = torch.tensor([[0, 0], [center, center + value], [1, 1]])
        
        # Create cubic spline
        cs = CubicSpline(points[:, 0], points[:, 1])
        
        # Apply the cubic spline to the color channel
        return torch.clamp(torch.from_numpy(cs(x)), 0, 1)

    # Apply the adjustments to each color channel
    # shadows, midtones, highlights are lists of length 3 (for R, G, B channels) with values between -1 and 1
    for i, (s, m, h) in enumerate(zip(shadows, midtones, highlights)):
        img_copy[..., i] = adjust(img_copy[..., i], shadow_center, s, shadow_max)
        img_copy[..., i] = adjust(img_copy[..., i], midtone_center, m, midtone_max)
        img_copy[..., i] = adjust(img_copy[..., i], highlight_center, h, highlight_max)

    # If preserve_luminosity is True, adjust the RGB values to match the original luminance
    if preserve_luminosity:
        current_luminance = 0.2126 * img_copy[..., 0] + 0.7152 * img_copy[..., 1] + 0.0722 * img_copy[..., 2]
        img_copy *= (original_luminance / current_luminance).unsqueeze(-1)

    return img_copy

class BlackAndWhite():
    NAME = "Black and White"
    CATEGORY = "Virtuoso"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_black_and_white"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "image": ("IMAGE",),
                "red": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "green": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "blue": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}), 
                "cyan": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "magenta": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),
                "yellow": ("FLOAT", {
                    "default": 0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, 
                    "display": "number"}),                 
            }
        }

    def do_black_and_white(self, image, red, green, blue, cyan, magenta, yellow):
        """
        Convert a color image to black and white with adjustable color weights.

        Parameters:
        img (torch.Tensor): Input image tensor with shape [batch size, height, width, number of channels]
        red (float): Weight for red, range -1.0 to 1.0
        green (float): Weight for green, range -1.0 to 1.0
        blue (float): Weight for blue, range -1.0 to 1.0
        cyan (float): Weight for cyan, range -1.0 to 1.0
        magenta (float): Weight for magenta, range -1.0 to 1.0
        yellow (float): Weight for yellow, range -1.0 to 1.0

        Returns:
        torch.Tensor: Black and white image tensor with values in range 0-1
        """
        # Calculate minimum color value across all color channels for each pixel
        min_c, _ = image.min(dim=-1)

        # Calculate differences between color channels and minimum color value
        diff = image - min_c.unsqueeze(-1)

        # Create masks for red, green, and blue pixels
        red_mask = (diff[:, :, :, 0] == 0)
        green_mask = torch.logical_and((diff[:, :, :, 1] == 0), ~red_mask)
        blue_mask = ~torch.logical_or(red_mask, green_mask)

        # Calculate c, m, and yel values
        c, _ = diff[:, :, :, 1:].min(dim=-1)
        m, _ = diff[:, :, :, [0, 2]].min(dim=-1)
        yel, _ = diff[:, :, :, :2].min(dim=-1)

        # Calculate luminance using vectorized operations
        luminance = min_c + red_mask * (c * cyan + (diff[:, :, :, 1] - c) * green + (diff[:, :, :, 2] - c) * blue)
        luminance += green_mask * (m * magenta + (diff[:, :, :, 0] - m) * red + (diff[:, :, :, 2] - m) * blue)
        luminance += blue_mask * (yel * yellow + (diff[:, :, :, 0] - yel) * red + (diff[:, :, :, 1] - yel) * green)

        # Clip luminance values to be between 0 and 1
        return (luminance.clamp(0, 1),)
    



class HueSat():
    NAME = "Hue/Saturation"
    CATEGORY = "Virtuoso"
    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "do_hue_sat"

    @classmethod
    def INPUT_TYPES(s) -> dict:
        return {
            "required": {
                "image": ("IMAGE",),
                "hue_low": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 360.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "hue_low_feather": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 180,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "hue_high": ("FLOAT", {
                    "default": 360,
                    "min": 0,
                    "max": 360.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "hue_high_feather": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": 180,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "hue_offset": ("FLOAT", {
                    "default": 0,
                    "min": -180.0,
                    "max": 180.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "sat_offset": ("FLOAT", {
                    "default": 0,
                    "min": -100,
                    "max": 100,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
                "lightness_offset": ("FLOAT", {
                    "default": 0,
                    "min": -100.0,
                    "max": 100.0,
                    "step": 1,
                    "round": 0.1, 
                    "display": "number"}),
            }
        }

    def do_hue_sat(self, image, hue_low, hue_low_feather, hue_high, hue_high_feather, hue_offset, sat_offset, lightness_offset):
        
        # Convert image to HSV and build mask
        image_hsv = rgb_to_hsv(image)
        mask = create_mask(image_hsv[..., 0], image_hsv[..., 1], hue_low, hue_high, hue_low_feather, hue_high_feather)
        # Adjust hue
        image_hsv[..., 0] = adjust_hue(image_hsv[..., 0], hue_offset)

        # Adjust saturation
        image_hsv[..., 1] = adjust_saturation(image_hsv[..., 1], sat_offset)

        # Adjust lightness
        image_hsv = adjust_lightness(image_hsv, lightness_offset)

        # Convert back to RGB
        adjusted_image_rgb = hsv_to_rgb(image_hsv[..., :3])

        # Blend the original and adjusted images based on the mask
        blended_rgb = (adjusted_image_rgb * mask.unsqueeze(-1)) + (image[..., :3] * (1 - mask.unsqueeze(-1)))

        # Include the alpha channel if present
        if image.shape[-1] == 4:
            blended_rgba = torch.cat((blended_rgb, image[..., 3:4]), dim=-1)
        else:
            blended_rgba = blended_rgb

        return (blended_rgba, mask)


# Thanks to MA Lee for conversion code    
def rgb_to_hsv(rgb: torch.Tensor) -> torch.Tensor:
    
    input_tensor = rgb.clone()

    # Check if there's an alpha channel
    has_alpha = input_tensor.shape[-1] == 4
    
    # Remove the alpha channel if it exists
    if has_alpha:
        alpha_channel = input_tensor[:, :, :, 3:4]
        input_tensor = input_tensor[:, :, :, :3]
    
    # Permute the dimensions from [B, H, W, 3] to [B, 3, H, W]
    input_tensor = input_tensor.permute(0, 3, 1, 2)
    
    # Convert RGB to HSV
    cmax, cmax_idx = torch.max(input_tensor, dim=1, keepdim=True)
    cmin = torch.min(input_tensor, dim=1, keepdim=True)[0]
    delta = cmax - cmin
    hsv_h = torch.empty_like(input_tensor[:, 0:1, :, :])
    cmax_idx[delta == 0] = 3
    hsv_h[cmax_idx == 0] = (((input_tensor[:, 1:2] - input_tensor[:, 2:3]) / delta) % 6)[cmax_idx == 0]
    hsv_h[cmax_idx == 1] = (((input_tensor[:, 2:3] - input_tensor[:, 0:1]) / delta) + 2)[cmax_idx == 1]
    hsv_h[cmax_idx == 2] = (((input_tensor[:, 0:1] - input_tensor[:, 1:2]) / delta) + 4)[cmax_idx == 2]
    hsv_h[cmax_idx == 3] = 0.
    hsv_h /= 6.
    hsv_s = torch.where(cmax == 0, torch.tensor(0.).type_as(input_tensor), delta / cmax)
    hsv_v = cmax
    hsv_tensor = torch.cat([hsv_h, hsv_s, hsv_v], dim=1)
    
    # Permute the dimensions back to [B, H, W, 3]
    hsv_tensor = hsv_tensor.permute(0, 2, 3, 1)
    
    # Add back the alpha channel if it was present
    if has_alpha:
        hsv_tensor = torch.cat([hsv_tensor, alpha_channel], dim=-1)
    
    return hsv_tensor

def hsv_to_rgb(hsv: torch.Tensor) -> torch.Tensor:

    input_tensor = hsv.clone()

    # Check if there's an alpha channel
    has_alpha = input_tensor.shape[-1] == 4
    
    # Remove the alpha channel if it exists
    if has_alpha:
        alpha_channel = input_tensor[:, :, :, 3:4]
        input_tensor = input_tensor[:, :, :, :3]
    
    # Permute the dimensions from [B, H, W, 3] to [B, 3, H, W]
    input_tensor = input_tensor.permute(0, 3, 1, 2)
    
    # Extract HSV components
    hsv_h, hsv_s, hsv_v = input_tensor[:, 0:1], input_tensor[:, 1:2], input_tensor[:, 2:3]
    _c = hsv_v * hsv_s
    _x = _c * (- torch.abs(hsv_h * 6. % 2. - 1) + 1.)
    _m = hsv_v - _c
    _o = torch.zeros_like(_c)
    idx = (hsv_h * 6.).type(torch.uint8)
    idx = (idx % 6).expand(-1, 3, -1, -1)
    rgb = torch.empty_like(input_tensor)
    rgb[idx == 0] = torch.cat([_c, _x, _o], dim=1)[idx == 0]
    rgb[idx == 1] = torch.cat([_x, _c, _o], dim=1)[idx == 1]
    rgb[idx == 2] = torch.cat([_o, _c, _x], dim=1)[idx == 2]
    rgb[idx == 3] = torch.cat([_o, _x, _c], dim=1)[idx == 3]
    rgb[idx == 4] = torch.cat([_x, _o, _c], dim=1)[idx == 4]
    rgb[idx == 5] = torch.cat([_c, _o, _x], dim=1)[idx == 5]
    rgb += _m
    
    # Permute the dimensions back to [B, H, W, 3]
    rgb_tensor = rgb.permute(0, 2, 3, 1)
    
    # Add back the alpha channel if it was present
    if has_alpha:
        rgb_tensor = torch.cat([rgb_tensor, alpha_channel], dim=-1)
    
    return rgb_tensor

def create_mask(hue, saturation, hue_low, hue_high, hue_low_feather, hue_high_feather):
    # Normalize the values to the range [0, 1]
    hue_low_norm = hue_low / 360.0
    hue_high_norm = hue_high / 360.0
    hue_low_feather_norm = hue_low_feather / 360.0
    hue_high_feather_norm = hue_high_feather / 360.0

    # Calculate the mask
    mask_low = linearstep(hue_low_norm - hue_low_feather_norm, hue_low_norm, hue, increasing=True)
    mask_high = linearstep(hue_high_norm, hue_high_norm + hue_high_feather_norm, hue, increasing=False)
    
    if hue_low_norm < hue_high_norm:
        mask_middle = torch.where((hue >= hue_low_norm) & (hue <= hue_high_norm), torch.tensor(1.0), torch.tensor(0.0))
    else:
        mask_middle = torch.where((hue <= hue_low_norm) & (hue >= hue_high_norm), torch.tensor(0.0), torch.tensor(1.0))

    # Calculate the final mask by taking the maximum value among the three masks
    mask = torch.max(torch.max(mask_low, mask_middle), mask_high)

    # Only select pixels with a saturation greater than 0
    mask = torch.where(saturation > 0, mask, torch.tensor(0.0))

    return mask

def save_hsv_components(image_hsv):
    save_image(image_hsv[..., 0].unsqueeze(0), 'C:/Users/chris/Desktop/hue.png')
    save_image(image_hsv[..., 1].unsqueeze(0), 'C:/Users/chris/Desktop/saturation.png')
    save_image(image_hsv[..., 2].unsqueeze(0), 'C:/Users/chris/Desktop/lightness.png')

def count_total_unique_values(tensor1, tensor2, tensor3):
    combined_tensor = torch.cat((tensor1.flatten(), tensor2.flatten(), tensor3.flatten()))
    unique_values = torch.unique(combined_tensor)
    print(f"The total number of unique values among the three tensors is {len(unique_values)}")

def count_unique_values(tensor):
    unique_values = torch.unique(tensor)
    print(f"The total number of unique values is {len(unique_values)}")

def count_out_of_range_values(tensor):
    unique_values = torch.unique(tensor)
    out_of_range_values = unique_values[(unique_values < 0) | (unique_values > 1)]
    print(f"The total number of unique values not in the range [0, 1] is {len(out_of_range_values)}")
    print(out_of_range_values)

def linearstep(low_edge, high_edge, x, increasing=True):
    # Handle the case where the gradient overflows past 0
    if low_edge < 0:
        # Define gradient function for low gradient
        overflow_mask_low = torch.where((x >= 0) & (x <= high_edge), (x - low_edge) / (high_edge - low_edge), torch.tensor(0.0))
        overflow_mask_high = torch.where((x >= (1 + low_edge)) & (x <= 1), (x - 1 - low_edge) / (high_edge - low_edge), torch.tensor(0.0))
        mask = torch.max(overflow_mask_low, overflow_mask_high)
    else:
        # Create a mask where values within the range are set to abs( (hue value - low_edge)/(high_edge - low_edge))
        gradient = torch.abs((x - low_edge) / (high_edge - low_edge))
        if not increasing:
            gradient = 1 - gradient
        # Return the mask where values within the range are set to the gradient, and 0 otherwise
        mask = torch.where((x >= low_edge) & (x <= high_edge), gradient, torch.tensor(0.0))

    return mask

def adjust_saturation(saturation, sat_offset):
    # Calculate the change in saturation
    if sat_offset < 0:
        delta_saturation = (sat_offset / 100.0) * saturation
    else:
        delta_saturation = (sat_offset / 100.0) * (1 - saturation)
    # Apply the change to the saturation channel
    new_saturation = torch.clamp(saturation + delta_saturation, 0, 1)
    return new_saturation

def adjust_hue(hue, hue_offset):
    # Normalize hue_offset to the range [0, 1]
    hue_offset_normalized = hue_offset / 360.0
    # Apply the normalized hue_offset and ensure the result is within [0, 1]
    new_hue = (hue + hue_offset_normalized) % 1.0
    return new_hue

def adjust_lightness(image_hsv, lightness_offset):
    # Map lightness_offset to [-1, 1]
    offset = lightness_offset / 100.0

    # If lightness_offset < 0, interpolate between the image and a black image
    if lightness_offset < 0:
        image_hsv[..., 2] = image_hsv[..., 2] * (1 + offset)
    # If lightness_offset > 0, interpolate between the image and a white image
    elif lightness_offset > 0:
        image_hsv[..., 2] = image_hsv[..., 2] * (1 - offset) + offset
        # Also reduce the saturation as the lightness increases
        image_hsv[..., 1] = image_hsv[..., 1] * ((1 - offset) ** 0.45)

    return image_hsv