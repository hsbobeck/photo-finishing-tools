from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from perlin_noise import PerlinNoise
import numpy as np


# image : PIL Image RGB 0-255
# curve_func : curve function
# strength : float              # grain strength multiplier (essentially contrast, like a gain that affects blacks as much as whites)
# scale : float >= 1.0          # zooms in on the grain plate by the specified factor
# blur : float                  # controls radius of the blur applied to the grain plate
# saturation: float             # controls color saturation of the grain plate
# image_softness : float        # controls radius of the blur applied to the image
# return : PIL Image RGB 0-255
def add_grain(
    image,
    curve_func="A",
    strength=1.0,
    scale=1.0,
    blur=0.0,
    saturation=1.0,
    image_softness=0.0,
):
    # set the curve function as specified
    if curve_func == "inverse":
        curve_func = curve_inverse
    elif curve_func == "A":
        curve_func = curve_A
    elif curve_func == "B":
        curve_func = curve_B
    else:
        curve_func = curve_A
        print("WARNING: Requested curve function not recognized. Defaulting to A.")

    # load grain plate
    grain_plate = Image.open("grain_plates/costarica-grainplate.tif")

    # control saturation of the grain plate by specified amount
    converter = ImageEnhance.Color(grain_plate)
    grain_plate = converter.enhance(saturation)

    # rotate grain plate to match the orientation of the image
    if is_different_orientation(image, grain_plate):
        grain_plate = grain_plate.rotate(90, expand=True)

    # crop the grain plate to the aspect ratio of the image
    grain_plate = crop_to_aspect_ratio(grain_plate, image.size[0] / image.size[1])

    # blur the grain plate by the specified amount
    grain_plate = grain_plate.filter(ImageFilter.BoxBlur(radius=blur))

    # scale the grain plate by the specified amount
    if scale > 1.0:
        grain_plate = zoom_image(grain_plate, scale)
    elif scale < 1.0:
        print(
            "Warning: Scaling not applied. The value of the 'scale' parameter must be >= 1.0"
        )

    # resize the grain plate to match the image
    # Image.Resampling.BOX is used because the 'better' algorithms cause grid-like artifacting. My guess is they are not optimized for noise-like images
    grain_plate = grain_plate.resize(
        (image.size[0], image.size[1]), resample=Image.Resampling.BOX
    )

    # convert the grain plate to np array and scale to 0-1
    grain_plate = np.array(grain_plate) / 255

    # blur the image the specified amount
    image = image.filter(ImageFilter.GaussianBlur(radius=image_softness))

    # apply the grain plate to the image
    image = np.array(image) / 255
    image += (
        (grain_plate - get_avg_rgb_of_image(grain_plate)) * curve_func(image) * strength
    )
    image = np.clip(image, 0, 1)
    image = Image.fromarray((image * 255).astype(np.uint8))

    # return the final image with added grain
    return image


# CURVE FUNCTION
# PASSTHROUGH - uses the input image
# image : np array 0-1
def curve_passthrough(image):
    return image


# CURVE FUNCTION
# INVERSE - uses the inverse of the input image
# image : np array 0-1
def curve_inverse(image):
    return 1 - image


# curve helper function
# applies a custom tone mapping to the inverse of the given image
# image : np array 0-1          # image before curve is applied
# lut_x : list of input values 0-255 (same length as lut_y)
# lut_y : list of output values 0-255 (same length as lut_x)
# return : np array 0-1         # image after curve is applied
def __generate_inverse_curve(image, lut_x, lut_y):
    # invert the image
    image = curve_inverse(image)

    # convert to PIL Image 0-255
    image = Image.fromarray((image * 255).astype(np.uint8))

    lut_u8 = np.interp(np.arange(0, 256), lut_x, lut_y).astype(np.uint8)

    R, G, B = [0, 1, 2]
    source = image.split()
    out = []
    for band in [R, G, B]:
        out.append(source[band].point(lut_u8))

    merged_img = Image.merge("RGB", out)
    # merged_img.show()

    output = np.asarray(merged_img) / 255
    return output


# CURVE FUNCTION
# (applies a custom tone mapping to the inverse of the given image)
# PRESET A - standard look
# image : np array 0-1          # image before curve is applied
# return : np array 0-1         # image after curve is applied
def curve_A(image):

    lut_x = [0, 25, 100, 176, 200, 215, 230, 245, 255]
    lut_y = [0, 12, 60, 70, 85, 105, 144, 100, 85]

    return __generate_inverse_curve(image, lut_x, lut_y)


# CURVE FUNCTION
# (applies a custom tone mapping to the inverse of the given image)
# PRESET B - standard look with more grain in the darks/blacks
# image : np array 0-1          # image before curve is applied
# return : np array 0-1         # image after curve is applied
def curve_B(image):

    lut_x = [0, 25, 100, 176, 200, 215, 230, 255]
    lut_y = [0, 12, 60, 70, 85, 105, 144, 98]

    return __generate_inverse_curve(image, lut_x, lut_y)


# image : PIL 'RGB' Image (0-255)
# ratio : float (ex: 1.33 for 4/3 aspect ratio)
# scale : float
# return : image
def crop_to_aspect_ratio(image, ratio):
    # if target ratio is skinnier, keep the original height
    if image.size[0] / image.size[1] >= ratio:
        h = image.size[1]
        w = int(ratio * h)
    else:  # if target ratio is wider, keep the original width
        w = image.size[0]
        h = int(w / ratio)

    return ImageOps.fit(image, (w, h))


# image1, image2 : PIL Image 'RGB' 0-255
# return : boolean
def is_different_orientation(image1, image2):
    return (image1.size[0] > image1.size[1] and image2.size[0] < image2.size[1]) or (
        image1.size[0] < image1.size[1] and image2.size[0] > image2.size[1]
    )


# image : PIL Image 'RGB' 0-255
# zoom_factor : float >= 1.0
def zoom_image(image, zoom_factor):
    left = int((zoom_factor - 1) / (zoom_factor * 2) * image.size[0])
    top = int((zoom_factor - 1) / (zoom_factor * 2) * image.size[1])
    right = image.size[0] - left
    bottom = image.size[1] - top
    return image.crop((left, top, right, bottom))


# returns true for horizontal OR square
# return : boolean
def is_horizontal(image):
    return image.size[0] >= image.size[1]


# returns true for vertical
# return : boolean
def is_vertical(image):
    return image.size[0] < image.size[1]


# image : np array
# return : 1x3 np array
def get_avg_rgb_of_image(image):
    avg_rgb_per_row = np.average(image, axis=0)
    avg_rgb = np.average(avg_rgb_per_row, axis=0)
    return avg_rgb


def main():
    # Example usage
    input_image_path = "test_images/test1_input.jpg"
    image = Image.open(input_image_path)
    image = add_grain(
        image, curve_A, strength=2, scale=1, saturation=1, image_softness=1
    )
    # Save the resulting image
    output_image_path = "test_images/test1_output.jpg"
    image.show()
    image.save(output_image_path)

    # input_image_path = "test_images/test1_input.jpg"
    # image = Image.open(input_image_path)
    # converter = ImageEnhance.Color(image)
    # image = converter.enhance(0.5)
    # image.show()


if __name__ == "__main__":
    main()
