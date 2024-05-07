"""
@author: Chris Freilich
@title: Virtuoso Pack - Blur
@nickname: Virtuoso Pack - Blur
@description: This extension provides blur nodes.
"""
import torch
import cv2
import numpy as np
from blurgenerator import motion_blur, motion_blur_with_depth_map, \
                          lens_blur, lens_blur_with_depth_map, \
                          gaussian_blur, gaussian_blur_with_depth_map

class MotionBlur:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "image": ("IMAGE",),
                "size": ("INT", {
                    "default": 100.0,
                    "min": 0.0,
                    "max": 4096.0,
                    "step": 0.1,
                    "round": 0.01, 
                    "display": "number"}),
                "angle": ("INT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 360.0,
                    "step": 0.1,
                    "round": 0.01, 
                    "display": "number"})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_blur"
    CATEGORY = "Virtuoso/Blur"

    def do_blur(self, image, size, angle):
        return blur(image, "motion", size=size, angle=angle)  

class LensBlur:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "image": ("IMAGE",),
                "radius": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "components": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 6,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "exposure_gamma": ("FLOAT", {
                    "default": 2,
                    "min": -100,
                    "max": 100,
                    "step": 0.01,
                    "round": 0.01, 
                    "display": "number"})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_blur"
    CATEGORY = "Virtuoso/Blur"

    def do_blur(self, image, radius, components, exposure_gamma):
        return blur(image, "lens", radius=radius, components=components, exposure_gamma=exposure_gamma)

class GaussianBlur:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "image": ("IMAGE",),
                "amount": ("INT", {
                    "default": 100,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "round": 1, 
                    "display": "number"})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_blur"
    CATEGORY = "Virtuoso/Blur"

    def do_blur(self, image, amount):
        return blur(image, "gaussian", amount=amount)
    
class MotionBlurDepth:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "image": ("IMAGE",),
                "depth_map": ("IMAGE",),
                "angle": ("INT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 360.0,
                    "step": 0.1,
                    "round": 0.01, 
                    "display": "number"}),
                "num_layers": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "min_blur": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "max_blur": ("INT", {
                    "default": 100,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "round": 1, 
                    "display": "number"})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_blur"
    CATEGORY = "Virtuoso/Blur"

    def do_blur(self, image, depth_map, angle, num_layers, min_blur, max_blur):
        return blur(image, "motion_depth", depth_map=depth_map, angle=angle, num_layers=num_layers, min_blur=min_blur, max_blur=max_blur)  

class LensBlurDepth:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "image": ("IMAGE",),
                "depth_map": ("IMAGE",),
                "components": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 6,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "exposure_gamma": ("FLOAT", {
                    "default": 2,
                    "min": -100,
                    "max": 100,
                    "step": 0.01,
                    "round": 0.01, 
                    "display": "number"}),
                "num_layers": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "min_blur": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "max_blur": ("INT", {
                    "default": 100,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "round": 1, 
                    "display": "number"})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_blur"
    CATEGORY = "Virtuoso/Blur"

    def do_blur(self, image, depth_map, components, exposure_gamma, num_layers, min_blur, max_blur):
        return blur(image, "lens_depth", depth_map=depth_map, components=components, exposure_gamma=exposure_gamma, num_layers=num_layers, min_blur=min_blur, max_blur=max_blur)

class GaussianBlurDepth:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "image": ("IMAGE",),
                "depth_map": ("IMAGE",),
                "sigma": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "num_layers": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "min_blur": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "round": 1, 
                    "display": "number"}),
                "max_blur": ("INT", {
                    "default": 100,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "round": 1, 
                    "display": "number"})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_blur"
    CATEGORY = "Virtuoso/Blur"

    def do_blur(self, image, depth_map, sigma, num_layers, min_blur, max_blur):
        return blur(image, "gaussian_depth",  depth_map=depth_map, sigma=sigma, num_layers=num_layers, min_blur=min_blur, max_blur=max_blur)


def blur(image, type, depth_map=None, **kwargs):

    if type in ["lens_depth", "gaussian_depth", "motion_depth"]:
        if depth_map.shape[3] == 4:
            depth_map = depth_map[:, :, :, :3]  # Remove alpha channel if it exists

        # If batch size of depth_map does not match with image, use the first depth_map for all images
        if depth_map.shape[0] != image.shape[0]:
            depth_map = depth_map[0].unsqueeze(0).repeat(image.shape[0], 1, 1, 1)

    if image.shape[3] == 4:
        original_alpha = image[:, :, :, 3]
        image = image[:, :, :, :3]
    else:
        original_alpha = None

    blurred_images = []
    for i, img in enumerate(image):
        img_cv2 = img.cpu().numpy()
        img_cv2 = (img_cv2 * 255).astype(np.uint8)
        img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_RGB2BGR)

        if type == "gaussian":
            blurred_img_cv2 = gaussian_blur(img_cv2, kwargs["amount"])
        elif type == "lens":
            blurred_img_cv2 = lens_blur(img_cv2, kwargs["radius"], kwargs["components"], kwargs["exposure_gamma"])
        elif type == "motion":
            blurred_img_cv2 = motion_blur(img_cv2, kwargs["size"], kwargs["angle"])
        else: #depth map blur
            depth_map_img = depth_map[i].cpu().numpy()
            depth_map_img = (depth_map_img * 255).astype(np.uint8)
            if type == "motion_depth":
                blurred_img_cv2 = motion_blur_with_depth_map(img_cv2, depth_map=depth_map_img, angle=kwargs["angle"], num_layers=kwargs["num_layers"], min_blur=kwargs["min_blur"], max_blur=kwargs["max_blur"])
            elif type == "lens_depth":
                blurred_img_cv2 = lens_blur_with_depth_map(img_cv2, depth_map=depth_map_img, components=kwargs["components"], exposure_gamma=kwargs["exposure_gamma"], num_layers=kwargs["num_layers"], min_blur=kwargs["min_blur"], max_blur=kwargs["max_blur"])
            elif type == "gaussian_depth":
                blurred_img_cv2 = gaussian_blur_with_depth_map(img_cv2, depth_map=depth_map_img, sigma=kwargs["sigma"], num_layers=kwargs["num_layers"], min_blur=kwargs["min_blur"], max_blur=kwargs["max_blur"])
        blurred_img = cv2.cvtColor(blurred_img_cv2, cv2.COLOR_BGR2RGB)
        blurred_img = torch.from_numpy(blurred_img.astype(np.float32) / 255.0).to(image.device)
        blurred_images.append(blurred_img)

    final_tensor = torch.stack(blurred_images)

    if original_alpha is not None:
        final_tensor = torch.cat((final_tensor, original_alpha.unsqueeze(3)), dim=3)

    return (final_tensor, )