#!/usr/bin/env python3
"""
Unittests module for the hash_utils module.

This script contains test cases to validate the functionality of utility
functions used for handling image hashing and hash prefix validation.
"""
import os
from PIL import Image
from src.utils.hash_utils import (
    validate_hex_prefix,
    calculate_image_hash,
    compare_hash_prefix,
)
import unittest
from unittest.mock import patch


class TestHashUtils(unittest.TestCase):
    """
    Unittests class for the src/utils/hash_utils module.

    It includes tests for validating hex prefixes, calculating image hashes,
    and comparing hash prefixes for matches.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by creating temporary image files.

        Creates dummy JPG and PNG images in the working directory for use
        in tests.
        """
        self.mock_image_path: str = "test.jpg"
        self.mock_png_image_path: str = "test.png"

        self.mock_image: Image.Image = Image.new("RGB", (100, 100), "white")
        self.mock_image.save(self.mock_image_path, "JPEG")

        self.mock_png_image: Image.Image = Image.new("RGB", (100, 100), "blue")
        self.mock_png_image.save(self.mock_png_image_path, "PNG")

    def tearDown(self) -> None:
        """
        Clean up the test environment by removing temporary image files.

        Deletes the dummy images created during the setup phase.
        """
        if os.path.exists(self.mock_image_path):
            os.remove(self.mock_image_path)
        if os.path.exists(self.mock_png_image_path):
            os.remove(self.mock_png_image_path)

    def test_validate_hex_prefix_valid(self) -> None:
        """Test that valid hex prefixes are accepted without errors."""
        validate_hex_prefix("0xabc123")

    def test_validate_hex_prefix_invalid_no_prefix(self) -> None:
        """Test that missing '0x' prefix raises a ValueError."""
        with self.assertRaises(ValueError):
            validate_hex_prefix("123")

    def test_validate_hex_prefix_invalid_characters(self) -> None:
        """Test that invalid characters in the hex prefix
        raise a ValueError."""
        with self.assertRaises(ValueError):
            validate_hex_prefix("0x12g!")

    def test_validate_hex_prefix_too_long(self) -> None:
        """Test that hex prefixes exceeding the maximum length
        raise a ValueError."""
        with self.assertRaises(ValueError):
            validate_hex_prefix("0x" + "a" * 65)

    @patch("PIL.Image.open")
    def test_calculate_image_hash_valid_jpg(self, mock_open) -> None:
        """
        Test that a valid hash is returned for a JPG image.

        Args:
            mock_open (patch): Mocked version of PIL.Image.open.
        """
        mock_open.return_value = self.mock_image
        algorithm = "sha256"
        hash_value = calculate_image_hash(self.mock_image_path, algorithm)
        self.assertIsInstance(hash_value, str)
        self.assertEqual(len(hash_value), 64)

    @patch("PIL.Image.open")
    def test_calculate_image_hash_valid_png(self, mock_open) -> None:
        """
        Test that a valid hash is returned for a PNG image.

        Args:
            mock_open (patch): Mocked version of PIL.Image.open.
        """
        mock_open.return_value = self.mock_png_image
        algorithm = "sha256"
        hash_value = calculate_image_hash(self.mock_png_image_path, algorithm)
        self.assertIsInstance(hash_value, str)
        self.assertEqual(len(hash_value), 64)

    def test_calculate_image_hash_invalid_file(self) -> None:
        """Test that a ValueError is raised for an invalid file path."""
        with self.assertRaises(ValueError):
            calculate_image_hash("nonexistent_file.jpg", "sha256")

    def test_compare_hash_prefix_match(self) -> None:
        """Test that hash prefixes are correctly identified as matching."""
        hash_value = "abc123"
        hex_prefix = "0xabc"
        self.assertTrue(compare_hash_prefix(hash_value, hex_prefix))

    def test_compare_hash_prefix_no_match(self) -> None:
        """Test that hash prefixes are correctly identified as not matching."""
        hash_value = "abc123"
        hex_prefix = "0xdef"
        self.assertFalse(compare_hash_prefix(hash_value, hex_prefix))

    def test_compare_hash_prefix_case_insensitivity(self) -> None:
        """Test that hash prefix comparison is case-insensitive."""
        hash_value = "ABC123"
        hex_prefix = "0xabc"
        self.assertTrue(compare_hash_prefix(hash_value, hex_prefix))


if __name__ == "__main__":
    unittest.main()
