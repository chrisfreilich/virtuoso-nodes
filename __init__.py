from .blend import Blend

NODE_CLASS_MAPPINGS = {
    "Blend": Blend
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Blend": "Blend Modes Node"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']