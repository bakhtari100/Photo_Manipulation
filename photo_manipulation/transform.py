from photo_manipulation.image import Image
from numpy import np

def adjust_brightness(image, factor):
    # factor is a value > 0
    # <1 darkens the image, >1 brightens the image
    x_pixels, y_pixels, num_channels = image.array.shape
    # make an empty image so we don't modify the original image
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)
    # NON-VECTORIZED VERSION - most intuitive way to do this
    # for x in range(x_pixels):
    #     for y in range(y_pixels):
    #         for c in range(num_channels):
    #             new_im.array[x, y, c] = image.array[x, y, c] * factor
    
    # VECTORIZED VERSION - much faster
    new_im.array = image.array * factor
    return new_im
    

def adjust_contrast(image, factor, mid=0.5):
    # adjust the contrast by increasing the distance from mid by some amount, factor
    x_pixels, y_pixels, num_channels = image.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)
    # NON-VECTORIZED VERSION 
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image.array[x, y, c] - mid) * factor + mid
    
    # VECTORIZED VERSION
    # new_im.array = (image.array - mid) * factor + mid
    
    return new_im

def blur(image, kernel_size):
    # kernel size is th number of pixels to take into account when applying the blur
    # kernel_size determines how wide you want your image to be
    # taking the pixel and averaging it with its neighbors
    # kernel_size should always be an odd number
    x_pixels, y_pixels, num_channels = image.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)
    
    neighbor_range = kernel_size // 2 # how many neighbors to one side we need to look at
    # NON-VECTORIZED VERSION 
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                # iterate through each neighbor and summing the values
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(x_pixels - 1, x+neighbor_range + 1)):
                    for y_i in range(max(0,y-neighbor_range), min(y_pixels - 1, y+neighbor_range + 1)):
                        total += image.array[x_i, y_i, c]
                new_im.array[x, y, c] = total / (kernel_size ** 2) # average
    
    return new_im
                





def apply_kernel(image, kernel):
    # the kernel should be a numpy 2D array that represents the blur kernel
    x_pixels, y_pixels, num_channels = image.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    kernel_size = kernel.shape[0]
    neighbor_range = kernel_size // 2 # how many neighbors to one side we need to look at
    
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(x_pixels - 1, x+neighbor_range + 1)):
                    for y_i in range(max(0,y-neighbor_range), min(y_pixels - 1, y+neighbor_range + 1)):
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val
                new_im.array[x, y, c] = total

    return new_im

def combine_image(image1, image2):
    # combine two images using the squared sum of squares: value = sqrt(value_1**2), value_2**2)
    # size of image1 and image2 must be the same
    x_pixels, y_pixels, num_channels = image1.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

 
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image1.array[x, y, c] **2 + image2.array[x, y, c] **2)**0.5

    return new_im




if __name__ == '__main__':
    im = Image(filename='lake.png')
    im.write_image('test.png')
    