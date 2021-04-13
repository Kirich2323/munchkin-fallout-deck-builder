from PIL import Image, ImageDraw, ImageFont, ImageMath, ImageStat, ImageFilter
import json
import numpy as np
from os import walk

def bfs(img, start_x, start_y):
    ans = img.copy()
    visited = set((start_x,start_y))
    q = [(start_x,start_y)]
    while len(q) > 0:
        x,y = q.pop(0)
        for dir in [(0,1),(0,-1),(1,0),(-1,0)]:
            new_x = x + dir[0]
            new_y = y + dir[1]

            if (new_x, new_y) not in visited and new_x >= 0 and new_x < img.shape[1] and new_y >= 0 and new_y < img.shape[0]:
                visited.add((new_x, new_y))
                pixel = ans[new_y, new_x,:3]
                alpha = ans[new_y, new_x, 3]
                if sum(pixel) > 90:
                    ans[new_y, new_x,:] = [0,0,0,max(0, 255-sum(pixel))]
                    q.append((new_x, new_y))
                
    return ans


in_dir = './imgs/elements_to_cut/'
out_dir = './imgs/cut_elements/'

_, _, filenames = next(walk(in_dir))

src_to_out = {
    './imgs/cut_elements/trap_baseball_pitcher.png': './imgs/trap_baseball_pitcher.png'
}

for fname in filenames:
    img = Image.open(in_dir+fname)
    img_np = np.asarray(img)
    print(fname, img_np.shape)

    img_np = bfs(img_np, 0, 0)
    for y in range(img_np.shape[0]):
        for x in range(img_np.shape[1]):
            if np.array_equal(img_np[y,x,:3], [255, 41, 112]):
                img_np = bfs(img_np, x, y)

    img = Image.fromarray(img_np)
    img.save(out_dir+fname)