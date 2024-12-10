#!/usr/bin/env python3
"""Unittests module"""
import unittest
from PIL import Image
import os
from utils.image_utils import read_image, modify_image
from utils.image_utils import display_images_side_by_side
from unittest.mock import patch


class TestImageUtils(unittest.TestCase):
    """
    Unittests for the spoofing/image_utils module.
    """
    def setUp(self):
        self.image_path = "test_images/test_img.png"
        self.modified_image_path = "test_images/modified_test.png"
        os.makedirs("test_images", exist_ok=True)

        self.image = Image.new("RGB", (128, 128), color="blue")
        self.image.save(self.image_path, format="PNG")
        self.image = Image.open(self.image_path)

    def tearDown(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        if os.path.exists(self.modified_image_path):
            os.remove(self.modified_image_path)
        if os.path.exists("test_images"):
            os.rmdir("test_images")

    def test_read_image_valid(self):
        image = read_image(self.image_path)
        self.assertEqual(image.size, (128, 128))
        self.assertEqual(image.format, "PNG")

    def test_read_image_non_existent(self):
        with self.assertRaises(ValueError):
            read_image("non_existent.png")

    def test_read_image_invalid_file(self):
        with open("test_images/invalid.txt", "w") as file:
            file.write("This is not an image.")
        with self.assertRaises(ValueError):
            read_image("test_images/invalid.txt")
        os.remove("test_images/invalid.txt")

    def test_modify_image_png(self):
        modify_image(self.image, self.modified_image_path, iteration=1)
        self.assertTrue(os.path.exists(self.modified_image_path))

    def test_modify_image_invalid_format(self):
        invalid_image = Image.new("RGB", (100, 100), color="red")
        invalid_image.format = "GIF"
        with self.assertRaises(ValueError):
            modify_image(invalid_image, self.modified_image_path, iteration=1)

    def test_modify_image_adds_padding(self):
        modify_image(self.image, self.modified_image_path,
                     iteration=2, use_padding=True)
        with open(self.modified_image_path, "rb") as file:
            content = file.read()
        self.assertIn(b"padding_2", content)

    @patch("PIL.Image.Image.show")
    def test_display_images_side_by_side(self, mock_show):
        modify_image(self.image, self.modified_image_path, iteration=1)
        display_images_side_by_side(self.image_path, self.modified_image_path)
        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
