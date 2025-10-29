#!/usr/bin/env python3

import argparse
import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

dpi = 800


def pdf_to_image(pdf_path):
    return convert_from_path(pdf_path, dpi=dpi)


def clamp(image, threshold=128):
    if image.mode != "L":
        image = image.convert("L")

    # image.point(lambda x: 0 if x < threshold else 255, mode="1")
    return image


def simplify(image, size=2, iterations=1):
    array = np.array(image)

    kernel = np.ones((size, size), np.uint8)

    # for i in range(passes):
    array = cv2.dilate(array, kernel, iterations=iterations)
    # for i in range(passes):
    array = cv2.erode(array, kernel, iterations=iterations)

    return Image.fromarray(array)


def quantify_darkness(image):
    if image.mode != "L":
        image = image.convert("L")

    array = np.array(image)

    return 255 - np.mean(array)


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
    parser.add_argument("--output-dir", "-o", default=".", help="Directory to save output images")
    parser.add_argument("--size", type=int, default=2, help="Kernel size for erosion")
    parser.add_argument("--iterations", type=int, default=1, help="iterations for erosion")

    args = parser.parse_args()

    # Get the PDF filename for use in output naming
    pdf_filename = os.path.basename(args.pdf_path)

    pages = pdf_to_image(args.pdf_path)

    page = pages[0]

    page = clamp(page)
    page = simplify(page, args.size, iterations=args.iterations)

    # Quantify darkness for each page
    darkness = quantify_darkness(page)
    print(f"Darkness score: {darkness:.4f}")

    save_images([page], args.output_dir, pdf_filename)


if __name__ == "__main__":
    main()
