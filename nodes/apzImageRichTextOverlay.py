# main_class.py

from ..utils.apz_text_box_utility import TextBoxUtility
from ..utils.apz_color_utility import ColorUtility
from ..utils.apz_font_loader_utility import FontLoaderUtility
from ..utils.apz_text_renderer_utility import TextRendererUtility
from ..utils.apz_image_conversion import tensor_to_pil, pil_to_single_tensor
from ..utils.apz_font_manager import FontManager

class APZmediaImageRichTextOverlay:
    def __init__(self, device="cpu"):
        print("APZmediaImageRichTextOverlay initialized")
        self.device = device

    # _alignments, INPUT_TYPES, RETURN_TYPES, FUNCTION, CATEGORY remain unchanged

    def apz_add_text_overlay(self, image, theText, theTextbox_width, theTextbox_height, max_font_size, font, italic_font, bold_font, alignment, vertical_alignment, font_color, italic_font_color, bold_font_color, box_start_x, box_start_y, padding, line_height_ratio):
        original_shape = image.shape
        original_dtype = image.dtype

        pil_images = tensor_to_pil(image)
        print(f"Input Tensor Shape: {image.shape}")

        color_utility = ColorUtility()
        font_color_rgb = color_utility.hex_to_rgb(font_color)
        italic_font_color_rgb = color_utility.hex_to_rgb(italic_font_color)
        bold_font_color_rgb = color_utility.hex_to_rgb(bold_font_color)

        font_manager = FontManager(font, italic_font, bold_font, max_font_size)
        font_loader = FontLoaderUtility(font_manager, max_font_size)

        processed_images = []
        for idx, image_pil in enumerate(pil_images):
            print(f"Processing Image {idx + 1}/{len(pil_images)}")

            effective_textbox_width = theTextbox_width - 2 * padding
            effective_textbox_height = theTextbox_height - 2 * padding

            font_size, wrapped_lines, total_text_height = font_loader.find_fitting_font_size(theText, effective_textbox_width, effective_textbox_height, line_height_ratio)

            if font_size:
                draw = ImageDraw.Draw(image_pil)
                TextRendererUtility.render_text(
                    draw, wrapped_lines, box_start_x, box_start_y, padding,
                    effective_textbox_width, effective_textbox_height, font_manager,
                    color_utility, alignment, vertical_alignment, line_height_ratio,
                    font_color_rgb, italic_font_color_rgb, bold_font_color_rgb
                )

            processed_image = pil_to_single_tensor(image_pil)
            print(f"Processed PIL image to tensor shape: {processed_image.shape}")
            processed_images.append(processed_image)

        processed_image = torch.cat(processed_images, dim=0)
        print(f"Final output tensor shape: {processed_image.shape}")

        processed_image = processed_image.to(original_dtype)

        return processed_image,
