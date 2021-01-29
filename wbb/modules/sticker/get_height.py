async def get_y_and_heights(
    text_wrapped,
    dimensions,
    margin,
    font
):
    _, descent = font.getmetrics()
    line_heights = [
        font.getmask(
            text_line,
        ).getbbox()[3] + descent + margin for text_line in text_wrapped
    ]
    line_heights[-1] -= margin
    height_text = sum(line_heights)
    y = (dimensions[1] - height_text) // 2
    return y, line_heights
