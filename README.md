# Image Hash Spoofing Tool
## Description
This tool allows an image file to be modified until its hash starts with a given hexadecimal prefix, while keeping the image visually identical to the human eye.

## Features
- Accepts any image file (e.g., JPEG, PNG).
- Outputs an altered image with a hash starting with the specified prefix.
- Ensures the altered image remains visually identical to the original.

## Prerequisites

- Python 3.8 or higher
- Pillow library (Python Imaging Library fork)

## Installation
1. Clone the repository
```bash
git clone https://github.com/lkendi/ImageHashSpoofing.git
cd ImageHashSpoofing
```

2. Create a virtual environment and activate it
```bash
python3 -m venv env
source env/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage
Run the tool from the command line
```bash
./spoof <hex_prefix> <input_image> <output_image>
```

Example
```bash
./spoof 0x20 original.jpg altered.jpg
```
## File Structure

-   `spoof.py`: Entry point.
-   `spoofing/`: Contains core functionality.
-   `tests/`: Unit tests.
-   `images/`: Contains input and output images.

## Testing
Run unit tests using 
```bash
python -m unittest discover tests/
```