import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk

# GLOBAL VARIABLES
current_region = 0
render_mode = False
g_cv_img = None

def preprocess_image(img):
    # Convert image to grayscale
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    # Thresholding
    thresh = 60
    max_val = 255   # Color range is from 0 to 255
    _, img = cv.threshold(img, thresh, max_val, cv.THRESH_BINARY)

    # Canny Edge Detection
    thresh1 = 50
    thresh2 = 150
    img = cv.Canny(img, thresh1, thresh2)

    # Return the image
    return img

def getImageRegion(img_cv):
    global current_region
    start_w = (current_region%3) * (IMG_WIDTH)//3
    start_h = (current_region//3) * (IMG_HEIGHT)//2
    img_region = img_cv[start_h:(start_h + (IMG_HEIGHT)//2), start_w:(start_w + (IMG_WIDTH)//3)]
    zoom_value = 2.0
    img_resize = cv.resize(img_region, None, fx=zoom_value, fy=zoom_value)
    return img_resize

def getTkImage(img_cv):
    img = Image.fromarray(img_cv)
    imgtk = ImageTk.PhotoImage(image=img)
    return imgtk

def renderImage(img_cv):
    _imgtk = getTkImage(img_cv)
    label_img.configure(image=_imgtk)
    label_img.image = _imgtk

def setPrevNextBtnState():
    if current_region <= 0:
        button_prev['state'] = tk.DISABLED
        button_next['state'] = tk.NORMAL
    elif current_region >= 5:
        button_prev['state'] = tk.NORMAL
        button_next['state'] = tk.DISABLED
    else:
        button_prev['state'] = tk.NORMAL
        button_next['state'] = tk.NORMAL

def prevBtnClicked():
    global current_region
    current_region = current_region - 1
    label_heading['text'] = f'Region {current_region+1}'
    img_cv = getImageRegion(g_cv_img)
    renderImage(img_cv)
    setPrevNextBtnState()

def nextBtnClicked():
    global current_region
    current_region = current_region + 1
    label_heading['text'] = f'Region {current_region+1}'
    img_cv = getImageRegion(g_cv_img)
    renderImage(img_cv)
    setPrevNextBtnState()

def renderFullBtnClicked():
    global render_mode
    if render_mode is False:
        render_mode = True
        label_heading['text'] = f'Region {current_region+1}'
        button_render_full['text'] = 'full'
        setPrevNextBtnState()
        img_cv = getImageRegion(g_cv_img)
        renderImage(img_cv)
    else:
        render_mode = False
        label_heading['text'] = "Click on render to view regions"
        button_render_full['text'] = 'render'
        button_prev['state'] = tk.DISABLED
        button_next['state'] = tk.DISABLED
        renderImage(g_cv_img)

def displayCamCapture():
    global label_img_callback_id
    global g_cv_img
    _, frame = cam_cap.read()
    g_cv_img = preprocess_image(frame)
    renderImage(g_cv_img)
    label_img_callback_id = label_img.after(10, displayCamCapture)

def resetApplication():
    global current_region
    current_region = 0
    displayCamCapture()
    button_capture_back['text'] = "capture"
    label_heading['text'] = "Click on capture to start"
    button_render_full['text'] = "render"
    button_render_full['state'] = tk.DISABLED
    button_prev['state'] = tk.DISABLED
    button_next['state'] = tk.DISABLED

def captureBackBtnClicked():
    global label_img_callback_id
    if label_img_callback_id is not None:
        label_img.after_cancel(label_img_callback_id)
        label_img_callback_id = None
        button_capture_back['text'] = "back"
        label_heading['text'] = "Click on render to view regions"
        button_render_full['state'] = tk.NORMAL
    else:
        resetApplication()


# MAIN
root = tk.Tk()
root.wm_title("Ka Naada Image Validator")

IMG_MAX_WIDTH = root.winfo_screenwidth() - 100
IMG_MAX_HEIGHT = root.winfo_screenheight() - 100
cam_cap = cv.VideoCapture(0)
cam_cap.set(cv.CAP_PROP_FRAME_WIDTH, IMG_MAX_WIDTH)
cam_cap.set(cv.CAP_PROP_FRAME_HEIGHT, IMG_MAX_HEIGHT)
IMG_WIDTH = int(cam_cap.get(cv.CAP_PROP_FRAME_WIDTH))
IMG_HEIGHT = int(cam_cap.get(cv.CAP_PROP_FRAME_HEIGHT))
print(IMG_MAX_WIDTH, IMG_MAX_HEIGHT)
print(IMG_WIDTH, IMG_HEIGHT)

label_heading = tk.Label(root, text="Click on capture to start")
label_heading.pack()
label_img = tk.Label(root, image=None)
label_img_callback_id = None
label_img.pack()
frame_for_buttons = tk.Frame(root)
frame_for_buttons.pack()
button_capture_back = tk.Button(frame_for_buttons, text="capture", command=captureBackBtnClicked)
button_render_full = tk.Button(frame_for_buttons, text="render", command=renderFullBtnClicked, state=tk.DISABLED)
button_prev = tk.Button(frame_for_buttons, text="prev", command=prevBtnClicked, state=tk.DISABLED)
button_next = tk.Button(frame_for_buttons, text="next", command=nextBtnClicked, state=tk.DISABLED)
button_capture_back.grid(row=0, column=0, padx=10, pady=5)
button_render_full.grid(row=0, column=1, padx=10, pady=5)
button_prev.grid(row=0, column=2, padx=10, pady=5)
button_next.grid(row=0, column=3, padx=10, pady=5)

displayCamCapture()
root.mainloop()