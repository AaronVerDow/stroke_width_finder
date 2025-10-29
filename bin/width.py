#!/usr/bin/env python3

import argparse
import os
from pdf2image import convert_from_path
from PIL import Image

dpi = 200


def pdf_to_image(pdf_path):
    return convert_from_path(pdf_path, dpi=dpi)


def clamp(image, threshold=128):
    if image.mode != "L":
        image = image.convert("L")

    return image.point(lambda x: 0 if x < threshold else 255, mode="1")


def save_images(images, output_dir, pdf_filename):
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(pdf_filename)[0]

    for i, image in enumerate(images):
        filename = f"{base_name}_page_{i+1}.png"
        filepath = os.path.join(output_dir, filename)
        image.save(filepath)
        print(f"Saved: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Check line width")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument(
        "--output-dir", "-o", default=".", help="Directory to save output images (default: current directory)"
    )

    args = parser.parse_args()

    # Get the PDF filename for use in output naming
    pdf_filename = os.path.basename(args.pdf_path)

    pages = pdf_to_image(args.pdf_path)

    processed_pages = []
    for page in pages:
        processed_page = clamp(page)
        processed_pages.append(processed_page)

    save_images(processed_pages, args.output_dir, pdf_filename)


if __name__ == "__main__":
    main()
