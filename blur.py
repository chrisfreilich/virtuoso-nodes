"""
@author: Chris Freilich
@title: Virtuoso Pack - Blur
@nickname: Virtuoso Pack - Blur
@description: This extension provides blur nodes.
"""
import torch
import cv2
import numpy as np
from blurgenerator import motion_blur, lens_blur, gaussian_blur

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

def blur(image, type, amount=100, radius=5, components=4, exposure_gamma=2, size=100, angle=0):
        
        if image.shape[3] == 4:
            original_alpha = image[:, :, :, 3]
            image = image[:, :, :, :3]
        else:
            original_alpha = None
        
        blurred_images = []
        for img in image:            
            img_cv2 = img.cpu().numpy()
            img_cv2 = (img_cv2 * 255).astype(np.uint8)  # Convert to uint8
            img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_RGB2BGR)
            if type == "gaussian":
                blurred_img_cv2 = gaussian_blur(img_cv2, amount)
            elif type == "lens":
                blurred_img_cv2 = lens_blur(img_cv2, radius=radius, components=components, exposure_gamma=exposure_gamma)
            elif type == "motion":
                blurred_img_cv2 = motion_blur(img_cv2, size=size, angle=angle)
            blurred_img = cv2.cvtColor(blurred_img_cv2, cv2.COLOR_BGR2RGB)
            blurred_img = torch.from_numpy(blurred_img.astype(np.float32) / 255.0).to(image.device)  # Convert back to float32
            blurred_images.append(blurred_img)

        final_tensor = torch.stack(blurred_images)
        
        if original_alpha is not None:
            final_tensor = torch.cat((final_tensor, original_alpha.unsqueeze(3)), dim=3)
        
        return (final_tensor, )