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
        # Calculate scale factor for top_layer
        scale_factor_top = max(bottom_layer.shape[1] / top_layer.shape[1], bottom_layer.shape[2] / top_layer.shape[2])

        # Resize top_layer while keeping aspect ratio constant
        top_layer = F.interpolate(top_layer.permute(0, 3, 1, 2), scale_factor=scale_factor_top, mode='bilinear', align_corners=False).permute(0, 2, 3, 1)

        # Crop top_layer to match bottom_layer size
        top_layer = top_layer[:, :bottom_layer.shape[1], :bottom_layer.shape[2], :]

        if m is not None:
            # Calculate scale factor for mask
            scale_factor_mask = max(bottom_layer.shape[1] / m.shape[1], bottom_layer.shape[2] / m.shape[2])

            # Resize and crop mask in the same way
            mask = F.interpolate(m.unsqueeze(1), scale_factor=scale_factor_mask, mode='nearest').squeeze(1).clone()
            mask = mask[:, :bottom_layer.shape[1], :bottom_layer.shape[2]]

    return top_layer, mask