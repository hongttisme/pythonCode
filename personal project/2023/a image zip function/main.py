from PIL import Image
import numpy as np


def zip_function(number_of_colour, input_rgb_array):
    channels = 3
    zipped_colour_array = np.random.randint(0, 256, size=(number_of_colour, channels))

    mapping_array = input_rgb_array[:, :, np.newaxis]
    conti = True
    counting = 0
    while conti:

        mapping_array = input_rgb_array[:, :, np.newaxis]

        if True:
            a = mapping_array - zipped_colour_array
            a = (a * a)
            a = np.sum(a, axis=-1)
            mapping_array = np.argmin(a, axis=-1)
        else:
            a = (mapping_array * mapping_array)
            a = np.sum(a, axis=-1) ** 0.5
            b = (zipped_colour_array * zipped_colour_array)
            b = np.sum(b, axis=-1) ** 0.5
            b = a * b

            mapping_array = (mapping_array * zipped_colour_array)
            mapping_array = np.sum(mapping_array, axis=-1)
            mapping_array = mapping_array / b

            mapping_array = np.argmax(mapping_array, axis=-1)

        sum_array = [[] for _ in range(zipped_colour_array.shape[0])]

        for row in range(input_rgb_array.shape[0]):
            for column in range(input_rgb_array.shape[1]):
                sum_array[mapping_array[row, column]].append(list(input_rgb_array[row, column]))

        conti = False
        for i, arr in enumerate(sum_array):
            if arr:
                average_arr = np.array(arr)
                average_arr = np.average(average_arr, axis=0)

                if not np.allclose(zipped_colour_array[i], average_arr, rtol=1e-1, atol=1e-2):
                    conti = True
                    zipped_colour_array[i] = average_arr

        print(number_of_colour, counting)
        counting += 1
        if counting > 1000:
            break

    zipped_rgb_array = zipped_colour_array[mapping_array]
    zipped_rgb_array = np.array(zipped_rgb_array, dtype=np.uint8)
    output_image = Image.fromarray(zipped_rgb_array)
    output_path = f'{number_of_colour}.jpg'
    output_image.save(output_path)


if __name__ == '__main__':
    image_path = 'input.jpg'
    image = Image.open(image_path)

    rgb_array = np.array(image)
    for x in range(2, 101):
        zip_function(x, rgb_array)
