from PIL import Image, ImageDraw, ImageFont, ImageMath, ImageStat, ImageFilter
import json
import numpy as np
from os import walk
import random
from itertools import combinations

random.seed(42)

def extract_common_background(imgs):
    # random.shuffle(imgs)
    # imgs[0].show()
    ans = np.asarray(imgs[0])*0
    combs = list(combinations(imgs, 2))
    random.shuffle(combs)

    for cnt, (i,j) in enumerate(combs):
        out = np.bitwise_xor(i, j)
        i_np = np.asarray(i)
        out[:,:] = np.all(out[:,:] == [0, 0, 0], axis=2).reshape(out.shape[0], out.shape[1], 1) * i_np[:,:]

        mask = np.all(ans < 15, axis=2).reshape(out.shape[0], out.shape[1], 1) * np.all(i_np > 50, axis=2).reshape(out.shape[0], out.shape[1], 1)
        ans += out * mask
        if cnt % 200 == 0:
            Image.fromarray(ans).show()
    
    print("Done")            

def cut_img_set(img_set_path):
    start_x = 98
    start_y = 246

    card_width = 662
    card_height = 993

    img_set_np = np.asarray(Image.open(img_set_path))

    imgs = []
    for r in range(2):
        cy = start_y + r * card_height
        for c in range(5):
            cx = start_x + c * card_width
            cut_img_np = img_set_np[cy:cy+card_height,cx:cx+card_width,:]
            if np.any(np.all(cut_img_np[:,:,:3] == [0, 80, 149], axis=2)):
                print(f'Bad: {path} {r} {c}')
                continue
            imgs.append(Image.fromarray(cut_img_np))
    
    return imgs


img_set_paths = [
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-1(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-2(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-3(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-4(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-5(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-6(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-7(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-8(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-9(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-10(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-11(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-12(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-13(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-14(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-15(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-16(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-17(18).jpg',
    # './Munchkin Fallout 2.0 PNP/Doors/Doors-18(18).jpg',
    './Munchkin Fallout 2.0 PNP/Treasures/Treasures-1(19).jpg',
    './Munchkin Fallout 2.0 PNP/Treasures/Treasures-2(19).jpg',
    './Munchkin Fallout 2.0 PNP/Treasures/Treasures-3(19).jpg',
    './Munchkin Fallout 2.0 PNP/Treasures/Treasures-4(19).jpg',
    './Munchkin Fallout 2.0 PNP/Treasures/Treasures-5(19).jpg',
    './Munchkin Fallout 2.0 PNP/Treasures/Treasures-6(19).jpg',
]


imgs = []
for path in img_set_paths:
    imgs += cut_img_set(path)

extract_common_background(imgs)
