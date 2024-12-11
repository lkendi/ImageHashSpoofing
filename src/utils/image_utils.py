#!/usr/bin/env python3
"""Module containing image-related utilities."""
import os
from PIL import Image, PngImagePlugin


def read_image(image_path: str) -> Image.Image:
    """
    Reads and validates an image file.

    Args:
        image_path (str): Path to the image file.

    Returns:
        Image.Image: The loaded image.

    Raises:
        ValueError: If the file is not a valid image or unsupported format.
    """
    if not os.path.exists(image_path):
        raise ValueError(f"File '{image_path}' does not exist.")
    try:
        with Image.open(image_path) as img:
            format = img.format
            image_copy = img.copy()
            image_copy.format = format
        print(f"Image loaded: {image_path}")
        print("-----------------------------------------------------------")
        return image_copy
    except Exception as e:
        raise ValueError(f"Error loading image: {e}")


def modify_image(image: Image.Image, output_path: str,
                 iteration: int, use_padding=True) -> None:
    """
    Modifies an image by updating metadata and optionally adding padding.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the modified image.
        iteration (int): Iteration count for unique modifications.
        use_padding (bool): If True, adds padding to the file.
    """
    if image.format == "PNG":
        meta = PngImagePlugin.PngInfo()
        meta.add_text("iteration", f"metadata_{iteration}")
        image.save(output_path, pnginfo=meta, format="PNG")
    elif image.format in {"JPEG", "JPG"}:
        exif_data = image.getexif()
        exif_data[0x9286] = f"Iteration {iteration}"
        image.save(output_path, exif=exif_data.tobytes(), format="JPEG")
    else:
        raise ValueError(f"Unsupported image format: {image.format}")

    if use_padding:
        with open(output_path, "ab") as file:
            file.write(f"padding_{iteration}".encode())


def display_images_side_by_side(input_path: str, output_path: str) -> None:
    """
    Displays the original and modified images side-by-side.

    Args:
        input_path (str): Path to the original image.
        output_path (str): Path to the modified image.
    """
    image1 = Image.open(input_path).resize((400, 400))
    image2 = Image.open(output_path).resize((400, 400))

    total_width = image1.width + image2.width
    side_by_side = Image.new("RGB",
                             (total_width, max(image1.height, image2.height)))
    side_by_side.paste(image1, (0, 0))
    side_by_side.paste(image2, (image1.width, 0))

    print("Displaying images (original on left, modified on right):")
    side_by_side.show()
