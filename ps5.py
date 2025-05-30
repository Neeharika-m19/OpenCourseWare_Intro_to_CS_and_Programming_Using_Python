"""
# Problem Set 5
# Name:
# Collaborators:
"""

from PIL import Image, ImageFont, ImageDraw
import numpy


def make_matrix(color):
    """
    Generates a transformation matrix for the specified color.
    Inputs:
        color: string with exactly one of the following values:
               'red', 'blue', 'green', or 'none'
    Returns:
        matrix: a transformation matrix corresponding to
                deficiency in that color
    """
    # You do not need to understand exactly how this function works.
    if color == 'red':
        c = [[.567, .433, 0], [.558, .442, 0], [0, .242, .758]]
    elif color == 'green':
        c = [[0.817, 0.183, 0], [0.333, 0.667, 0], [0, 0.125, 0.875]]
    elif color == 'blue':
        c = [[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 0.7]]
    elif color == 'none':
        c = [[1, 0., 0], [0, 1, 0.], [0, 0., 1]]
    return c


def matrix_multiply(m1, m2):
    """
    Multiplies the input matrices.
    Inputs:
        m1,m2: the input matrices
    Returns:
        result: matrix product of m1 and m2
        in a list of floats
    """
    product = numpy.matmul(m1, m2)
    if type(product) == numpy.int64:
        return float(product)
    else:
        result = list(product)
        return result


def img_to_pix(filename):
    """
    Input: string representing an image file, like 'image.jpg'
    Output: list of pixels in the image, e.g., [(0,0,0),(255,255,255),...] for RGB
            or [60, 66, 72,...] for BW
    """
    img = Image.open(filename)
    # Convert image to list of pixels
    return list(img.getdata())


def pix_to_img(pixels_list, size, mode):
    """
    Creates an Image object from a list of pixels
    
    pixels_list: a list of pixels, each represented as a tuple of RGB values or a single value for BW
    size: a tuple of (width, height) representing image dimensions
    mode: 'RGB' for color images or 'L' for black and white images
    
    Returns: PIL.Image object
    """
    img = Image.new(mode, size)
    img.putdata(pixels_list)
    return img


def filter(pixels_list, color):
    """
    Applies a color transformation to simulate color deficiency
    
    pixels_list: list of RGB tuples, e.g., [(0,0,0), (255,255,255),...]
    color: string, one of 'red', 'blue', 'green', or 'none'
    Returns: list of transformed RGB tuples
    """
    matrix = make_matrix(color)
    transformed = []
    
    for pixel in pixels_list:
        # Multiply pixel by transformation matrix
        new_pixel = matrix_multiply(matrix, pixel)
        # Convert float values back to integers and ensure they're in valid range
        new_pixel = tuple(max(0, min(255, int(x))) for x in new_pixel)
        transformed.append(new_pixel)
    
    return transformed


def extract_end_bits(num_end_bits, pixel):
    """
    Extract the specified number of least significant bits from a pixel value
    
    num_end_bits: number of LSBs to extract
    pixel: integer pixel value or tuple of RGB values
    Returns: integer value of the extracted bits or tuple of extracted bits
    """
    if isinstance(pixel, tuple):
        # Handle RGB pixel by extracting bits from each channel
        return tuple(p & ((1 << num_end_bits) - 1) for p in pixel)
    else:
        # Handle BW pixel
        return pixel & ((1 << num_end_bits) - 1)


def reveal_bw_image(filename):
    """
    Reveals hidden black and white image in the least significant bit
    
    filename: string, name of the image file
    Returns: PIL.Image object of the revealed image
    """
    # Get the original image and its size
    img = Image.open(filename)
    size = img.size
    pixels = img_to_pix(filename)
    
    # Extract LSB from each pixel and scale to full range (0 or 255)
    hidden_pixels = [extract_end_bits(1, p) * 255 for p in pixels]
    
    # Create and return new image
    return pix_to_img(hidden_pixels, size, 'L')


def reveal_color_image(filename):
    """
    Reveals hidden color image in the three least significant bits
    
    filename: string, name of the image file
    Returns: PIL.Image object of the revealed image
    """
    # Get the original image and its size
    img = Image.open(filename)
    size = img.size
    pixels = img_to_pix(filename)
    
    # Extract 3 LSBs from each channel and rescale
    hidden_pixels = []
    for p in pixels:
        # Extract 3 LSBs from each channel using bitwise operations
        rgb = extract_end_bits(3, p)
        # Scale from 0-7 to 0-255 range
        r = (rgb[0] * 255) // 7
        g = (rgb[1] * 255) // 7
        b = (rgb[2] * 255) // 7
        hidden_pixels.append((r, g, b))
    
    # Create and return new image
    return pix_to_img(hidden_pixels, size, 'RGB')


def reveal_image(filename):
    """
    Reveals the hidden image from filename
    
    filename: string, name of the image file
    Returns: PIL.Image object of the revealed image
    """
    img = Image.open(filename)
    if img.mode == 'L':  # Black and white image
        return reveal_bw_image(filename)
    else:  # RGB image
        return reveal_color_image(filename)


def draw_kerb(image_file, kerb):
    """
    Adds a watermark of the given kerberos to the image
    
    image_file: string, name of the image file
    kerb: string, kerberos to add as watermark
    """
    img = Image.open(image_file)
    # Create a copy of the image to draw on
    draw = ImageDraw.Draw(img)
    # Add watermark text in bottom right corner
    width, height = img.size
    draw.text((width - 100, height - 20), kerb, fill=(255, 255, 255))
    # Save with _kerb suffix
    name, ext = image_file.rsplit('.', 1)
    img.save(f"{name}_kerb.{ext}")


def main():
    # Test color filter
    img = Image.open("image_15.png")
    size = img.size
    pixels = img_to_pix("image_15.png")
    filtered_pixels = filter(pixels, 'red')
    filtered_img = pix_to_img(filtered_pixels, size, 'RGB')
    filtered_img.save("image_15_filtered.png")
    
    # Reveal and save hidden images
    hidden1 = reveal_image("hidden1.bmp")
    hidden1.save("revealed1.png")
    
    hidden2 = reveal_image("hidden2.bmp")
    hidden2.save("revealed2.png")
    
    # Add kerb watermark to all images
    kerb = input("Enter your kerberos: ")
    draw_kerb("image_15_filtered.png", kerb)
    draw_kerb("revealed1.png", kerb)
    draw_kerb("revealed2.png", kerb)


if __name__ == "__main__":
    main()
