import matplotlib.pyplot as plt
import numpy as np
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        return result
    return wrapper


def array_concatenation(img, start_img=None):
    height = 24
    new_img = []
    for i in range(height):
        if start_img is None:
            new_img_i = np.concatenate((img[i], img[i]), axis=0)
        else:
            new_img_i = np.concatenate((img[i], start_img[i]), axis=0)
        new_img.append(new_img_i)
    new_img = np.array(new_img)
    return new_img


def img_multiplication(input_path: str, output_path: str, count: int):
    start_img = plt.imread(input_path)
    img = start_img
    if count != 1:
        for i in range(int(np.sqrt(count))):
            img = array_concatenation(img)
        new_cnt = np.power(2, int(np.sqrt(count)))
        for i in range(count - new_cnt):
            img = array_concatenation(img, start_img)
        img = np.array(img)
    plt.imsave(output_path, img)
