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

# Importing custom nodes
try:
    from .nodes.apzImageRichTextOverlay import APZmediaImageRichTextOverlay
    logger.info("Successfully imported APZmediaImageRichTextOverlay node.")
except Exception as e:
    logger.error("Failed to import APZmediaImageRichTextOverlay node.", exc_info=True)

try:
    from .nodes.apzImageRichTextOverlayV2 import APZmediaImageRichTextOverlayV2
    logger.info("Successfully imported APZmediaImageRichTextOverlayV2 node.")
except Exception as e:
    logger.error("Failed to import APZmediaImageRichTextOverlayV2 node.", exc_info=True)

try:
    from .nodes.apzImageMarkdownTextOverlay import APZmediaImageMarkdownTextOverlay
    logger.info("Successfully imported APZmediaImageMarkdownTextOverlay node.")
except Exception as e:
    logger.error("Failed to import APZmediaImageMarkdownTextOverlay node.", exc_info=True)

NODE_CLASS_MAPPINGS = {
    # Primary node names (clean, no duplicates)
    "APZmediaImageRichTextOverlay": APZmediaImageRichTextOverlay,
    "APZmediaImageRichTextOverlayV2": APZmediaImageRichTextOverlayV2,
    "APZmediaImageMarkdownTextOverlay": APZmediaImageMarkdownTextOverlay,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # Clean display names (no duplicates)
    "APZmediaImageRichTextOverlay": "APZmedia Image Rich Text Overlay",
    "APZmediaImageRichTextOverlayV2": "APZmedia Image Rich Text Overlay V2",
    "APZmediaImageMarkdownTextOverlay": "APZmedia Image Markdown Text Overlay",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Additional setup, such as threading or other initializations, can be added here if necessary

logger.info("ComfyUI Text Tools extension has been loaded successfully.")
