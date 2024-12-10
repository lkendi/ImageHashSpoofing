#!/usr/bin/env python3
"""Module containing hashing-related utilities."""
import hashlib


def validate_hex_prefix(hex_prefix: str) -> None:
    """
    Validates if the input string is a proper hexadecimal prefix.

    Args:
        hex_prefix (str): Hexadecimal prefix to validate.

    Raises:
        ValueError: If the prefix is not valid.
    """
    if not hex_prefix.startswith("0x"):
        raise ValueError("Hex prefix must start with '0x'.")
    if not all(c in "0123456789abcdefABCDEF" for c in hex_prefix[2:]):
        raise ValueError("Hex prefix must contain only "
                         "hexadecimal characters.")


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
    return hash_value.startswith(hex_prefix[2:])
