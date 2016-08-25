from __future__ import absolute_import, print_function

import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(1, parent_dir)
sys.modules['IWat'] = __import__('IWat')

if __package__ is None:
    __package__ = 'IWat'


from IWat import parser, \
    get_image_list, check_or_make_dest_dir, \
    water_mark_image, reduce_opacity, rotate_image, \
    Image


args = parser.parse_args()

ext_list = []

if args.png:
    ext_list.append('.png')

if args.jpg:
    ext_list.append('.jpg')

files = get_image_list(args.source_dir, ext_list)

check_or_make_dest_dir(args.dest_dir)

mark_image = Image.open(args.mark_file)
mark_image = reduce_opacity(
    mark_image,
    args.opacity
)

if args.rotate_angle != 0:
    mark_image = rotate_image(mark_image, args.rotate_angle)

for image_file_path in files:
    marked_image = water_mark_image(image_file_path, mark_image)
    dest_file_path = image_file_path.replace(args.source_dir,
                                             args.dest_dir)
    if not os.path.exists(os.path.dirname(dest_file_path)):
        os.makedirs(os.path.dirname(dest_file_path))
    marked_image.save(dest_file_path)
