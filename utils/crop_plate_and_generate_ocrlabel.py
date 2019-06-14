#coding=utf-8
import os
import argparse
import re
import numpy as np
import cv2
import glob
import json
import codecs
import pdb
from cutplate import four_point_transform

provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "O"]
alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z', 'O']
ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
       'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']

def parse_corner_str(corner_str):
    pts = corner_str.split('_')
    corners = []
    for pt in pts:
        xy = pt.split('&')
        corners.append(int(xy[0]))
        corners.append(int(xy[1]))
    return corners

def parse_ocr_str(ocr_str):
    labels = ocr_str.split('_')
    pp = int(labels[0])
    aa = int(labels[1])
    dd = labels[2:]
    digits = [ ads[int(ii)] for ii in dd]
    ocr_chars = [provinces[pp], alphabets[aa]]
    ocr_chars = ocr_chars + digits

    ocr = ''.join(ocr_chars)
    return ocr


def write_plate_image(img_path, out_dir, label_txt):
    """
    Crop the plate from the car image according to label results (json file),
    and write it to out_dir

    If there is multiple rows in a plate, (like hongkong plate),
    write multiple plate images into files.
    """
    corner = json.load(open(json_path))

    car_images = glob.glob(img_path + '*/*.jpg')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    fo = codecs.open(label_txt, "w", encoding='utf-8')

    for i, image_name in enumerate(car_images):
        if i >5:
            continue
        fname_split = os.path.basename(image_name).split('_')
        if len(fname_split) <6:
            continue
        corner_str, ocr_str = fname_split[3], fname_split[4]
        corners = parse_corner_str(corner_str)
        ocr     = parse_ocr_str(ocr_str)

        print('### {}: Processing {}'.format(i, bname.encode('utf8')))
        if len(corners) < 8:
            print('{}: {} length of pts shorter than 8'.format(i, image_name))
            continue
        img = imread(image_name)
        if img is None:
            continue
        plate_img = four_point_transform(img, corner_pts)
        out_path = os.path.join(out_dir, bname.replace('.jpg', '_plate.jpg'))
        cv2.imwrite(out_path, plate_img)

        plate_ocr = ocr.strip()
        plate_ocr = plate_ocr.replace(' ', '')
        plate_label = '|' + '|'.join(plate_ocr.decode('utf8')) + '|'
        line = out_path + ';' + plate_label + '\n'
        print line
        fo.write("%s" % line)

    fo.close()


def parse_args():
    parser = argparse.ArgumentParser(description='Plate end to end test')
    parser.add_argument('--img_dir', default='/ssd/wfei/data/plate_for_label/hongkong/hkia_car_crop/caffe_crop/',
                        type=str, help='Input test image dir')
    parser.add_argument('--plate_dir', default='/ssd/wfei/data/plate_for_label/hongkong/plates/',
                        type=str, help='Output plate image dir')
    parser.add_argument('--label_txt', default='/ssd/wfei/data/plate_for_label/hongkong/hkia_car_ocrlabel.txt',
                        type=str, help='Output OCR label txt')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    write_plate_image(args.img_dir, args.plate_dir, args.label_txt)

