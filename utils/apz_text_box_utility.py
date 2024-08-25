# apz_text_box_utility.py

class TextBoxUtility:
    @staticmethod
    def calculate_initial_y(vertical_alignment, box_start_y, padding, effective_textbox_height, total_text_height):
        if vertical_alignment == "top":
            return box_start_y + padding
        elif vertical_alignment == "bottom":
            return box_start_y + effective_textbox_height - total_text_height - padding
        else:  # "middle"
            return box_start_y + padding + (effective_textbox_height - total_text_height) // 2

    @staticmethod
    def calculate_initial_x(alignment, box_start_x, padding, effective_textbox_width, line, font):
        line_width = font.getbbox(line)[2] - font.getbbox(line)[0]
        if alignment == "left":
            return box_start_x + padding
        elif alignment == "right":
            return box_start_x + effective_textbox_width - line_width + padding
        else:  # "center"
            return box_start_x + padding + (effective_textbox_width - line_width) // 2
