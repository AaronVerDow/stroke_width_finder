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


def find_biggest_change(darkness_values):
    """Find the biggest change in darkness values"""
    if len(darkness_values) < 2:
        return 0, 0

    max_change = 0
    max_change_index = 0

    for i in range(1, len(darkness_values)):
        change = abs(darkness_values[i] - darkness_values[i - 1])
        if change > max_change:
            max_change = change
            max_change_index = i

    return max_change_index, max_change


def generate_graph(iteration_counts, darkness_values, output_dir, pdf_filename):
    base_name = os.path.splitext(pdf_filename)[0]
    filename = f"{base_name}_graph.png"
    filepath = os.path.join(output_dir, filename)

    plt.figure(figsize=(10, 6))
    plt.plot(iteration_counts, darkness_values, marker="o")

    # Find biggest change and circle it in red
    max_change_index, max_change = find_biggest_change(darkness_values)
    if max_change_index > 0:
        plt.scatter(
            iteration_counts[max_change_index],
            darkness_values[max_change_index],
            color="red",
            s=100,
            zorder=5,
            label=f"Biggest change: {max_change:.4f}",
        )

    plt.xlabel("Iteration Count")
    plt.ylabel("Darkness")
    plt.title("Darkness vs Iteration Count")
    plt.grid(True)
    plt.legend()
    plt.savefig(filepath)
    plt.close()

    print(f"Graph saved as {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Check line width")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument("--output-dir", "-o", default=".", help="Directory to save output images")
    parser.add_argument("--size", type=int, default=2, help="Kernel size for erosion")
    parser.add_argument("--iterations", type=int, default=1, help="iterations for erosion")
    parser.add_argument("--threshold", type=float, default=1.0, help="Darkness threshold")

    args = parser.parse_args()

    # Get the PDF filename for use in output naming
    pdf_filename = os.path.basename(args.pdf_path)

    # Process PDF with iterations until threshold is met
    iteration_counts, darkness_values = process_pdf_with_iterations(
        args.pdf_path, threshold=args.threshold, size=args.size
    )

    # Find biggest change
    max_change_index, max_change = find_biggest_change(darkness_values)
    print(f"Biggest change: {max_change:.4f} at iteration {max_change_index}")

    # Generate graph
    generate_graph(iteration_counts, darkness_values, args.output_dir, pdf_filename)

    # Also save the final processed image
    pages = pdf_to_image(args.pdf_path)
    page = pages[0]

    page = clamp(page)
    page = simplify(page, args.size, iterations=iteration_counts[-1])

    # save_images([page], args.output_dir, pdf_filename)


if __name__ == "__main__":
    main()
