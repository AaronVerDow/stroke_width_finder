#!/usr/bin/env python3

import argparse
from pdf2image import convert_from_path
from PIL import Image

dpi = 200


def pdf_to_image(pdf_path):
    return convert_from_path(pdf_path, dpi=dpi)


def clamp(image, threshold=128):
    if image.mode != "L":
        image = image.convert("L")

    return image.point(lambda x: 0 if x < threshold else 255, mode="1")


def main():
    parser = argparse.ArgumentParser(description="Check line width")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    args = parser.parse_args()
    pages = pdf_to_image(args.pdf_path)
    for page in pages:
        image = clamp(page)


if __name__ == "__main__":
    main()
