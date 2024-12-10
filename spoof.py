#!/usr/bin/env python3
"""Main script for image hash spoofing."""
import sys
import time
from spoofing.hash_utils import validate_hex_prefix
from spoofing.hash_utils import calculate_image_hash, compare_hash_prefix
from spoofing.image_utils import read_image, modify_image
from spoofing.image_utils import display_images_side_by_side

def update_progress_message(current: int, total: int) -> None:
    """
    Prints a simple message showing the current iteration out of total attempts.

    Args:
        current (int): The current number of iterations.
        total (int): The total number of iterations.
    """
    print(f"Attempt {current}/{total}: Working...", end="\r")


def spoof():
    """
    Modifies an image to generate a hash that begins with a specified
    hexadecimal prefix.

    The image is continuously modified until its hash begins with the
    prefix or the maximum number of attempts is reached.

    Args:
        hex_prefix (str): The hexadecimal prefix to spoof.
        input_image (str): Path to the input image.
        output_image (str): Path to save the modified image.

    Returns:
        None
    """
    if len(sys.argv) != 4:
        print("Usage: ./spoof <hex-prefix> <input-image> <output-file-name>")
        sys.exit(1)

    hex_prefix, input_image, output_image = sys.argv[1:]
    validate_hex_prefix(hex_prefix)

    iteration, max_attempts = 0, 100000
    image = read_image(input_image)
    start_time = time.time()
    print("Starting spoofing process. This may take some time...")
    
    while iteration < max_attempts:
        try:
            modify_image(image, output_image, iteration)
            hash_value = calculate_image_hash(output_image)

            if compare_hash_prefix(hash_value, hex_prefix):
                elapsed_time = time.time() - start_time
                print(f"Success! Hash matches prefix '{hex_prefix}'.")
                print(f"Hash: {hash_value}")
                print(f"Output saved to: {output_image}")
                print(f"Time elapsed: {elapsed_time:.2f} seconds")
                display_images_side_by_side(input_image, output_image)
                return

            iteration += 1
            update_progress_message(iteration, max_attempts)

        except Exception as e:
            print(f"Error during iteration {iteration}: {e}")
            sys.exit(1)

    print(f"Failed to find a matching hash after {max_attempts} attempts.")
    sys.exit(1)


if __name__ == "__main__":
    spoof()
    print("Done!")
