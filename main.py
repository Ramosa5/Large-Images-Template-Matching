import cv2
import numpy as np

img = cv2.imread('./photos/ushuaia.jpg')

height, width, x = img.shape

r = np.zeros((height, width))
g = np.zeros((height, width))
b = np.zeros((height, width))
r2 = np.zeros((height, width))
g2 = np.zeros((height, width))
b2 = np.zeros((height, width))

for i in range(height):
    for j in range(width):
        b[i, j] = img[i, j, 0]
        g[i, j] = img[i, j, 1]
        r[i, j] = img[i, j, 2]

print(height, width)

bound_r = np.zeros((height, width), dtype=np.uint8)
bound_g = np.zeros((height, width), dtype=np.uint8)
bound_b = np.zeros((height, width), dtype=np.uint8)
check = np.zeros((height, width), dtype=np.uint8)

highest = 0
lowest = 160
right = 160
left = 0
detected = []
w_det_buf = 0
h_buf = 0

for i in range(int(height)):
    for j in range(int(width)):
        bound_r[i, j] = r[i, j]
        bound_g[i, j] = g[i, j]
        bound_b[i, j] = b[i, j]
        if np.abs(r[i, j] - 251) < 8 and np.abs(g[i, j] - 177) < 8 and np.abs(b[i, j] - 171) < 8 and check[i, j] != 254:
            detected.append([i-50, i + 50, j + 50, j - 50])
            for k in range(i-100, i + 100):
                for l in range(j - 100, j + 100):
                    if k > height-1:
                        k = height-1
                    if l > width-1:
                        l = width-1
                    check[k, l] = 254

w_buf = 0
found = False
high1 = 0
high2 = 0
low1 = 0
low2 = 0
mid1 = 0
mid2 = 0
left_bound = 0
boundings = []
precision = 12
second_ver = []

for box in detected:
    print('box')
    highest = box[0]
    lowest = box[1]
    right = box[2]
    left = box[3]
    found = False
    one_det_buf = 0
    two_det_buf = 0
    three_det_buf = 0
    # print(highest, lowest, right, left)
    for i in range(highest, lowest):
        w_buf = 0
        if not found:
            for j in range(left, right):
                if i > height - 1:
                    i = height - 1
                if j > width - 1:
                    j = width - 1
                if np.abs(r[i, j] - 110) < precision and np.abs(g[i, j] - 20) < precision and np.abs(b[i, j] - 25) < precision:
                    one_det_buf += 1
                    # print('ke')
                    if one_det_buf == 5:
                        low1 = i
                        low2 = j
                    # w_buf = 30
                    j_buf = j
                    i_buf = i
                if np.abs(r[i, j] - 251) < precision and np.abs(g[i, j] - 177) < precision and np.abs(b[i, j] - 161) < precision:
                    two_det_buf += 1
                    j2_buf = j
                    i2_buf = i
                    if two_det_buf == 5:
                        mid1 = i
                        mid2 = j
                if np.abs(r[i, j] - 41) < precision and np.abs(g[i, j] - 58) < precision and np.abs(b[i, j] - 39) < precision:
                    three_det_buf += 1
                    j3_buf = j
                    i3_buf = i
                    if three_det_buf == 3:
                        high1 = i
                        high2 = j
                # if np.abs(r[i, j] - 95) + np.abs(g[i, j] - 95) + np.abs(b[i, j] - 69) < precision:
                #     w_det_buf += 1
                if one_det_buf>5:
                    one_det_buf = 5
                if two_det_buf > 5:
                    two_det_buf = 5
                if three_det_buf > 3:
                    three_det_buf = 3
                buff = one_det_buf+two_det_buf+three_det_buf
                if buff==13 and (i_buf<i2_buf<i3_buf or i3_buf<i2_buf<i_buf or j_buf<j2_buf<j3_buf or j3_buf<j2_buf<j_buf):
                    found = True
                    if np.abs(high1-low1) > np.abs(high2-low2):
                        boundings.append((high1, low1, mid1, mid2))
                    else:
                        boundings.append((high2, low2, mid1, mid2))
                    second_ver.append(box)
                    print(i, j)
                    break
                if w_buf > 0:
                    w_buf -= 1

for box in boundings:
    high = box[0]
    low = box[1]
    mid1 = box[2]
    mid2 = box[3]
    print(high, low, mid1, mid2)
    dim = int(np.abs(high-low))
    for i in range(mid1-dim, mid1+dim):
        bound_r[i, mid2 - dim] = 0
        bound_g[i, mid2 - dim] = 255
        bound_b[i, mid2 - dim] = 0
        bound_r[i, mid2 + dim] = 0
        bound_g[i, mid2 + dim] = 255
        bound_b[i, mid2 + dim] = 0
    for j in range(mid2 - dim, mid2 + dim,):
        bound_r[mid1-dim, j] = 0
        bound_g[mid1-dim, j] = 255
        bound_b[mid1-dim, j] = 0
        bound_r[mid1+dim, j] = 0
        bound_g[mid1+dim, j] = 255
        bound_b[mid1+dim, j] = 0

rgb_array2 = np.dstack((bound_b, bound_g, bound_r))
cv2.imwrite('output6.png', rgb_array2)
