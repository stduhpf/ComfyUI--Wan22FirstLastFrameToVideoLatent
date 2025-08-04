# Wan22FirstLastFrameToVideoLatent for ComfyUI

This is a custom node for ComfyUI that can be used to generate videos from either a starting frame, an end frame or both; with the Wan2.2 5B model (which uses the new Wan2.2 VAE, unlike Wan 2.2 A14B model wich uses the old Wan2.1 VAE).

## Description

Wan22FirstLastFrameToVideoLatent is designed to be used just like the WanFirstLastFrameToVideo node in ComfyUI, with support for the Wan2.2 VAE.

There is also an alternative more experimental node called "Wan22FirstLastFrameToVideoLatent (Tiled VAE encode)" included in this extension. By using a tiled VAE, it significantly reduces the VRAM needed, making it more accessible for users with limited resources. I found it very useful for [ComfyUI-zluda](https://github.com/patientx/ComfyUI-Zluda), since the VAE is particularly VRAM-hungry there. It can be used as a drop in replacement for the other node.

If you want to take adventage tiled VAE encoding for other Wan Img2Vid workflows, see here: https://github.com/stduhpf/ComfyUI--WanImageToVideoTiled

## Installation

To install this node, follow these steps:

1. Clone this repository into your ComfyUI custom nodes directory.
2. Restart ComfyUI to load the new node.

```bash
git clone https://github.com/stduhpf/ComfyUI--Wan22FirstLastFrameToVideoLatent.git /path/to/ComfyUI/custom_nodes/Wan22FirstLastFrameToVideoLatent
```

## Usage

You need to connect the Wan2.2 VAE in the `vae` input.

You can then use it with just a start frame (functionally equivalent to the Wan22ImageToVideoLatent), or with just an end frame, or both a start frame and end frame. The base Wan2.2 5B model can handle all these cases just fine.

### Example:

![example workflow included](assets/example.webp)

## Acknowledgments

Most of the code is either copied or heavily inspired by the built-in `Wan22ImageToVideoLatent` and `WanFirstLastFrameToVideo` nodes. Credit goes to comfyanonymous, the original author.

## License

This project mostly contains code copy-pasted from ComfyUI, which is licenced under GPL3.0. Therefore it is also licenced under GPL 3.0. (see LICENCE file for more details)