#!/usr/bin/env python3

import argparse
from pdf2image import convert_from_path

dpi = 200


def pdf_to_image(pdf_path):
    pages = convert_from_path(pdf_path, dpi=dpi)


def main():
    parser = argparse.ArgumentParser(description="Check line width")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    args = parser.parse_args()
    pdf_to_image(args.pdf_path)


if __name__ == "__main__":
    main()
