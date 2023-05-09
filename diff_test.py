import numpy as np
import matplotlib.pyplot as plt
import cv2

img1 = cv2.imread('demo/in.png')
img2 = cv2.imread('demo/out.png')
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
h, w = img1_gray.shape


def error(img1, img2):
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff ** 2)
    mse = err / (float(h * w))
    msre = np.sqrt(mse)
    return mse, diff


match_error12, diff12 = error(img1_gray, img2_gray)

print("Image matching Error between image 1 and image 2:", match_error12)
img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
plt.subplot(221), plt.imshow(img1), plt.title("Input"), plt.axis('off')
plt.subplot(222), plt.imshow(img2), plt.title("Output"), plt.axis('off')
plt.subplot(223), plt.imshow(diff12, 'gray'), plt.title("Diff"), plt.axis('off')
plt.rcParams['figure.figsize'] = (20, 7)
# plt.show()
plt.savefig('demo/diff.png')
