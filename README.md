# Virtuoso Nodes for ComfyUI

This set of nodes is designed to give some Photoshop-like functionality within ComfyUI. The nodes available are:

1. [**Blend Modes**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#blend-modes): Applies an image to another image using a blend mode operation. Every conceivable blend mode is available.
2. [**Blend If**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#blend-if-node): Composites one image on top of another with transparency based on several parameters.
3. [**Selective Color**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#selective-color-node): Adjust the color of a specific color or brightness range in an image, as with Photoshop's Selective Color adjustment layer.
4. [**Color Balance**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#color-balance-node): Make detailed color balance adjustments to shadows, midtones, and highlights of an image.
5. [**Color Balance Advanced**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#color-balance-advanced-node): Color balance of a targeted brightness range.
6. [**SplitRGB**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#split-rgb-and-merge-rgb): This node takes an image and splits it into its red, green, and blue components. These then can be used in creative ways with blend modes as well.
7. [**MergeRGB**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#split-rgb-and-merge-rgb): This node takes three images, and merges the specified channels into one image. It is the complementary node to the SplitRGB node, to be used to recombine channels that you have split, though you can feel free to merge any images you wish for trippy effects.
8. [**Levels**](https://github.com/chrisfreilich/virtuoso-nodes/blob/contrast/README.md#levels): Adjust the brightness levels of an image or single color channels. Works the same as Photoshop's Levels adjustment layer.
9. [**Black and White**](): Transform a color image into Black and White while controlling brightness levels based on hue. Works the same as Photoshop's Black and White adjustment layer.
10. [**Hue/Saturation**](): Simplified version of the Advanced Hue/Saturation Node. Allows you to choose colors by name, and choose from preset range sizes and feather values.
11. [**Hue/Saturation Advanced**](): Control Hue, Saturation, and Lightness of an image based on the selection of a range of hues. Works the same as Photoshop's Hue/Saturation adjustment layer.
12. [**Solid Color**](): Create a solid color image by choosing from a list of 16 basic colors.
13. [**Solid Color RGB**](): Create a solid color image by entering Red, Green, and Blue values, or entering an RGB hex value.
14. [**Solid Color HSV**](): Create a solid color image by entering Hue, Saturation, and Value.

[**Installation Instructions**](https://github.com/chrisfreilich/virtuoso-nodes/blob/selective-nodes/README.md#installation)
<br><br>

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

## Split RGB and Merge RGB 

![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/d8ae9988-5f5b-43da-bfaa-15b9778f1959)

These nodes split apart images into their component color channels and merge them back together. You can do fun things with the layers once they're separate, and then combine them back together when you're done. If you want even more control when merging them back together, you can use the Linear Dodge (Add) blend mode instead (twice), which will accomplish the same thing while giving you the ability to play around with the opacities of each layer.

### Node controls:

- **image**: The image to split on the Split RGB node, and the merged image on the Merge RGB node
- **red, green, blue**: The separate images holding the red, green, and blue channels of the image. Note that there is nothing stopping you from using any images you want here on the Merge RGB node-- the node will only take the indicated color channel from each image.

 <br>

 ## Levels 

![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/1e94949f-8e97-4e35-81b2-3f110bce9ea5)

This node works just like Photoshop's Levels, without the fancy controls. Move around your black and white points and your gamma, across all channels, or select just one color channel.

### Node controls:

- **image**: The image to set the levels for.
- **channel**: Choose 'RGB' to work on the whole image, or a color to set levels only on that color channel.
- **input_black_point**: Choose what brightness level becomes black. 0 is black, 1 is white.
- **input_gamma**: Adjust the gamma.
- **input_white_point**: Choose what brightness level becomes white. 0 is black, 1 is white.
- **output_black_point**: After input calculations are complete, what brightness will black pixels be output at.
- **output_white_point**: After input calculations are complete, what brightness will white pixels be output at.

  <br>
  
## Black and White 

![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/847120dd-6b24-4255-b7f7-070cf9482b2d)

This node works just like Photoshop's Black and White adjustment layer. Add or remove brightness based on each of the color ranges in the image.

### Node controls:

- **image**: The image to set the levels for.
- **red, green, blue, cyan, magenta, yellow**: Reduce these values to make the given color range darker, increase the values to make the given color range brighter.

  <br>
  

  # Installation:

1. Git clone this repo into a folder in ComfyUI\custom_nodes.
2. pip install -r requirements.txt.
3. [Install FFmpeg](https://ffmpeg.org/download.html), which is required for the Selective Color Node.

**Please let me know if you have any thoughts or suggestions!**
<br><br>




