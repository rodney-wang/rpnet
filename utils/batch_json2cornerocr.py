import os
from json_2_corner_ocr import json_to_ocrtxt


img_json_pair = {
        '/ssd/wfei/data/plate_detection/images/wanda_20180921_crop':
                '/ssd/wfei/data/plate_detection/images/20181119_carplate_wanda_0921.json',
        '/ssd/wfei/data/plate_for_label/wanda_10k/20190311_wanda_1w_plate_det_benchmark_fixed.json':
                '/ssd/wfei/data/plate_for_label/wanda_10k/wanda_10k_filtered',
        '/ssd/wfei/data/plate_for_label/wanda_generic_15k/20190531_wanda_generic_15k.json':
                '/ssd/wfei/data/plate_for_label/wanda_generic_15k/images',
        '/ssd/wfei/data/plate_for_label/wanda_entrance/20190604_wanda_entrance_may2829.json':
                '/ssd/wfei/data/plate_for_label/wanda_entrance/images',
        '/ssd/wfei/data/plate_for_label/energy_wanda/20190601_energy_wanda_16k.json':
                '/ssd/wfei/data/plate_for_label/energy_wanda/images',
        '/ssd/wfei/data/plate_for_label/k11_1003/20181101_carplate_k11_1003.json':
                '/ssd/wfei/data/plate_for_label/k11_1003/crops'
}

out_folder = '/ssd/wfei/code/rpnet/data/train_label/'
for img_dir, json_label in img_json_pair.iteritems():
        json_name = os.path.basename(json_label)
        cornerocr_txt = json_name.replace('.json', '_cornerocr.txt')
        out_txt = os.path.join(out_folder, cornerocr_txt)
        json_to_ocrtxt(json_label, out_txt, img_dir)