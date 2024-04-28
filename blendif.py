class ImageProcessor:
    def calculate_alpha_channel(self, img, start_rise, end_rise, start_fall, end_fall):
        # Calculate the luminosity of each pixel using the ITU BT.709 standard
        luminosity = 0.2126 * img[0, :, :, 0] + 0.7152 * img[0, :, :, 1] + 0.0722 * img[0, :, :, 2]

        # Initialize the alpha channel tensor
        alpha_channel = torch.zeros_like(luminosity)

        # Calculate the alpha values based on the luminosity and the transition points
        rise_mask = (start_rise <= luminosity) & (luminosity <= end_rise)
        fall_mask = (start_fall < luminosity) & (luminosity <= end_fall)
        
        t_rise = (luminosity[rise_mask] - start_rise) / (end_rise - start_rise)
        t_fall = (luminosity[fall_mask] - start_fall) / (end_fall - start_fall)
        
        alpha_channel[rise_mask] = t_rise * t_rise * (3.0 - 2.0 * t_rise)
        alpha_channel[fall_mask] = 1.0 - (t_fall * t_fall * (3.0 - 2.0 * t_fall))

        return alpha_channel.unsqueeze(0)
    
import torch
import cv2

class ImageProcessor:
    def hue_to_alpha(self, img, hue, width, smoothing):
        # Convert the image to HSV
        img_hsv = cv2.cvtColor(img.numpy(), cv2.COLOR_RGB2HSV)

        # Extract the hue channel
        hue_channel = img_hsv[:, :, 0]

        # Calculate the lower and upper hue bounds for full visibility
        lower_bound = hue - width
        upper_bound = hue + width

        # Calculate the lower and upper hue bounds for the smoothing transition
        lower_smooth_bound = lower_bound - smoothing
        upper_smooth_bound = upper_bound + smoothing

        # Initialize the alpha channel tensor
        alpha_channel = torch.zeros_like(hue_channel)

        # Calculate the alpha values based on the hue and the transition points
        rise_mask = (lower_bound <= hue_channel) & (hue_channel <= upper_bound)
        fall_mask = (start_fall < hue_channel) & (hue_channel <= end_fall)
        
        t_rise = (hue_channel[rise_mask] - lower_bound) / (upper_bound - lower_bound)
        t_fall = (hue_channel[fall_mask] - upper_bound) / (upper_smooth_bound - upper_bound)
        
        alpha_channel[rise_mask] = t_rise * t_rise * (3.0 - 2.0 * t_rise)
        alpha_channel[fall_mask] = 1.0 - (t_fall * t_fall * (3.0 - 2.0 * t_fall))

        return alpha_channel.unsqueeze(0)

