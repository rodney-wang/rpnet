from torch.utils.data import *
from imutils import paths
import cv2
import numpy as np
from ocr_utils import encode_plate


class labelFpsDataLoader(Dataset):
    def __init__(self, co_list, imgSize, is_transform=None):
        """
        :param co_list: List file contains the images;corners;ocr
        :param imgSize:
        :param is_transform:
        """
        #self.img_dir = img_dir
        self.img_paths = []
        self.corners = []
        self.ocrs =[]
        with open(co_list, "r") as ff:
            for line in ff:
                img_path, corner_str, ocr = line.split(';')
                self.img_paths.append(img_path)
                corner = [int(i) for i in corner_str.split(',')]
                self.corners.append(corner)
                ocr = ocr.strip().decode('utf8')
                self.ocrs.append(ocr)

        self.img_size = imgSize
        self.is_transform = is_transform

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, index):
        img_name = self.img_paths[index]
        img = cv2.imread(img_name)
        # img = img.astype('float32')
        resizedImage = cv2.resize(img, self.img_size)
        resizedImage = np.transpose(resizedImage, (2,0,1))
        resizedImage = resizedImage.astype('float32')
        resizedImage /= 255.0

        lbl = encode_plate(self.ocrs[index])

        corners = self.corners[index]
        x_max = int(max(corners[::2]))
        y_max = int(max(corners[1::2]))
        x_min = int(min(corners[::2]))
        y_min = int(min(corners[1::2]))
        leftUp     = [x_min, y_min]
        rightDown  = [x_max, y_max]

        #[leftUp, rightDown] = [[int(eel) for eel in el.split('&')] for el in iname[2].split('_')]
        ori_w, ori_h = float(img.shape[1]), float(img.shape[0])
        new_labels = [(leftUp[0] + rightDown[0]) / (2 * ori_w), (leftUp[1] + rightDown[1]) / (2 * ori_h),
                      (rightDown[0] - leftUp[0]) / ori_w, (rightDown[1] - leftUp[1]) / ori_h]

        return resizedImage, new_labels, lbl, img_name


class labelTestDataLoader(Dataset):
    def __init__(self, co_list, imgSize, is_transform=None):
        self.img_paths = []
        self.corners = []
        self.ocrs =[]
        with open(co_list, "r") as ff:
            for line in ff:
                img_path, corner_str, ocr = line.split(';')
                self.img_paths.append(img_path)
                corner = [int(i) for i in corner_str.split(',')]
                self.corners.append(corner)
                ocr = ocr.strip().decode('utf8')
                self.ocrs.append(ocr)

        self.img_size = imgSize
        self.is_transform = is_transform

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, index):
        img_name = self.img_paths[index]
        img = cv2.imread(img_name)
        resizedImage = cv2.resize(img, self.img_size)
        resizedImage = np.transpose(resizedImage, (2,0,1))
        resizedImage = resizedImage.astype('float32')
        resizedImage /= 255.0

        lbl = encode_plate(self.ocrs[index])
        return resizedImage, lbl, img_name



class ChaLocDataLoader(Dataset):
    def __init__(self, co_list, imgSize, is_transform=None):
        self.img_paths = []
        self.corners = []
        #self.ocrs = []
        with open(co_list, "r") as ff:
            for line in ff:
                img_path, corner_str, ocr = line.split(';')
                self.img_paths.append(img_path)
                corner = [int(i) for i in corner_str.split(',')]
                self.corners.append(corner)
                #ocr = ocr.strip().decode('utf8')
                #self.ocrs.append(ocr)

        self.img_size = imgSize
        self.is_transform = is_transform

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, index):
        img_name = self.img_paths[index]
        img = cv2.imread(img_name)
        # img = img.astype('float32')
        resizedImage = cv2.resize(img, self.img_size)
        resizedImage = np.transpose(resizedImage, (2,0,1))
        resizedImage = resizedImage.astype('float32')
        resizedImage /= 255.0

        corners = self.corners[index]
        x_max = int(max(corners[::2]))
        y_max = int(max(corners[1::2]))
        x_min = int(min(corners[::2]))
        y_min = int(min(corners[1::2]))
        leftUp     = [x_min, y_min]
        rightDown  = [x_max, y_max]

        ori_w, ori_h = float(img.shape[1]), float(img.shape[0])
        new_labels = [(leftUp[0] + rightDown[0]) / (2 * ori_w), (leftUp[1] + rightDown[1]) / (2 * ori_h),
                      (rightDown[0] - leftUp[0]) / ori_w, (rightDown[1] - leftUp[1]) / ori_h]

        #print(img_name, corners, new_labels)
        return resizedImage, new_labels


class demoTestDataLoader(Dataset):
    def __init__(self, img_dir, imgSize, is_transform=None):
        self.img_dir = img_dir
        self.img_paths = []
        for i in range(len(img_dir)):
            self.img_paths += [el for el in paths.list_images(img_dir[i])]
        # self.img_paths = os.listdir(img_dir)
        # print self.img_paths
        self.img_size = imgSize
        self.is_transform = is_transform

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, index):
        img_name = self.img_paths[index]
        img = cv2.imread(img_name)
        # img = img.astype('float32')
        resizedImage = cv2.resize(img, self.img_size)
        resizedImage = np.transpose(resizedImage, (2,0,1))
        resizedImage = resizedImage.astype('float32')
        resizedImage /= 255.0
        return resizedImage, img_name
