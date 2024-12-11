#!/usr/bin/env python3
"""Unittests for the image_utils module."""
import os
from PIL import Image
from src.utils.image_utils import (
    read_image,
    modify_image,
    display_images_side_by_side
)
import unittest
from unittest.mock import patch


class TestImageUtils(unittest.TestCase):
    """
    Unittests for the image_utils module.
    """

    def setUp(self):
        """
        Set up static file paths for testing.
        """
        self.image_path = "images/test.png"
        self.modified_image_path = "images/test_output.png"

        if not os.path.exists(self.image_path):
            raise FileNotFoundError(
                f"Test image not found at {self.image_path}.")

    def tearDown(self):
        """
        Clean up by removing the modified image if it exists.
        """
        if os.path.exists(self.modified_image_path):
            os.remove(self.modified_image_path)

    def test_read_image_valid(self):
        """Test reading a valid image."""
        image = read_image(self.image_path)
        self.assertIsNotNone(image, "Image should not be None.")
        self.assertEqual(image.format, "PNG")

    def test_read_image_non_existent(self):
        """Test that reading a non-existent image raises a ValueError."""
        with self.assertRaises(ValueError):
            read_image("non_existent.png")

    def test_read_image_invalid_file(self):
        """Test that reading an invalid file raises a ValueError."""
        invalid_path = "images/invalid.txt"
        with open(invalid_path, "w") as f:
            f.write("This is not an image.")

        try:
            with self.assertRaises(ValueError):
                read_image(invalid_path)
        finally:
            os.remove(invalid_path)

    def test_modify_image_png(self):
        """Test modifying a PNG image and saving metadata."""
        image = read_image(self.image_path)
        modify_image(image, self.modified_image_path, iteration=1)
        self.assertTrue(os.path.exists(self.modified_image_path),
                        "Modified image was not created.")

        with Image.open(self.modified_image_path) as img:
            self.assertEqual(img.format, "PNG")
            self.assertIn("metadata_1", img.info.values())

    def test_modify_image_invalid_format(self):
        """Test modifying an image with an unsupported format
        raises a ValueError."""
        invalid_image = Image.new("RGB", (100, 100), color="red")
        invalid_image.format = "GIF"

        with self.assertRaises(ValueError):
            modify_image(invalid_image, self.modified_image_path, iteration=1)

    def test_modify_image_with_padding(self):
        """Test modifying an image and adding padding."""
        image = read_image(self.image_path)
        modify_image(image, self.modified_image_path,
                     iteration=2, use_padding=True)

        with open(self.modified_image_path, "rb") as file:
            content = file.read()
        self.assertIn(b"padding_2", content)

    @patch("PIL.Image.Image.show")
    def test_display_images_side_by_side(self, mock_show):
        """Test displaying images side-by-side."""
        image = read_image(self.image_path)
        modify_image(image, self.modified_image_path, iteration=1)
        display_images_side_by_side(self.image_path, self.modified_image_path)
        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
