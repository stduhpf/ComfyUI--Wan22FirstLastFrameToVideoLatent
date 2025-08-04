import torch
import nodes
import comfy.utils
import comfy.model_management
import comfy.latent_formats

class Wan22FirstLastFrameToVideoLatent:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"vae": ("VAE", ),
                             "width": ("INT", {"default": 832, "min": 16, "max": nodes.MAX_RESOLUTION, "step": 16}),
                             "height": ("INT", {"default": 480, "min": 16, "max": nodes.MAX_RESOLUTION, "step": 16}),
                             "length": ("INT", {"default": 81, "min": 1, "max": nodes.MAX_RESOLUTION, "step": 4}),
                             "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
                },
                "optional": {"start_image": ("IMAGE", ),
                             "end_image": ("IMAGE", ),
                }}

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    FUNCTION = "encode"

    CATEGORY = "conditioning/video_models"

    def encode(self, vae, width, height, length, batch_size, start_image=None, end_image=None):
        latent = torch.zeros([1, 48, ((length - 1) // 4) + 1, height // 16, width // 16], device=comfy.model_management.intermediate_device())
        if start_image is None and end_image is None:
            out_latent = {}
            out_latent["samples"] = latent
            return (out_latent,)
        if start_image is not None:
            start_image = comfy.utils.common_upscale(start_image[:length].movedim(-1, 1), width, height, "bilinear", "center").movedim(1, -1)
        if end_image is not None:
            end_image = comfy.utils.common_upscale(end_image[-length:].movedim(-1, 1), width, height, "bilinear", "center").movedim(1, -1)

        mask = torch.ones([latent.shape[0], 1, ((length - 1) // 4) + 1, latent.shape[-2], latent.shape[-1]], device=comfy.model_management.intermediate_device())

        if start_image is not None:
            latent_temp = vae.encode(start_image)
            latent[:, :, :latent_temp.shape[-3]] = latent_temp
            mask[:, :, :latent_temp.shape[-3]] *= 0.0

        if end_image is not None:
            latent_temp = vae.encode(end_image)
            latent[:, :, -latent_temp.shape[-3]:] = latent_temp
            mask[:, :, -latent_temp.shape[-3]:] *= 0.0




        out_latent = {}
        latent_format = comfy.latent_formats.Wan22()
        latent = latent_format.process_out(latent) * mask + latent * (1.0 - mask)
        out_latent["samples"] = latent.repeat((batch_size, ) + (1,) * (latent.ndim - 1))
        out_latent["noise_mask"] = mask.repeat((batch_size, ) + (1,) * (mask.ndim - 1))
        return (out_latent,)

class Wan22FirstLastFrameToVideoLatentTiledVAE:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"vae": ("VAE", ),
                             "width": ("INT", {"default": 832, "min": 16, "max": nodes.MAX_RESOLUTION, "step": 16}),
                             "height": ("INT", {"default": 480, "min": 16, "max": nodes.MAX_RESOLUTION, "step": 16}),
                             "length": ("INT", {"default": 81, "min": 1, "max": nodes.MAX_RESOLUTION, "step": 4}),
                             "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),

                            "tile_size": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 64}),
                            "overlap": ("INT", {"default": 64, "min": 0, "max": 4096, "step": 32}),
                            "temporal_size": ("INT", {"default": 64, "min": 8, "max": 4096, "step": 4, "tooltip": "Amount of frames to encode at a time."}),
                            "temporal_overlap": ("INT", {"default": 8, "min": 4, "max": 4096, "step": 4, "tooltip": "Amount of frames to overlap."})
                },
                "optional": {"start_image": ("IMAGE", ),
                             "end_image": ("IMAGE", ),
                }}

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    FUNCTION = "encode"

    CATEGORY = "conditioning/video_models"

    def encode(self, vae, width, height, length, batch_size,  tile_size, overlap, temporal_size=64, temporal_overlap=8, start_image=None, end_image=None):
        latent = torch.zeros([1, 48, ((length - 1) // 4) + 1, height // 16, width // 16], device=comfy.model_management.intermediate_device())
        if start_image is None and end_image is None:
            out_latent = {}
            out_latent["samples"] = latent
            return (out_latent,)
        if start_image is not None:
            start_image = comfy.utils.common_upscale(start_image[:length].movedim(-1, 1), width, height, "bilinear", "center").movedim(1, -1)
        if end_image is not None:
            end_image = comfy.utils.common_upscale(end_image[-length:].movedim(-1, 1), width, height, "bilinear", "center").movedim(1, -1)

        mask = torch.ones([latent.shape[0], 1, ((length - 1) // 4) + 1, latent.shape[-2], latent.shape[-1]], device=comfy.model_management.intermediate_device())

        if start_image is not None:
            latent_temp = vae.encode(start_image, tile_x=tile_size, tile_y=tile_size, overlap=overlap, tile_t=temporal_size, overlap_t=temporal_overlap)
            latent[:, :, :latent_temp.shape[-3]] = latent_temp
            mask[:, :, :latent_temp.shape[-3]] *= 0.0

        if end_image is not None:
            latent_temp = vae.encode(end_image, tile_x=tile_size, tile_y=tile_size, overlap=overlap, tile_t=temporal_size, overlap_t=temporal_overlap)
            latent[:, :, -latent_temp.shape[-3]:] = latent_temp
            mask[:, :, -latent_temp.shape[-3]:] *= 0.0




        out_latent = {}
        latent_format = comfy.latent_formats.Wan22()
        latent = latent_format.process_out(latent) * mask + latent * (1.0 - mask)
        out_latent["samples"] = latent.repeat((batch_size, ) + (1,) * (latent.ndim - 1))
        out_latent["noise_mask"] = mask.repeat((batch_size, ) + (1,) * (mask.ndim - 1))
        return (out_latent,)
