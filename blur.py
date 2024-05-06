"""
@author: Chris Freilich
@title: Virtuoso Pack - Blur
@nickname: Virtuoso Pack - Blur
@description: This extension provides a blur nodes.
"""
import torch
import cv2
from blurgenerator import motion_blur

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
        
        if image.shape[3] == 4:
            original_alpha = image[:, :, :, 3]
            image = image[:, :, :, :3]
        else:
            original_alpha = None
        
        blurred_images = []
        for img in image:            
            img_cv2 = img.cpu().numpy()
            img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_RGB2BGR)
            blurred_img_cv2 = motion_blur(img_cv2, size=size, angle=angle)
            blurred_img = cv2.cvtColor(blurred_img_cv2, cv2.COLOR_BGR2RGB)
            blurred_img = torch.from_numpy(blurred_img).to(image.device)
            blurred_images.append(blurred_img)

        final_tensor = torch.stack(blurred_images)
        
        if original_alpha is not None:
            final_tensor = torch.cat((final_tensor, original_alpha.unsqueeze(3)), dim=3)
        
        return (final_tensor, )