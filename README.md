# Virtuoso ComfyUI Blend Modes Node

![Blend Mode Example Image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/868f4c58-f7c8-44f3-b537-6c34b38b18db)

This is my first go at a custom Comfy node. I figured it would be useful to have a simple image difference node to see the effects of whatever process you're analyzing. Once that was done I figured why not allow any of the blend modes? So here it is!

Very simple controls:

- backdrop: This is the background image. The output image will have the same dimensions as this image
- source: This is the top image. If it is not the same size as the backdrop image, it will be resized to cover the backdrop
- opacity: The opacity of the source image. (The backdrop image is 100% opacity) Opacity is a little weird with blend modes, so the effect might not be as you would expect.
- source_adjust: The method by which the source image will be resized if necessary.
     - Stretch will change each dimension just as much as needed to match that dimension, potentially changing the aspect ratio of the source image and causing distortion.
     - Crop will maintain the aspect ratio of the source image, and resize it until it just covers the backdrop image, then crop what doesn't fit.
- blend_mode: difference is the default, but all the common blending modes are available.

  Installation:

  1. Git clone this repo into a folder in ComfyUI\custom_nodes
  2. pip install -r requirements.txt
 
  Please let me know if you have any thoughts or suggestions!
