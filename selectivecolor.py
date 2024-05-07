"""
@author: Chris Freilich
@title: Virtuoso Pack - Selective Color
@nickname: Virtuoso Pack - Selective Color
@description: This extension provides a selective color node.
"""
import torch
import torchvision.transforms as transforms
import subprocess
import imageio
import tempfile

class SelectiveColor:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "image": ("IMAGE",),
                "color_range": (["reds", "yellows","greens", "cyans","blues", "magentas","whites", "neutrals", "blacks"],),
                "cyan": ("FLOAT", {
                    "default": 0.0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.01, 
                    "display": "number"}),
                "magenta": ("FLOAT", {
                    "default": 0.0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.01, 
                    "display": "number"}),
                "yellow": ("FLOAT", {
                    "default": 0.0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.01, 
                    "display": "number"}),
                "black": ("FLOAT", {
                    "default": 0.0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.01, 
                    "display": "number"}),
                "method": (["absolute", "relative"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "do_selectivecolor"
    CATEGORY = "Virtuoso/Adjustment"
    
    def do_selectivecolor(self, image, color_range, cyan, magenta, yellow, black, method):
        
        output_tensors = []

        # Create a temporary directory using the tempfile module
        with tempfile.TemporaryDirectory() as tmpdirname:

            # Iterate over each image in the batch
            for i in range(image.shape[0]):
                
                batch_image = image[i]

                # Permute the dimensions to be in the format expected by ToPILImage (C x H x W)
                batch_image = batch_image.permute(2, 0, 1)

                # Convert the PyTorch tensor to a PIL image
                img_pil = transforms.ToPILImage()(batch_image)
                img_pil.save(f"{tmpdirname}/temp{i}.png")

                # Construct the ffmpeg command
                command = ["ffmpeg", "-i", f"{tmpdirname}/temp{i}.png", "-vf"]
                command.append(f"selectivecolor={method}:{color_range}={cyan} {magenta} {yellow} {black}")
                command.extend(["-update", "1", f"{tmpdirname}/output{i}.png"])

                # Run the ffmpeg command
                subprocess.run(command)

                # Load the output image as a PyTorch tensor
                img_array = imageio.imread(f"{tmpdirname}/output{i}.png")
                img_tensor = transforms.ToTensor()(img_array)

                # Permute the dimensions back to the original format (H x W x C)
                img_tensor = img_tensor.permute(1, 2, 0)

                # Add the output tensor to the list
                output_tensors.append(img_tensor)

        # Stack the output tensors along a new dimension to form a batch
        output_batch = torch.stack(output_tensors)

        # Return the output batch
        return (output_batch,)

                
