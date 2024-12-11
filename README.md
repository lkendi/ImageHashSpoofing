# Image Hash Spoofing Tool

## **Description**

This tool modifies an image file until its hash begins with a specified hexadecimal prefix, while ensuring that the image remains visually identical to the original one.

## **Features**

-   Supports PNG and JPEG/JPG image formats.
-   Ensures output image remains visually identical to the original.
-   Efficiently computes hashes and modifies image metadata or unused byte space to achieve the desired hash.
-   Provides side-by-side visualization of the original and modified images.


## **Prerequisites**
-   **Python**: Version 3.8 or higher.
-   **Libraries**:
    -   [Pillow](https://pillow.readthedocs.io/): A Python Library for handling images.

## **Installation**

1.  Clone the repository:
    ```bash
    git clone https://github.com/lkendi/ImageHashSpoofing.git
    cd ImageHashSpoofing
    ```
2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```
3.  Install required dependencies:
    ```
    pip install -r requirements.txt
    ```

## **Usage**

Run the tool from the command line:

```bash
./spoof.py <hex_prefix> <input_image> <output_file_name>
```

### **Example**
```bash
./spoof.py 0x20 images/original.jpg images/altered.jpg
```

This command modifies the image `original.jpg` until its hash begins with `0x20`, then saves the modified image as `altered.jpg`.

### **How It Works**

1.  **Input Parsing**:

    -  A hex prefix (e.g., `0x20`), an input image file (PNG or JPEG), and an output filename are passed as command-line arguments.
    -  Both the hex prefix and image file are validated before proceeding to the next steps.

2.  **Image Modification and Hash Calculation**:

    -  After reading the input image, the image is continuously modified.
    -  Modifications are through changes to metadata fields (e.g., EXIF for JPEG, text chunks for PNG) or by appending padding bytes to ensure that visual integrity is maintained.
    - After every iteration of the image modification, the hash of the modified image is calculated.
    - The hash is then checked to confirm whether it starts with the desired prefix.
    - This process stops when the hash begins with the specified prefix or the maximum attempts are reached.

3.  **Output**:

    -   The modified image file, with the required hash prefix.
    -   Final hash and processing details.


## File Structure
-   `src/`:

    -   `spoof.py`: Entry point for the tool.
    -   `utils/`:
        -   `hash_utils.py`: Handles hash-related functions.
        -   `image_utils.py`: Contains image manipulation functions.
    -   `images/`: Directory for input and output images.

-   `tests/`: Contains unit tests for the tool.

## **Testing**

Run the unit tests using:

```bash
python -m unittest discover tests/
```

___

## **Acknowledgments**

- This tool uses the Python Pillow and hashlib libraries.
- All images were sourced from [Pixabay](https://pixabay.com/).
