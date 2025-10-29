#!/usr/bin/env python3

import argparse
import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import matplotlib.pyplot as plt

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


def process_pdf_with_iterations(pdf_path, threshold=1, size=2):
    darkness_values = []
    iteration_counts = []

    pages = pdf_to_image(pdf_path)
    page = pages[0]

    # Process with increasing iterations
    iterations = 1
    while True:
        # Apply processing
        processed_page = clamp(page)
        simplified_page = simplify(processed_page, size=size, iterations=iterations)

        # Quantify darkness
        darkness = quantify_darkness(simplified_page)

        darkness_values.append(darkness)
        iteration_counts.append(iterations)

        print(f"Iterations: {iterations}, Darkness: {darkness:.4f}")

        if darkness <= threshold:
            break

        iterations += 1

    return iteration_counts, darkness_values


def generate_graph(iteration_counts, darkness_values):
    """Generate graph with iterations on x-axis and darkness on y-axis"""
    plt.figure(figsize=(10, 6))
    plt.plot(iteration_counts, darkness_values, marker="o")
    plt.xlabel("Iteration Count")
    plt.ylabel("Darkness")
    plt.title("Darkness vs Iteration Count")
    plt.grid(True)
    plt.savefig("darkness_iterations.png")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Check line width")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument("--output-dir", "-o", default=".", help="Directory to save output images")
    parser.add_argument("--size", type=int, default=2, help="Kernel size for erosion")
    parser.add_argument("--iterations", type=int, default=1, help="iterations for erosion")
    parser.add_argument("--threshold", type=float, default=5.0, help="Darkness threshold")

    args = parser.parse_args()

    # Get the PDF filename for use in output naming
    pdf_filename = os.path.basename(args.pdf_path)

    # Process PDF with iterations until threshold is met
    iteration_counts, darkness_values = process_pdf_with_iterations(
        args.pdf_path, threshold=args.threshold, size=args.size
    )

    # Generate graph
    generate_graph(iteration_counts, darkness_values)

    print(f"Graph saved as 'darkness_iterations.png'")

    # Also save the final processed image
    pages = pdf_to_image(args.pdf_path)
    page = pages[0]

    page = clamp(page)
    page = simplify(page, args.size, iterations=iteration_counts[-1])

    save_images([page], args.output_dir, pdf_filename)


if __name__ == "__main__":
    main()
