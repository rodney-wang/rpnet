#coding=utf-8

"""
encode and decode a plate
e.g.
粤AF56839   [19, 0, 5, 29, 30, 32, 27, 33]
"""
provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "-"]
alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z', '-']
ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
       'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '港', '澳', '警', '学', '-']

prov_map = {p.decode('utf8'):index for index, p in enumerate(provinces)}
albe_map = {p:index for index, p in enumerate(alphabets)}
ads_map  = {p.decode('utf8'):index for index, p in enumerate(ads)}

def encode_plate(plate_ocr):
    pcode  = prov_map[plate_ocr[0]]
    abcode = albe_map[plate_ocr[1]]
    plate_code = []
    plate_code.extend([pcode, abcode])
    for char in plate_ocr[2:]:
        plate_code.append(ads_map[char])
    #if seven digits plate, append '-' to the string
    if len(plate_ocr) == 7:
        plate_code.append(38)

    pcode = [str(i) for i in plate_code]
    return '_'.join(pcode)


