from .nodes_wan import *

NODE_CLASS_MAPPINGS = {
    "Wan22FirstLastFrameToVideoLatent": Wan22FirstLastFrameToVideoLatent,
    "Wan22FirstLastFrameToVideoLatentTiledVAE": Wan22FirstLastFrameToVideoLatentTiledVAE,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Wan22FirstLastFrameToVideoLatent": "Wan22FirstLastFrameToVideoLatent",
    "Wan22FirstLastFrameToVideoLatentTiledVAE": "Wan22FirstLastFrameToVideoLatent (Tiled VAE encode)",
}
