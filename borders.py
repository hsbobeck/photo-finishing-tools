from PIL import Image, ImageOps


def add_white_border(input_image_path, output_image_path, size_percentage=0.9):
    # Open the input image
    image = Image.open(input_image_path)

    # Calculate the border sizes
    top_bottom_border = int(image.height * size_percentage / 100)
    left_right_border = int(image.width * size_percentage / 100)

    # Add a white border with different widths for top/bottom and left/right
    bordered_image = ImageOps.expand(
        image,
        border=(
            left_right_border,
            top_bottom_border,
            left_right_border,
            top_bottom_border,
        ),
        fill="white",
    )

    # Save the resulting image
    bordered_image.save(output_image_path)


def main():
    # Example usage
    input_image_path = "input.jpg"
    output_image_path = "output.jpg"
    add_white_border(input_image_path, output_image_path, 0.9)


if __name__ == "__main__":
    main()
