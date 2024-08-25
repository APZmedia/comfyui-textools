"""
@author: Pablo Apiolazza
@title: ComfyUI APZmedia Text Tools
@nickname: ComfyUI Text Tools
@description: This extension provides rich text overlay functionalities, color management, and text parsing utilities for ComfyUI.
"""

import os
import sys
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the path to the current directory and subdirectories
comfyui_texttools_path = os.path.dirname(os.path.realpath(__file__))
nodes_path = os.path.join(comfyui_texttools_path, "nodes")

# Ensure the nodes path is added to sys.path for importing custom nodes
sys.path.append(nodes_path)

# Importing custom nodes
try:
    from .nodes.apzImageRichTextOverlay import APZmediaImageRichTextOverlay
    logger.info("Successfully imported APZmediaImageRichTextOverlay node.")
except Exception as e:
    logger.error("Failed to import APZmediaImageRichTextOverlay node.", exc_info=True)

# Utilities should be imported as needed, but not registered as nodes
try:
    from .utils import apz_font_manager
    from .utils import apz_rich_text_parser
    from .utils import apz_image_conversion
    from .utils import apz_text_wrapper
    logger.info("Successfully imported utility modules.")
except Exception as e:
    logger.error("Failed to import utility modules.", exc_info=True)

NODE_CLASS_MAPPINGS = {
    "APZmediaImageRichTextOverlay": APZmediaImageRichTextOverlay,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APZmediaImageRichTextOverlay": "APZmedia Image Rich Text Overlay",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Additional setup, such as threading or other initializations, can be added here if necessary

logger.info("ComfyUI Text Tools extension has been loaded successfully.")
