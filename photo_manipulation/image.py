import numpy as np
import png 


class Image:
    def __init__(self, x_pixels=0, y_pixels=0, num_channels=0, filename=''):
        #you need to input either filename OR x_pixels, y_pixels, and num_channels
        self.input_path = 'input/'
        self.output_path = 'output/'
        if x_pixels and y_pixels and num_channels:
            self.x_pizels = x_pixels
            self.y_pixels = y_pixels
            self.num_channels = num_channels
            self.array = np.zeros((x_pixels, y_pixels, num_channels))
        elif filename:
            self.array = self.read_image(filename)
        else:
            raise ValueError('You need to input either filename OR x_pixels, y_pixels, and num_channels')
        
        def read_image(self, filename, gamma=2.2):
            # read PNG RGB image, return 3d numpy array organized along y, x, channel values are float, gamma is decoded

            im = png.Reader(self.input_path + filename).asFloat()
            resized_image = np.vstack(list(im[2]))
            resized_image = resized_image.reshape(im[1], im[0], 3)
            resized_image = resized_image ** gamma
            return resized_image 
        
        def write_image(self, output_file_name, gamma=2.2):
            # 3D numpy array (y, x, channel) of values between 0 and 1 -> write to png

            im = np.clip(self.array, 0, 1)
            y, x = self.array.shape[0], self.array.shape[1]
            im = im.reshape(y, x*3)
            writer = png.writer(x, y)
            with open(self.output_path + output_file_name, 'wb') as f:
                writer.write(f, 255*(im**(1/gamma)))

            self.array.resize(y, x, 3)


if __name__ == '__main__':
    im = Image(filename='NAME_OF_YOUR_IMAGE.png')
    im.write_image('test.png')
