from __future__ import print_function
import os
from shutil import copyfile
from IWat import iw_parser, \
    get_image_list, check_or_make_dest_dir, \
    is_marked, save_with_meta, \
    water_mark_image, reduce_opacity, rotate_image, \
    Image


iw_args = iw_parser.parse_args()

ext_list = []

if iw_args.png:
    ext_list.append('.png')

if iw_args.jpg:
    ext_list.append('.jpg')
    ext_list.append('.jpeg')

normal_files = []

if iw_args.file is not None:
    files = [iw_args.file]
else:
    files, normal_files = get_image_list(iw_args.source_dir, ext_list)

check_or_make_dest_dir(iw_args.dest_dir)

mark_image = Image.open(iw_args.mark_file)
mark_image = reduce_opacity(
    mark_image,
    iw_args.opacity
)

if iw_args.rotate_angle != 0:
    mark_image = rotate_image(mark_image, iw_args.rotate_angle)

for image_file_path in files:
    try:
        marking_image = Image.open(image_file_path)
        if iw_args.copyright is not None:
            if is_marked(marking_image, iw_args.copyright):
                normal_files.append(image_file_path)
                continue
        ori_w, ori_h = marking_image.size
        if ori_w < 500:
            normal_files.append(image_file_path)
            continue
        marked_image = water_mark_image(marking_image, mark_image)
        dest_file_path = image_file_path.replace(iw_args.source_dir,
                                                 iw_args.dest_dir)
        if not os.path.exists(os.path.dirname(dest_file_path)):
            os.makedirs(os.path.dirname(dest_file_path))

        if iw_args.copyright is not None:
            save_with_meta(marked_image,
                           dest_file_path,
                           iw_args.copyright)

        else:
            marked_image.save(dest_file_path, quality=100)
        print("Marked: {fp}".format(fp=image_file_path))
    except IOError:
        print("Error file (will be copy): {fp}".format(fp=image_file_path))
        normal_files.append(image_file_path)
        pass

for normal_file_path in normal_files:
    try:
        dest_file_path = normal_file_path.replace(
            iw_args.source_dir,
            iw_args.dest_dir
        )
        if not os.path.exists(os.path.dirname(dest_file_path)):
            os.makedirs(os.path.dirname(dest_file_path))
        copyfile(normal_file_path, dest_file_path)
        print("Copied: {fp}".format(fp=normal_file_path))
    except IOError:
        print("Error file (no copy): {fp}".format(fp=normal_file_path))
        pass
