import os
from pathlib import Path


def delete_unannotated(images_filepath, labels_filepath):
    img_paths = []
    for root, dirs, files in os.walk(images_filepath):
        for filename in files:
            modified_filename = filename[:-3] + r'xml'
            img_paths.append(modified_filename)

    label_paths = []
    for root, dirs, files in os.walk(labels_filepath):
        for filename in files:
            label_paths.append(filename)

    for img_path in img_paths:
        if img_path not in label_paths:
            actual_img_name = img_path[:-3] + r'jpg'
            full_img_path = r'C:\Users\justi\Downloads\DDR-dataset_test-val_fused\Images' + '\\' + actual_img_name
            os.remove(full_img_path)

    # since there were 2 labels that had no associated image, I had to find + remove them
    # for label_path in label_paths:
    #     if label_path not in img_paths:
    #         actual_lbl_name = label_path[:-3] + r'xml'
    #         full_lbl_path = r'C:\Users\justi\Downloads\DDR-dataset_test-val_fused\labels' + '\\' + actual_lbl_name
    #         os.remove(full_lbl_path)


images_filepath = r'C:\Users\justi\Downloads\DDR-dataset_test-val_fused\Images'
labels_filepath = r'C:\Users\justi\Downloads\DDR-dataset_test-val_fused\labels'
delete_unannotated(images_filepath, labels_filepath)