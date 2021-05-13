import numpy as np
import cv2
from PIL import Image


def draw_image(image_path, logo, placement, margin, step):
    logo_size = logo.size
    if placement == 'A':
        position = find_position(image_path, logo_size, margin=margin, step=step)
    else:
        position = get_position(image_path, logo_size, placement, margin)
    image = Image.open(image_path)
    image_copy = image.copy()
    image_copy.paste(logo, position, logo)
    return image_copy


def draw_images(images: list, logo=None, placement='A', margin=10, step=20):
    if logo is None or len(images) == 0:
        return
    logo = Image.open(logo)
    errors = []
    correct = []
    for image_path in images:
        image = draw_image(image_path, logo, placement, margin, step)
        if image:
            correct.append(image)
        else:
            errors.append(image)
    return correct, errors


def find_position(image_path, logo_size, margin, step):
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), 1)
    row = np.full(logo_size[1] + margin, 255)
    matrix = np.full((logo_size[0] + margin, logo_size[1] + margin), 255)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(gray, 200, 255, 0)
    gray = cv2.bitwise_not(gray)
    for x in range(0, gray.shape[1] - logo_size[1] + 1, step):
        for y in range(0, gray.shape[0] - logo_size[0] + 1, step):
            if np.array_equal(row, gray[y, x:logo_size[1] + x + margin]):
                if np.array_equal(matrix, gray[y:logo_size[0] + y + margin, x:logo_size[1] + x + margin]):
                    return int(x + margin/2), int(y + margin/2)


def get_position(image_path, logo_size, placement, margin):
    placement = placement.upper()
    if placement == 'N' or placement == 'S':
        placement = placement + 'C'
    elif placement == 'W' or placement == 'E':
        placement = 'C' + placement
    elif placement[0] not in 'NSC' or placement[1] not in 'WEC':
        return
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), 1)
    im_height, im_width, _ = image.shape
    print(im_width, im_height)
    print(logo_size)
    x, y = 0, 0
    if placement[0] == 'N':
        y = margin
    elif placement[0] == 'S':
        y = im_height - logo_size[1] - margin
    elif placement[0] == 'C':
        y = im_height // 2 - logo_size[1] // 2
    if placement[1] == 'W':
        x = margin
    elif placement[1] == 'E':
        x = im_width - logo_size[0] - margin
    elif placement[1] == 'C':
        x = im_width // 2 - logo_size[0] // 2
    print(x, y)
    return x, y
