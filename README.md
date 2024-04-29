# Virtuoso Nodes for ComfyUI

This set of nodes is designed to give some Photoshop-like functionality within ComfyUI. The nodes available are:

1. [**Blend Modes**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#blend-modes): Applies an image to another image using a blend mode operation. Every conceivable blend mode is available.
2. [**Blend If**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#blend-if-node): Composites one image on top of another with transparency based on several parameters.
3. [**Selective Color**](): Adjust the color of a specific color or brightness range in an image, as with Photoshop's Selective Color adjustment layer.
4. [**Color Balance**](): Make detailed color balance adjustments to shadows, midtones, and highlights of an image.
5. [**Color Balance Advanced**](): Color balance of a targeted brightness range.
6. [**Solid Color Image**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#solid-color-image): This node allows you to create an image of a single color. These can be very useful in conjunction with the blend modes.
7. [**SplitRGB**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#split-rgb-and-merge-rgb): This node takes an image and splits it into its red, green, and blue components. These then can be used in creative ways with blend modes as well.
8. [**MergeRGB**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#split-rgb-and-merge-rgb): This node takes three images, and merges the specified channels into one image. It is the complementary node to the SplitRGB node, to be used to recombine channels that you have split, though you can feel free to merge any images you wish for trippy effects.
<br>

[Installation Instructions]()

## Blend Modes

![Blend Modes Node Image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/baf71856-aefa-4ffb-9972-fc0b7e165956)

This node gives access to thirty different blend modes, and includes a scaling option for the top layer and the ability to use external masks.

### Node controls:

- **backdrop**: This is the background image. The output image will have the same dimensions as this image.
- **source**: This is the top image. If it is not the same size as the backdrop image, it will be resized to cover the backdrop.
- **mask**: Can be used to retain the alpha channel from the source image, or you can use an external mask to control the blended area.
- **opacity**: The opacity of the source image. The backdrop image is always 100% opacity. 
- **source_adjust**: The method by which the source image will be resized if necessary.
     - *Stretch* will change each dimension independently just as much as needed to match that dimension, potentially changing the aspect ratio of the source image and causing distortion.
     - *Crop* will maintain the aspect ratio of the source image, and resize it until it just covers the backdrop image, then crop what doesn't fit.
- **blend_mode**: normal is the default blend mode.

### Examples
[Normal](https://github.com/chrisfreilich/virtuoso-nodes/blob/main/normal-modes.md)
[Darken](https://github.com/chrisfreilich/virtuoso-nodes/blob/main/darken-modes.md)
[Lighten](https://github.com/chrisfreilich/virtuoso-nodes/blob/main/lighten-modes.md)
[Contrast](https://github.com/chrisfreilich/virtuoso-nodes/blob/main/contrast-modes.md)
[Component](https://github.com/chrisfreilich/virtuoso-nodes/blob/main/component-modes.md)
[Specialty](https://github.com/chrisfreilich/virtuoso-nodes/blob/main/specialty-mode.md)

[Learn about the math behind blend modes](https://learning.hccs.edu/faculty/bradly.brown/arts2348/handouts/blending-modes)  
[A practical discussion of the blend modes](https://www.youtube.com/watch?v=i1D9ijh3_-I)
<br><br>

## Blend If Node

![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/cab68d47-454b-4ae3-860b-f7d999caec2c)

This node gives you the functionality that is available with Photoshop's Blend If feature:

![Screenshot 2024-04-29 164742](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/5743979f-62d5-4a37-96c1-12b91d6eb3a4)

This feature composites the top_layer image over the bottom_layer image based on various possible calculations. ComfyUI's interface options being limited, the inputs have all been converted to fields instead of nice sliders.

### Node input controls:

- **top_layer**: This is the top image. If it is not the same size as the bottom_layer image, it will be resized to cover the bottom layer. This is equivalent to 'current layer' in Photoshop.
- **bottom_layer**: This is the background image. The output image will have the same dimensions as this image. This is equivalent to 'underlying layer' in Photoshop.
- **mask**: This is an optional mask for the top layer, which will add to the transparency of the top layer in addition to the transparency created by the Blend If process. Any alpha channels in the top_layer and bottom_layer images are ignored.
- **blend_if_layer**: Choose the layer that will be analyzed to determine the opacity of the top layer. This is equivalent to Photoshop's 'current layer' and 'underlying layer' sliders. This node only calculates one or the other.
- **blend_if_channel**: Which color channel (or gray) will be used to analyze the selected layer. This is equivalent to the "Blend If:" dropdown in photoshop.
- **start_rise, end_rise, start_fall, end_fall**: These four inputs define which brightness values for the selected channel on the selected layer are opaque. They are equivalent to the triangles below the 'current layer' and 'underlying layer' sliders, which each split into two to add softness to the selection. In this node, any brightness values lower than start_rise or greater than end_fall will be completely transparent, and brightness values between end_rise and start_fall will be completely opaque. Brightness values between start_rise and end_rise and between start_fall and end_fall will be partially transparent to feather the edges of the selection.
- **opacity**: Values less than 1 will reduce the opacity of the top_layer image in addition to any transparency calculated by the Blend If process. This is the equivalent to the opacity setting for the entire layer in Photoshop.
- **match_size**: Method to use to resize the top_layer image if it is not the same size as the bottom_layer image.
- **invert_mask**: 'yes' will invert the incoming mask before applying it to the top_layer image. Set to 'yes' by default, as it seems to be the more common situation.

### Node Outputs
- **IMAGE**: The final image with top_layer composited on top of bottom_layer.
- **MASK**: This is the mask generated by the Blend If process. It can be useful to ensure you are getting the result you want, or to do further processing on the same pixels.
<br>

## Selective Color Node

![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/667feff0-3237-4567-ae20-03ee91bc2330)

This feature allows you to adjust the color balance of a specified range of colors or brightness in an image. This node can be chained to affect different color ranges.

### Node input controls:

- **image**: This is image to be adjusted.
- **color_range**: This selects which range of colors or gray values will be affected.
- **cyan, magenta, yellow, black**: These inputs control how much of each secondary color or black is added or removed from the color range selected.
- **method**: 'absolute' will directly apply the change, whereas 'relative' will apply the change as a percentage of the current value, resulting in a subtler effect.

[Good reference on selective color](https://fstoppers.com/photoshop/selective-color-possibly-best-tool-photographers-7954) 

<br>


## Color Balance Node

![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/18963b51-2fc9-41e0-b6d8-b007d1d53853)

This feature allows you to finely adjust the color balance of the shadows, midtones, and highlights of an image. It reproduces the Photoshop functionality of the Color Balance layer.

### Node input controls:

- **image**: This is image to be adjusted.
- **lows, mids, highs**: Each of these prefixes indicates the brightness range on which the correction will have the greatest effect.
- **cyan_red, magenta_green, yellow_blue**: These suffixes indicate the color axis the adjustment will work on. -1 will be the most cyan/magenta/yellow possible, and 1 will be the most red/green/blue possible.
- **preserve luminosity**: This will maintain the brightness of the image while adjusting the relative color values. This will help prevent clipping of brightness values, while making the overall effect more subtle.
<br>

## Color Balance Advanced Node

![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/31bc0abe-547e-476f-a8fa-53ad5407e291)

This node allows you to target a specific brightness as the center of an adjustment range, and gives full range of adjustment. Unlike the standard Color Balance Node, it is easy to create distorted corrections with this node if you are not careful.

### Node input controls:

- **image**: This is image to be adjusted.
- **brightness_target**: What brightness level the correction should be centered on. 0 is black and 1 is white. This brightness level will receive the strongest correction, tapering off for brighter and darker pixels.
- **cyan_red, magenta_green, yellow_blue**: These suffixes indicate the color axis the adjustment will work on. -1 will be the most cyan/magenta/yellow possible, and 1 will be the most red/green/blue possible. Unlike the standard Color Balance Mode, these adjustments are unrestricted, so less is more!
- **preserve luminosity**: This will maintain the brightness of the image while adjusting the relative color values. This will help prevent clipping of brightness values, while making the overall effect more subtle.
<br>

## Solid Color Image

![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/d2fea774-a390-4adc-a2d5-4f475c508acf)

This node creates an image of a single color. This can be particularly useful for many of the blend modes. When using as the source image of a blend mode mode, the size is unimportant as it will be stretched to fit.

### Node controls:

- **RGB**: You can enter the red, green, and blue levels manually, or use the circle on the right to bring up a color picker. The color picker window appears at the top left of the screen.
- **size**: Enter the width and height of the image. If you're using the image as the source for a blending mode, you can set both values to 1 to save space, as it will be stretched to fit.
<br>

## Split RGB and Merge RGB 

![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/d8ae9988-5f5b-43da-bfaa-15b9778f1959)

These nodes split apart images into their component color channels and merge them back together. You can do fun things with the layers once they're separate, and then combine them back together when you're done. If you want even more control when merging them back together, you can use the Linear Dodge (Add) blend mode instead (twice), which will accomplish the same thing while giving you the ability to play around with the opacities of each layer.

### Node controls:

- **image**: The image to split on the Split RGB node, and the merged image on the Merge RGB node
- **red, green, blue**: The separate images holding the red, green, and blue channels of the image. Note that there is nothing stopping you from using any images you want here on the Merge RGB node-- the node will only take the indicated color channel from each image.
  
# Installation:

1. Git clone this repo into a folder in ComfyUI\custom_nodes.
2. pip install -r requirements.txt.
3. [Install FFmpeg](https://ffmpeg.org/download.html), which is required for the Selective Color Node.

**Please let me know if you have any thoughts or suggestions!**
<br><br>




