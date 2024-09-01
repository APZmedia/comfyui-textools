# utils/apz_box_utility.py

class BoxUtility:
    @staticmethod
    def calculate_effective_dimensions(theTextbox_width, theTextbox_height, padding):
        effective_textbox_width = theTextbox_width - 2 * padding
        effective_textbox_height = theTextbox_height - 2 * padding
        return effective_textbox_width, effective_textbox_height

    @staticmethod
    def calculate_box_coordinates(box_start_x, box_start_y, theTextbox_width, theTextbox_height):
        box_left = box_start_x
        box_top = box_start_y
        box_right = box_start_x + theTextbox_width
        box_bottom = box_start_y + theTextbox_height
        return box_left, box_top, box_right, box_bottom

    @staticmethod
    def draw_bounding_box(draw, box_left, box_top, box_right, box_bottom, bounding_box_rgb, box_background_rgb, line_width):
        # Draw filled background box
        draw.rectangle([box_left, box_top, box_right, box_bottom], fill=box_background_rgb)
        # Draw the outline box with specified line opacity
        draw.rectangle([box_left, box_top, box_right, box_bottom], outline=bounding_box_rgb, width=line_width)
