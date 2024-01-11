import numpy as np

from scipy import ndimage

def transform_img(image):

    rotated1 = stretch_img(ndimage.rotate(image, 4, reshape=True, cval=255))
    rotated2 = stretch_img(ndimage.rotate(image, 7, reshape=True, cval=255))
    rotated3 = stretch_img(ndimage.rotate(image, 10, reshape=True, cval=255))
    rotated4 = stretch_img(ndimage.rotate(image, -4, reshape=True, cval=255))
    rotated5 = stretch_img(ndimage.rotate(image, -7, reshape=True, cval=255))
    rotated6 = stretch_img(ndimage.rotate(image, -10, reshape=True, cval=255))

    shifted1 = stretch_img(ndimage.zoom(image, (1, 0.95)))
    shifted2 = stretch_img(ndimage.zoom(image, (1, 0.90)))
    shifted3 = stretch_img(ndimage.zoom(image, (0.95, 1)))
    shifted4 = stretch_img(ndimage.zoom(image, (0.90, 1)))

    return rotated1, rotated2, rotated3, rotated4, rotated5, rotated6, shifted1, shifted2, shifted3, shifted4


def stretch_img(np_img):
    non_white_indices = np.where(np_img < 255)
    row_indices, column_indices = non_white_indices[0], non_white_indices[1]

    if len(row_indices) == 0:
        return None

    top = np.min(row_indices)
    bottom = np.max(row_indices)
    left = np.min(column_indices)
    right = np.max(column_indices)

    diff_y = bottom - top
    diff_x = right - left

    final_size = max(diff_y, diff_x) + 1

    img_without_white_spaces = np_img[top:bottom + 1, left:right + 1]
    square_img = np.full((final_size, final_size), 255)

    if diff_y > diff_x:
        new_top = 0
        new_bottom = diff_y
        new_left = (diff_y - diff_x) // 2
        new_right = new_left + diff_x

    else:
        new_top = (diff_x - diff_y) // 2
        new_bottom = new_top + diff_y
        new_left = 0
        new_right = diff_x

    square_img[new_top:new_bottom + 1, new_left:new_right + 1] = img_without_white_spaces
    return ndimage.zoom(square_img, 32/square_img.shape[0])
