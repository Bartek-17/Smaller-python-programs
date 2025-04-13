from PIL import Image
import time 

YODA = 'yoda.jpeg'
ROAD = 'road.jpg'


def get_rgb_representation(image_path):
    """
    returns 2D list of RGB tuples
    """
    img = Image.open(image_path)
    width, height = img.size
    rgb_data = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            row.append((r, g, b))
        rgb_data.append(row)
    return rgb_data


def convert_to_grayscale(image_path):
    img = Image.open(image_path)
    width, height = img.size
    # new image with the same size
    grayscale_img = Image.new('RGB', (width, height))

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            gray = (r + g + b) // 3
            grayscale_img.putpixel((x, y), (gray, gray, gray))
    return grayscale_img


def black_and_white_single_threshold(image_path, threshold):
    grayscale_img = convert_to_grayscale(image_path)
    width, height = grayscale_img.size

    bw_img = Image.new('RGB', (width, height))

    for y in range(height):
        for x in range(width):
            gray_intensity = grayscale_img.getpixel((x, y))[0]

            if gray_intensity >= threshold:
                bw_img.putpixel((x, y), (255, 255, 255))  # White
            else:
                bw_img.putpixel((x, y), (0, 0, 0))  # Black

    return bw_img


def black_and_white_double_threshold(image_path, low_threshold, high_threshold):
    grayscale_img = convert_to_grayscale(image_path)
    width, height = grayscale_img.size

    bw_img = Image.new('RGB', (width, height))

    for y in range(height):
        for x in range(width):
            gray_intensity = grayscale_img.getpixel((x, y))[0]

            if low_threshold <= gray_intensity <= high_threshold:
                bw_img.putpixel((x, y), (255, 255, 255))
            else:
                bw_img.putpixel((x, y), (0, 0, 0))

    return bw_img


# Ex 1

rgb_data = get_rgb_representation(YODA)
print(rgb_data[1])


# Ex 2

# grayscale_img = convert_to_grayscale(YODA)
# grayscale_img.show()


#bw_single = black_and_white_single_threshold(YODA, 128)
#bw_single.show()

#bw_double = black_and_white_double_threshold(YODA, 85, 170)
#bw_double.show()

'''

# Ex 3

def histogram_equalization(image_path):
    img = convert_to_grayscale(image_path)
    pixels = list(img.getdata())
    histogram = [0] * 256
    width, height = img.size
    img_size = width * height

    # calculate the occurences of each value 0-255
    for px in pixels:
        histogram[px[0]] += 1

    # calculate the cumulative distribution function
    cdf = [0] * len(histogram)
    cdf_min = None
    sum_cdf = 0

    for i in range(len(histogram)):
        sum_cdf += histogram[i]
        cdf[i] = sum_cdf
        if cdf_min is None and histogram[i] > 0:
            cdf_min = sum_cdf  # first non-zero value

    # Normalize the CDF
    cdf_normalized = [0] * 256
    for i in range(256):
        cdf_normalized[i] = (cdf[i] - cdf_min) / (img_size - cdf_min) * 255


    # Step 3: Equalize the histogram
    equalized = Image.new('RGB', (width, height))
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))[0]
            new_pixel_value = int(cdf_normalized[pixel])
            equalized.putpixel((x, y), (new_pixel_value, new_pixel_value, new_pixel_value))

    return equalized

grey = convert_to_grayscale(YODA)
grey.show()

equalized_image = histogram_equalization(YODA)
equalized_image.show()

'''

# Ex 4


def calculate_summed_area_table(image):
    width, height = image.size
    grayscale_img = image.convert('L')
    
    # Initialize the summed area table with zeros
    summed_area_table = []
    for i in range(height):
        row = [0] * width
        summed_area_table.append(row)
    
    # Set the first value
    summed_area_table[0][0] = grayscale_img.getpixel((0, 0))
    
    # Fill the first row
    for x in range(1, width):
        summed_area_table[0][x] = summed_area_table[0][x - 1] + grayscale_img.getpixel((x, 0))
    
    # Fill the first column
    for y in range(1, height):
        summed_area_table[y][0] = summed_area_table[y - 1][0] + grayscale_img.getpixel((0, y))
    
    # Fill the whole table based on previous values
    for y in range(1, height):
        for x in range(1, width):
            summed_area_table[y][x] = (grayscale_img.getpixel((x, y)) +
                                       summed_area_table[y - 1][x] +
                                       summed_area_table[y][x - 1] -
                                       summed_area_table[y - 1][x - 1])
    return summed_area_table

def apply_mean_filter(image_path, mask_size):
    image = Image.open(image_path)
    width, height = image.size
    summed_area_table = calculate_summed_area_table(image)
    half_mask = mask_size // 2
    window_area = mask_size * mask_size
    filtered_image = Image.new('L', (width, height))
    
    for y in range(height):
        for x in range(width):
            top = max(0, y - half_mask)
            bottom = min(height - 1, y + half_mask)
            left = max(0, x - half_mask)
            right = min(width - 1, x + half_mask)
            
            if top > 0 and left > 0:
                sum_pixels = (summed_area_table[bottom][right] -
                              summed_area_table[top - 1][right] -
                              summed_area_table[bottom][left - 1] +
                              summed_area_table[top - 1][left - 1])
            elif top > 0:
                sum_pixels = summed_area_table[bottom][right] - summed_area_table[top - 1][right]
            elif left > 0:
                sum_pixels = summed_area_table[bottom][right] - summed_area_table[bottom][left - 1]
            else:
                sum_pixels = summed_area_table[bottom][right]

            average_pixel = sum_pixels // window_area
            filtered_image.putpixel((x, y), int(average_pixel))

    return filtered_image

# iterates over each pixel in the image and computes the average value
# of the pixels within a square window (mask) centered around each pixel

def apply_mean_filter_naive(image_path, mask_size):
    image = Image.open(image_path)
    grayscale_img = image.convert('L')
    width, height = grayscale_img.size
    half_mask = mask_size // 2
    filtered_image = Image.new('L', (width, height))

    for y in range(height):
        if (y % 10 == 0):
            print(y)
        for x in range(width):
            pixel_sum = 0
            count = 0
            for offset_y in range(-half_mask, half_mask):
                for offset_x in range(-half_mask, half_mask):
                    pixel_y, pixel_x = y + offset_y, x + offset_x
                    if 0 <= pixel_y < height and 0 <= pixel_x < width:
                        pixel_sum += grayscale_img.getpixel((pixel_x, pixel_y))
                        count += 1
            average_pixel = pixel_sum // count
            filtered_image.putpixel((x, y), average_pixel)
    return filtered_image


# Timing and comparison

start_time = time.time()
filtered_image_summed_area = apply_mean_filter(ROAD, mask_size=71)
end_time = time.time()
print(f"Summed-area table method took {end_time - start_time:.2f} seconds")
filtered_image_summed_area.show()


greyscale = convert_to_grayscale(YODA)
greyscale.show()

start_time = time.time()
filtered_image_naive = apply_mean_filter_naive(YODA, mask_size=6)
end_time = time.time()
print(f"Naive method took {end_time - start_time:.2f} seconds")
filtered_image_naive.show()
