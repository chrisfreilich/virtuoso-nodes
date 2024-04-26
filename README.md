# Virtuoso Nodes for ComfyUI

This set of nodes is designed to give some Photoshop-like functionality within ComfyUI. The nodes available are:

1. **Blend Modes**: Applies an image to another image using a blend mode operation. Every conceivable blend mode is available!
2. **Solid Color Image**: This node allows you to create an image of a single color. These can be very useful in conjunction with the blend modes.
3. **SplitRGB**: This node takes an image and splits it into its red, green, and blue components. These then can be used in creative ways with blend modes as well.
4. **MergeRGB**: This node takes three images, and merges the specified channels into one image. It is the complementary node to the SplitRGB node, to be used to recombine channels that you have split, though you can feel free to merge any images you wish for trippy effects!
<br>

## Blend Modes

![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/baf71856-aefa-4ffb-9972-fc0b7e165956)

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
  
### Installation:

1. Git clone this repo into a folder in ComfyUI\custom_nodes
2. pip install -r requirements.txt

Learn about the math behind the blend modes here: https://learning.hccs.edu/faculty/bradly.brown/arts2348/handouts/blending-modes
A practical discussion of the blend modes here: https://www.youtube.com/watch?v=i1D9ijh3_-I

**Please let me know if you have any thoughts or suggestions!**
<br><br>


# Examples
Normal Modes: [Normal](https://github.com/chrisfreilich/virtuoso-nodes/tree/main#normal-mode), [Dissolve](https://github.com/chrisfreilich/virtuoso-nodes/edit/tree/README.md#dissolve-mode-not-terribly-useful-on-its-own-used-here-with-a-second-screen-blend-mode)  
Darken Modes: [Darken](https://github.com/chrisfreilich/virtuoso-nodes/tree/main/README.md#darken-mode), [Multiply](https://github.com/chrisfreilich/virtuoso-nodes/tree/main/README.md#multiply-mode), [Color Burn](https://github.com/chrisfreilich/virtuoso-nodes/tree/main/README.md#color-burn-mode), [Linear Burn](https://github.com/chrisfreilich/virtuoso-nodes/tree/main/README.md#linear-burn-mode), [Darker Color](https://github.com/chrisfreilich/virtuoso-nodes/tree/main/README.md#darker-color-mode)  
Lighten Modes: [Lighten](https://github.com/chrisfreilich/virtuoso-nodes/tree/main/README.md#lighten-mode), [Screen](https://github.com/chrisfreilich/virtuoso-nodes/tree/main/README.md#screen-mode)

### Normal Mode
![Normal Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/fd400439-51f3-40a0-b5a3-2c7ff3d78f61)

### Dissolve Mode *(not terribly useful on its own, used here with a second screen blend mode)*
![Dissolve Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/783ac2aa-7532-4ca2-a1ef-78ba5aa7d4fd)

### Darken Mode  
![Darken Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/c4dc2918-d346-4731-94a8-da6920ea75e3)

### Multiply Mode  
![Multiply Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/8b49c096-d189-4228-a297-fcf72260e6f5)

### Color Burn Mode
![Color Burn Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/011a398a-4f64-46d6-ad2c-6359c1e88d3a)

### Linear Burn Mode
![Linear Burn Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/776201fd-b49f-4c42-b4aa-f03a9458b817)

### Darker Color Mode
![Darker Color Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/0c5be8f6-a761-4fa5-8484-eca6102a7b80)

### Lighten Mode
![Lighten Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/ac05104d-6d64-4084-a44c-a78b51745ce9)

### Screen Mode
![Screen Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/594b788d-49f4-4bfc-8b9d-445e2436f6d9)

**Difference Mode**
![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/02e939ab-fcd1-4f05-a5ce-8a333a32cf9e)

**Exclusion Mode**  
![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/2bd9f600-160c-4087-b2c7-ae0285bb6b3e)

**Soft Light Mode**
![Soft Light Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/079c6d67-faef-47ca-9835-27b1c1234dfb)



**Dodge Mode**
![Dodge Blending Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/747899e7-896d-49cc-af4f-8c914bb3ea8c)

**Addition (aka Linear Dodge) Mode**
![Addition Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/1d6c94c5-6b52-4a1f-a99b-f12b535d478c)







**Hard Light Mode**
![Hard Light Blending Mode example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/97eccf07-2369-4cae-bd24-0b035fb3fbbf)

**Subtract Mode**  
![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/566b19ea-663e-4a8e-9924-85e2e213a67d)

**Grain Extract Mode**  
![Grain Extract Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/13880223-3653-4eaa-b1e7-371c8fe07fc5)

**Grain Merge Mode**
![Grain Merge Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/0e1691e1-e92d-4282-8989-ac9e8281120e)

**Divide Mode**  
![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/14100f42-b5a4-4be3-8a61-cde77b53e65c)

**Overlay Mode**  
![Overlay Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/de63d31c-99e9-434c-ad97-84767f9cac09)

