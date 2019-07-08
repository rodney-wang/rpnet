#coding=utf-8
import os
import argparse
import cv2
import glob
import json
import codecs
from shutil import copyfile
#from cutplate import four_point_transform

"""
Convert the json labels into box&ocr txt, 
txt label is in the following format: 
filename; corners; ocrtxt
e.g. 
1540450977637959529_plate.jpg; 12,315,400,20,400,55,500,200; 粤AD21811

Write the valid plates into out_folder 
"""

chars = "1234567890QWERTYUPASDFGHJKLZXCVBNM京鄂津湘冀粤晋桂蒙琼辽渝吉川黑贵沪云苏藏浙陕皖甘闽青赣宁鲁新豫警港澳使领学试挂".decode('utf8')
provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "O"]
alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z', 'O']
ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
       'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '港', '澳', '警', '学', 'O']


def encode_plate(plate_ocr):

    return None

def json_to_ocrtxt(json_file, ocrtxt_file, img_dir):

    json_data = json.load( open(json_file, 'r' ) )
    i=0
    fo = codecs.open(ocrtxt_file, "w", encoding='utf-8')

    for fname, label in json_data.iteritems():
        ocr = label[0]['text'].strip()

        if ocr is None or len(ocr) ==0:
            continue
        fpath = os.path.join(img_dir, fname)
        if not os.path.exists(fpath):
            continue

        plate_ocr = ocr.strip()
        plate_ocr = plate_ocr.replace('-', '')
        plate_code = encode_plate(plate_ocr)

        print '### Processing ', i, fname, ocr
        if plate_ocr.encode('utf8')[0:3] in provinces:
            cor = label[0]["coordinates"]
            #cor = cor.split(',')
            print plate_ocr, len(plate_ocr), cor
        else:
            continue
        if len(cor) < 8:
            continue
        corner_str = [str(i) for i in cor[:8]]
        corner_str = ','.join(corner_str)

        line = fpath + ';' + corner_str + ';' + plate_ocr + '\n'
        fo.write("%s" % line)
        i += 1
    print "Json label file converted to boxocr file", ocrtxt_file


def parse_args():
    parser = argparse.ArgumentParser(description='Plate end to end test')
    parser.add_argument('--json', default='/ssd/wfei/data/plate_for_label/energy_cars/20190221/20190329_energy_car_20190221.json',
                        type=str, help='Label file in Json format')
    parser.add_argument('--img_dir', default='/ssd/wfei/data/plate_for_label/energy_cars/20190221/car_crop',
                        type=str, help='Input image dir')
    parser.add_argument('--label_txt', default='/ssd/wfei/code/rpnet/data/train_label/20190221_energy_cars_plates_corner_ocr.txt',
                        type=str, help='Plate label file in txt format')

    args = parser.parse_args()
    return args



if __name__ == '__main__':

    args = parse_args()
    json_to_ocrtxt(args.json, args.label_txt, args.img_dir)

