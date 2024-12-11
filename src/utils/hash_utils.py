#!/usr/bin/env python3
"""Module containing hashing-related utilities."""
import hashlib


def validate_hex_prefix(hex_prefix: str, max_length: int = 16) -> None:
    """
    Validates if the input string is a proper hexadecimal prefix.

    Args:
        hex_prefix (str): Hexadecimal prefix to validate.
        max_length (int): Maximum allowable length for the hex portion.

    Raises:
        ValueError: If the prefix is not valid or exceeds the maximum length.
    """
    if not hex_prefix.startswith("0x"):
        raise ValueError("Hex prefix must start with '0x'.")
    hex_part = hex_prefix[2:]
    if not hex_part:
        raise ValueError("Hex prefix must not be empty after '0x'.")
    if len(hex_part) > max_length:
        raise ValueError(
            f"Hex prefix must not exceed {max_length} characters.")
    if not all(c in "0123456789abcdefABCDEF" for c in hex_part):
        raise ValueError(
            "Hex prefix must contain only hexadecimal characters.")


def calculate_image_hash(image_path: str, algorithm: str = "sha256") -> str:
    """
    Computes the hash of an image file using a specified algorithm.

    Args:
        image_path (str): Path to the image file.
        algorithm (str): Hashing algorithm to use.

    Returns:
        str: The hash of the image.
    """
    try:
        hasher = hashlib.new(algorithm)
        with open(image_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        raise ValueError(f"Error hashing file '{image_path}': {e}")


def compare_hash_prefix(hash_value: str, hex_prefix: str) -> bool:
    """
    Checks if a hash value starts with a given hex prefix.

    Args:
        hash_value (str): The full hash value.
        hex_prefix (str): The hex prefix to check against.

    Returns:
        bool: True if hash matches the prefix; False otherwise.
    """
    hash_value = hash_value.strip().lower()
    hex_prefix = hex_prefix[2:].strip().lower()
    return hash_value.startswith(hex_prefix)
