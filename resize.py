import torch.nn.functional as F

def match_sizes(match_size, top, bottom, m=None):
    top_layer = top.clone()
    bottom_layer = bottom.clone()
    mask = None

    # Resize top_layer and mask to match bottom_layer
    if match_size == 'stretch':
        top_layer = F.interpolate(top_layer.permute(0, 3, 1, 2), size=(bottom_layer.shape[1], bottom_layer.shape[2]), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)

        if m is not None:
            # Resize mask to match bottom_layer size
            mask = F.interpolate(m.unsqueeze(1), size=(bottom_layer.shape[1], bottom_layer.shape[2]), mode='nearest').squeeze(1).clone()
    else:
        # Calculate the scale factors for both dimensions separately
        scale_factor_h = bottom_layer.shape[1] / top_layer.shape[1]
        scale_factor_w = bottom_layer.shape[2] / top_layer.shape[2]

        # Use the correct scale factor to resize the top_layer
        scale_factor = max(scale_factor_w, scale_factor_h) # must grow/shrink while covering both dimensions of bottom_layer

        new_h = round(top_layer.shape[1] * scale_factor)
        new_w = round(top_layer.shape[2] * scale_factor)

        # Resize top_layer while keeping aspect ratio constant
        top_layer = F.interpolate(top_layer.permute(0, 3, 1, 2), size=(new_h, new_w), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)

        # Crop top_layer to match bottom_layer size
        top_layer = top_layer[:, :bottom_layer.shape[1], :bottom_layer.shape[2], :]

        if m is not None:
            # Calculate the scale factors for both dimensions separately for mask
            scale_factor_mask_h = bottom_layer.shape[1] / m.shape[1]
            scale_factor_mask_w = bottom_layer.shape[2] / m.shape[2]

            # Use the correct scale factor to resize the mask
            scale_factor_mask = max(scale_factor_mask_w, scale_factor_mask_h) # must grow to cover both dimensions

            new_h_mask = round(m.shape[1] * scale_factor_mask)
            new_w_mask = round(m.shape[2] * scale_factor_mask)

            # Resize and crop mask in the same way
            mask = F.interpolate(m.unsqueeze(1), size=(new_h_mask, new_w_mask), mode='nearest').squeeze(1).clone()
            mask = mask[:, :bottom_layer.shape[1], :bottom_layer.shape[2]]

    return top_layer, mask