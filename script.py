# If the library is not present, install it with the command:
# pip install opencv-python
import cv2 as cv
import numpy as np

def align_images(img1, img2):
    height, width = img1.shape[:2]
    center = (width//2, height//2)

    # Syntax = (start, stop, step) step doesnt work. Make it work
    # Finetune these values
    x_range = (-2, 2, 0.1)   # Step of 0.1
    y_range = (-2, 2, 0.1)   # Step of 0.1
    rotation_range = (-1, 1, 0.1)    # Step of 0.1

    rotate_matrix = cv.getRotationMatrix2D(center=center, angle=1, scale=1)
    rotated_img = cv.warpAffine(src=img2, M=rotate_matrix, dsize=(width, height))

    # cv.imshow("rotated image OR", cv.bitwise_or(rotated_img, img1))

    # x = 5
    # y = 5
    # translation_matrix = np.array([
    #     [1, 0, x],
    #     [0, 1, y]
    # ], dtype=np.float32)
    # translated_image = cv.warpAffine(src=img2, M=translation_matrix, dsize=(width, height))
    # cv.imshow("translated image OR", cv.bitwise_or(translated_image, img1))

    for x in range(x_range[0], x_range[1]):
        for y in range(y_range[0], y_range[1]):
            translation_matrix = np.array([
                [1, 0, x],
                [0, 1, y]
            ], dtype=np.float32)
            translated_image = cv.warpAffine(src=img2, M=translation_matrix, dsize=(width, height))
            for angle in range(rotation_range[0], rotation_range[1]):
                rotate_matrix = cv.getRotationMatrix2D(center=center, angle=angle, scale=1)
                rotated_image = cv.warpAffine(src=translated_image, M=rotate_matrix, dsize=(width, height))
                bitwise_or_img = cv.bitwise_or(img1, rotated_image)
                # if np.allclose(bitwise_or_img, img1):
                #     cv.imshow("Match", bitwise_or_img)
                #     print(f"x={x}, y={y}, angle={angle}")
                #     return
                cv.imshow(f"x={x}, y={y}, angle={angle}", bitwise_or_img)

def preprocess_image(img):
    # Convert image to grayscale
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    # Thresholding
    thresh = 60
    max_val = 255   # Color range is from 0 to 255
    ret, img = cv.threshold(img, thresh, max_val, cv.THRESH_BINARY)

    # Canny Edge Detection
    thresh1 = 50
    thresh2 = 150
    img = cv.Canny(img, thresh1, thresh2)

    # Return the image
    return img



# Reading the images
cap1 = cv.imread("./images/good.jpg")
cap2 = cv.imread("./images/bad.jpg")

img1 = preprocess_image(cap1)
img2 = preprocess_image(cap2)

# Displaying the read images
# cv.imshow("Original 1", cap1)
# cv.imshow("Original 2", cap2)

# # Converting image to grayscale
# img1 = cv.cvtColor(cap1, cv.COLOR_BGR2GRAY)
# img2 = cv.cvtColor(cap2, cv.COLOR_BGR2GRAY)


# # Thresholding
# thresh = 60
# max_val = 255   # Color range is from 0 to 255
# ret, img1 = cv.threshold(img1, thresh, max_val, cv.THRESH_BINARY)
# ret, img2 = cv.threshold(img2, thresh, max_val, cv.THRESH_BINARY)

# # Canny Edge Detection
# thresh1 = 50
# thresh2 = 150
# img1 = cv.Canny(img1, thresh1, thresh2)
# img2 = cv.Canny(img2, thresh1, thresh2)

# Displaying the images
cv.imshow("Image 1", img1)
cv.imshow("Image 2", img2)

# Displaying the image formed by performing bitwise AND on the two samples
# cv.imshow("Filtered AND", cv.bitwise_and(img1, img2))

# # Displaying the image formed by performing bitwise AND on the two samples
# cv.imshow("Filtered OR", cv.bitwise_or(img1, img2))

# align_images(img1, img2)

# cv.imshow("Filtered XOR1", cv.bitwise_xor(img1, img2))
# cv.imshow("Filtered XOR2", cv.bitwise_xor(img2, img1))

cv.waitKey(0)
