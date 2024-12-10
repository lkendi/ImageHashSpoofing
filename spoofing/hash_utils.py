#!/usr/bin/env python3
"""Module that contains hashing-related utilities"""
import hashlib

def validate_hex_prefix(hex_prefix: str) -> None:
    """
    Checks if the input string is a valid hexadecimal prefix.

    Args:
        hex_prefix (str) - String to check.

    Raises:
        ValueError: If the string is not a valid hexadecimal prefix.
    """
    if not hex_prefix.startswith("0x"):
        raise ValueError("Hex prefix must start with '0x'")
    
def calculate_hash(image_path: str) -> str:
    """
    Calculates the SHA-512 hash of an image file.

    Args:
        image_path (str) - Path to the image file.

    Returns:
        SHA-512 hash of the image file.
    """
    with open(image_path, 'rb') as file:
        file_content = file.read()
    return hashlib.sha512(file_content).hexdigest()


def compare_hash_prefix(hash_value: str, hex_prefix: str) -> bool:
    """
    Compares a hash value with a hex prefix.

    Args:
        hash_value (str) - Hash value.
        hex_prefix (str) - Hex prefix to compare.

    Returns:
        True if the hash value starts with the hex prefix, else False.
    """
    return hash_value.startswith(hex_prefix)
