import torch

def rgb_to_hsv(rgb):
    # Separate the RGB channels
    r, g, b = rgb[:, :, :, 0:1], rgb[:, :, :, 1:2], rgb[:, :, :, 2:3]

    # Compute the HSV channels
    max_val, _ = torch.max(rgb[:, :, :, :3], dim=-1, keepdim=True)
    min_val, _ = torch.min(rgb[:, :, :, :3], dim=-1, keepdim=True)
    diff = max_val - min_val

    v = max_val

    s = diff / v
    s = torch.where(torch.isnan(s), torch.zeros_like(s), s)

    h = torch.zeros_like(r)
    h = torch.where((max_val == r) & (g >= b), ((g - b) / diff) / 6, h)
    h = torch.where((max_val == r) & (g < b), ((g - b) / diff) / 6 + 1, h)
    h = torch.where(max_val == g, ((b - r) / diff) / 6 + 1 / 3, h)
    h = torch.where(max_val == b, ((r - g) / diff) / 6 + 2 / 3, h)
    h = torch.where(max_val == min_val, torch.zeros_like(h), h)

    # If the input has an alpha channel, append it to the output
    if rgb.shape[-1] == 4:
        hsv = torch.cat((h, s, v, rgb[:, :, :, 3:4]), dim=-1)
    else:
        hsv = torch.cat((h, s, v), dim=-1)

    return hsv

def hsv_to_rgb(hsv):
    # Separate the HSV channels
    h, s, v = hsv[:, :, :, 0:1], hsv[:, :, :, 1:2], hsv[:, :, :, 2:3]

    # Compute the RGB channels
    i = (h * 6).floor()
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    i = i % 6

    r = torch.where(i == 0, v, torch.where(i == 1, q, torch.where(i == 2, p, torch.where(i == 3, p, torch.where(i == 4, t, v)))))
    g = torch.where(i == 0, t, torch.where(i == 1, v, torch.where(i == 2, v, torch.where(i == 3, q, torch.where(i == 4, p, p)))))
    b = torch.where(i == 0, p, torch.where(i == 1, p, torch.where(i == 2, t, torch.where(i == 3, v, torch.where(i == 4, v, q)))))

    # If the input has an alpha channel, append it to the output
    if hsv.shape[-1] == 4:
        rgb = torch.cat((r, g, b, hsv[:, :, :, 3:4]), dim=-1)
    else:
        rgb = torch.cat((r, g, b), dim=-1)

    return rgb

