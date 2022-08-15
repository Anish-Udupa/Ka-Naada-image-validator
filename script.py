# If the library is not present, install it with the command:
# pip install opencv-python
import cv2 as cv

# Reading the images
cap1 = cv.imread("./images/good.jpg")
cap2 = cv.imread("./images/bad.jpg")

# Displaying the read images
cv.imshow("Original 1", cap1)
cv.imshow("Original 2", cap2)

# Converting image to grayscale
img1 = cv.cvtColor(cap1, cv.COLOR_BGR2GRAY)
img2 = cv.cvtColor(cap2, cv.COLOR_BGR2GRAY)


# Thresholding
thresh = 60
max_val = 255   # Color range is from 0 to 255
ret, img1 = cv.threshold(img1, thresh, max_val, cv.THRESH_BINARY)
ret, img2 = cv.threshold(img2, thresh, max_val, cv.THRESH_BINARY)

# Canny Edge Detection
thresh1 = 50
thresh2 = 150
img1 = cv.Canny(img1, thresh1, thresh2)
img2 = cv.Canny(img2, thresh1, thresh2)

# Displaying the images
cv.imshow("Image 1", img1)
cv.imshow("Image 2", img2)

# Displaying the image formed by performing bitwise AND on the two samples
cv.imshow("Filtered AND", cv.bitwise_and(img1, img2))

# Displaying the image formed by performing bitwise AND on the two samples
cv.imshow("Filtered OR", cv.bitwise_or(img1, img2))

# cv.imshow("Filtered XOR1", cv.bitwise_xor(img1, img2))
# cv.imshow("Filtered XOR2", cv.bitwise_xor(img2, img1))

cv.waitKey(0)
