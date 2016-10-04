from __future__ import absolute_import, print_function

import argparse
import os
from PIL import Image, ImageEnhance


iw_parser = argparse.ArgumentParser(description='Choosing location and destination.')

iw_parser.add_argument(
    '-m', '--mark-file',
    required=True
)
iw_parser.add_argument(
    '-s', '--source-dir'
)
iw_parser.add_argument(
    '-d', '--dest-dir',
    required=True
)
iw_parser.add_argument(
    '-o', '--opacity',
    required=True,
    type=float
)
iw_parser.add_argument(
    '-r', '--rotate-angle',
    required=False,
    default=0,
    type=float
)
iw_parser.add_argument(
    '--png',
    action='store_true'
)
iw_parser.add_argument(
    '--jpg',
    action='store_true'
)
iw_parser.add_argument(
    '-f', '--file',
    default=None
)
iw_parser.add_argument(
    '--copyright',
    default=None
)


def get_image_list(source_dir, ext_list):
    file_paths = []
    normal_file_paths = []

    for path, subdirs, files in os.walk(source_dir):
        for name in files:
            file_path = os.path.join(path, name)
            if os.path.splitext(file_path)[1] in ext_list:
                file_paths.append(file_path)
            else:
                normal_file_paths.append(file_path)
    return file_paths, normal_file_paths


def check_or_make_dest_dir(dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)


def is_marked(image, copyright_string):
    info = image.info
    if not not info:
        if 'Copyright' in info:
            if info['Copyright'] == copyright_string:
                return True

    return False


def save_with_meta(image, file_path, copyright_string):
    image.info['Copyright'] = copyright_string
    image.save(file_path, quality=100)


def reduce_opacity(image, opacity):
    assert 0 <= opacity <= 1

    if image.mode != 'RGBA':
        image.convert('RGBA')

    alpha = image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    image.putalpha(alpha)

    return image


def rotate_image(image, angle):
    assert -45 <= angle <= 45

    if image.mode != 'RGBA':
        image.convert('RGBA')

    image = image.rotate(angle, expand=1)

    return image


def water_mark_image(ori_image, mark_image):
    ori_w, ori_h = ori_image.size

    if ori_w < 500:
        return ori_image

    mark_w, mark_h = mark_image.size

    resized_mark_h = ori_h/8
    resized_mark_w = resized_mark_h * mark_w / mark_h

    offset = (
        ori_w - resized_mark_w - ori_w/25,
        ori_h - resized_mark_h - ori_h/20
    )

    resized_mark_image = mark_image.resize((resized_mark_w, resized_mark_h),
                                           Image.LANCZOS)

    ori_image.paste(resized_mark_image, offset, resized_mark_image)

    return ori_image
