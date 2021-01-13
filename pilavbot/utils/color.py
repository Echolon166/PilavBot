import math

from discord import Color

from constants import *


def mix_colors(start_color, final_color, ratio=0.5):
    """Given two colors, mix their values by proportions weighted by percentage.

    Args:
        start_color (discord.Color): Starter color of the color mix.
        final_color (discord.Color): Expected final color of the color mix.
        ratio (float): Ratio of the color mix.

    Returns:
        discord.Color: Color mix which obtained from given colors.
    """

    start_color_tuple = start_color.to_rgb()
    final_color_tuple = final_color.to_rgb()

    mixed_color = []

    # Mix the R, G, and B components
    for int1, int2 in zip(start_color_tuple, final_color_tuple):
        mixed_color.append(int(int1 * (1 - ratio) + int2 * ratio))

    return Color.from_rgb(*mixed_color)


def gradient(*colors, percentage=100):
    """Given many discord.Colors and a percentage, mix them together as if on a linear gradient.

    Args:
        colors (discord.Color): Colors to be mixed together to create the gradient.
        percentage (int): The higher the percentage, the more of the final color listed appears 
            and vice versa for lower percentages.

    Returns:
        discord.Color: Color gradient which obtained from given colors.
    """

    # Range between 0 - 100
    percentage = max(0, min(percentage, 100))

    # Determine which two colors to mix
    size = 100 / (len(colors) - 1)
    start_color_index = 0

    # Find where on the gradient the percentage is
    while size * (start_color_index + 1) < percentage:
        start_color_index += 1

    mix_ratio = (percentage - size * start_color_index) / size

    start_color = colors[start_color_index]
    final_color = colors[start_color_index + 1]
    return mix_colors(start_color, final_color, mix_ratio)
