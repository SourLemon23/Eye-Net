import os
from pathlib import Path
import shutil
from xml.etree import ElementTree


labels_filepath = r'C:\Users\justi\Downloads\DDR_lesions\labels'
# labels_filepath = r'C:\Users\justi\Downloads\dataset\train'
# labels_filepath2 = r'C:\Users\justi\Downloads\dataset\test'


def parse_annotations(abs_path):
    dom = ElementTree.parse(abs_path)

    img_width = float(dom.find('size/width').text)
    img_height = float(dom.find('size/height').text)

    classes = []
    class_names = dom.findall('object/name')
    for obj in class_names:
        if obj.text == 'ma':
            class_num = 0
        elif obj.text == 'he':
            class_num = 1
        elif obj.text == 'se':
            class_num = 2
        elif obj.text == 'ex':
            class_num = 3
        classes.append(class_num)

    xmins_list = []
    xmins = dom.findall('object/bndbox/xmin')
    for xmin in xmins:
        xmins_list.append(float(xmin.text))

    xmaxes_list = []
    xmaxes = dom.findall('object/bndbox/xmax')
    for xmax in xmaxes:
        xmaxes_list.append(float(xmax.text))

    ymins_list = []
    ymins = dom.findall('object/bndbox/ymin')
    for ymin in ymins:
        ymins_list.append(float(ymin.text))

    ymaxes_list = []
    ymaxes = dom.findall('object/bndbox/ymax')
    for ymax in ymaxes:
        ymaxes_list.append(float(ymax.text))

    x_centers = []
    y_centers = []
    widths = []
    heights = []
    for i in range(len(ymaxes_list)):
        x_center = (xmins_list[i] + xmaxes_list[i]) / 2
        x_center = x_center/img_width
        x_centers.append(x_center)

        y_center = (ymins_list[i] + ymaxes_list[i]) / 2
        y_center = y_center/img_height
        y_centers.append(y_center)

        width = (xmaxes_list[i] - xmins_list[i]) / img_width
        widths.append(width)

        height = (ymaxes_list[i] - ymins_list[i]) / img_height
        heights.append(height)

    return classes, x_centers, y_centers, widths, heights


train_file_name_no_exts = []
for root, dirs, files in os.walk(labels_filepath):
    for filename in files:
        abs_path = os.path.abspath(os.path.join(root, filename))
        # print('abs', abs_path)
        file_name_no_type = filename[:-4]
        # print('file_name_no_type', file_name_no_type)
        train_file_name_no_exts.append(file_name_no_type)

        classes, x_centers, y_centers, widths, heights = parse_annotations(abs_path)

        # print(classes[:3])
        # print(x_centers[:3])
        # print(y_centers[:3])
        # print(widths[:3])
        # print(heights[:3])

        txt_file_path = str((Path(abs_path).parent))[:-6] + 'Images\\' + str(filename[:-3]) + r'txt'
        print(txt_file_path)
        txt_file = open(txt_file_path, 'w')

        for i in range(len(classes)):
            txt_file.write(str(classes[i]) + ' ' + str(x_centers[i]) + ' ' + str(y_centers[i]) +  ' ' +
                str(widths[i]) + ' ' + str(heights[i]))
            if i != len(classes) - 1:
                txt_file.write('\n')
        txt_file.close()

# test_file_name_no_exts = []
# for root, dirs, files in os.walk(labels_filepath2):
#     for filename in files:
#         abs_path = os.path.abspath(os.path.join(root, filename))
#         # print('abs', abs_path)
#         file_name_no_type = filename[:-4]
#         # print('file_name_no_type', file_name_no_type)
#         test_file_name_no_exts.append(file_name_no_type)

# print(len(train_file_name_no_exts))
# print(len(test_file_name_no_exts))

# for test_file in test_file_name_no_exts:
#     if test_file in train_file_name_no_exts:
#         from_path = labels_filepath + "\\" + str(test_file) + r'.txt'
#         to_path = labels_filepath2 + "\\" + str(test_file) + r'.txt'
#         shutil.copyfile(from_path, to_path)