# Virtuoso ComfyUI Blend Modes Node

This node extends the functionality of the built-in Blend node by including many more blend modes, and including a scaling option for the top layer.

**Difference Mode**
![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/02e939ab-fcd1-4f05-a5ce-8a333a32cf9e)

**Normal Mode (50% Opacity)**
![Normal Blending Mode example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/e9a16322-a1bb-425d-ad2c-3d69dfd4b887)

**Screen Mode**
![Screen Blending Mode example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/594b788d-49f4-4bfc-8b9d-445e2436f6d9)

**Soft Light Mode**
![Soft Light Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/079c6d67-faef-47ca-9835-27b1c1234dfb)

**Lighten Mode**
![Lighten Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/ac05104d-6d64-4084-a44c-a78b51745ce9)

**Dodge Mode**
![Dodge Blending Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/747899e7-896d-49cc-af4f-8c914bb3ea8c)

**Addition (aka Linear Dodge) Mode**
![Addition Mode Example](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/1d6c94c5-6b52-4a1f-a99b-f12b535d478c)

**Darken Only Mode**  
![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/f62c784f-63e8-4786-8fa1-b5ffe729fb4e)

**Multiply Mode**  
![image](https://github.com/chrisfreilich/virtuoso-nodes/assets/108036952/844852a1-a946-4c69-89d5-6f3bb6f40ef5)

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



### Node controls:

- backdrop: This is the background image. The output image will have the same dimensions as this image
- source: This is the top image. If it is not the same size as the backdrop image, it will be resized to cover the backdrop
- opacity: The opacity of the source image. (The backdrop image is 100% opacity) Opacity is a little weird with blend modes, so the effect might not be as you would expect.
- source_adjust: The method by which the source image will be resized if necessary.
     - Stretch will change each dimension just as much as needed to match that dimension, potentially changing the aspect ratio of the source image and causing distortion.
     - Crop will maintain the aspect ratio of the source image, and resize it until it just covers the backdrop image, then crop what doesn't fit.
- blend_mode: difference is the default, but all the common blending modes are available.

### Installation:

1. Git clone this repo into a folder in ComfyUI\custom_nodes
2. pip install -r requirements.txt

Please let me know if you have any thoughts or suggestions!
