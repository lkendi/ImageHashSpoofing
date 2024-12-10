#!/usr/bin/env python3
"""Unittests module"""
import unittest
from utils.hash_utils import compare_hash_prefix, validate_hex_prefix
from utils.hash_utils import calculate_image_hash


class TestHashUtils(unittest.TestCase):
    """
    Unittests for the spoofing/hash_utils module.
    """
    def test_validate_hex_prefix_valid(self):
        validate_hex_prefix("0xabc123")

    def test_validate_hex_prefix_invalid_no_prefix(self):
        with self.assertRaises(ValueError):
            validate_hex_prefix("123")

    def test_validate_hex_prefix_invalid_characters(self):
        with self.assertRaises(ValueError):
            validate_hex_prefix("0x12g!")

    def test_validate_hex_prefix_too_long(self):
        with self.assertRaises(ValueError):
            validate_hex_prefix("0x" + "a" * 65)

    def test_calculate_image_hash_valid_jpg(self):
        image_path = "tests/images/test.jpg"
        algorithm = "sha256"
        hash_value = calculate_image_hash(image_path, algorithm)
        self.assertIsInstance(hash_value, str)
        self.assertEqual(len(hash_value), 64)

    def test_calculate_image_hash_valid_png(self):
        image_path = "tests/images/test.png"
        algorithm = "sha256"
        hash_value = calculate_image_hash(image_path,algorithm)
        self.assertIsInstance(hash_value, str)
        self.assertEqual(len(hash_value), 64)

    def test_calculate_image_hash_invalid_file(self):
        with self.assertRaises(ValueError):
            calculate_image_hash("nonexistent_file.jpg", "sha256")

    def test_compare_hash_prefix_match(self):
        hash_value = "abc123"
        hex_prefix = "0xabc"
        self.assertTrue(compare_hash_prefix(hash_value, hex_prefix))

    def test_compare_hash_prefix_no_match(self):
        hash_value = "abc123"
        hex_prefix = "0xdef"
        self.assertFalse(compare_hash_prefix(hash_value, hex_prefix))

    def test_compare_hash_prefix_case_insensitivity(self):
        hash_value = "ABC123"
        hex_prefix = "0xabc"
        self.assertTrue(compare_hash_prefix(hash_value, hex_prefix))


if __name__ == "__main__":
    unittest.main()
