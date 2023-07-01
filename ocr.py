import cv2
# import pytesseract
import numpy as np
import easyocr


x = 555
y = 600
w = 144
h = 45

img = cv2.imread('/Users/bendyer/Downloads/test-ocr/2023-06-13-12-34-23-456872.jpg')

height, width, channels = img.shape

# show image dinmensions
print("width", width, "height", height)


# rotate image
center = (width/2, height/2)
rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=-7, scale=1)
rotated_img = cv2.warpAffine(src=img, M=rotate_matrix, dsize=(width, height))



cv2.rectangle(rotated_img,(x,y),(x+w,h+y), color=(0, 255, 0), thickness=1)
# cv2.imshow("output",rotated_img)
# cv2.waitKey(1)

roi = rotated_img[y:y+h, x:x+w]



# cv2.imshow("cropped",roi)
# cv2.waitKey(1)


# approach 1
# processed_img = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
# processed_img = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
# processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)

# approach 2
"""
processed_img = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
processed_img = cv2.resize(processed_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
# thr = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
thr = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4)
processed_img = cv2.bitwise_not(thr)
"""


# invert image

# thr = cv2.adaptiveThreshold(processed_img, 252, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 91, 93)
# processed_img = cv2.bitwise_not(thr)

# hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
# lower = np.array([0,0,0])
# upper = np.array([179,100,130])
# mask = cv2.inRange(hsv, lower, upper)
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
# close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
# extract = cv2.merge((close,close,close))


# thr = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# processed_img = cv2.bitwise_not(thr)


# processed_img = cv2.adaptiveThreshold(processed_img,252,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,91,93)
# processed_img = cv2.bitwise_not(processed_img)

# cv2.imshow("procesed",processed_img)
# cv2.waitKey(1)

# plate = pytesseract.image_to_string(processed_img, config='-l eng --oem 1 --psm 7') 
# plate = pytesseract.image_to_string(processed_img, config='-l eng --oem 1 --psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') 
# plate = pytesseract.image_to_string( processed_img, config='-l eng --oem 0 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') 
# print("oem0", plate)

##############

# x,y,w, h = int(coordinates[0]), int(coordinates[1]), int(coordinates[2]),int(coordinates[3])
#    img = img[y:h,x:w]

reader = easyocr.Reader(['en'], gpu=True)
gray = cv2.cvtColor(roi , cv2.COLOR_RGB2GRAY)
    #gray = cv2.resize(gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
result = reader.readtext(gray)
text = ""

for res in result:
    if len(result) == 1:
        text = res[1]
    if len(result) >1 and len(res[1])>6 and res[2]> 0.2:
        text = res[1]

##############



# plate = pytesseract.image_to_string( processed_img, config='-l eng --oem 1 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') 
# print("oem1", plate)

# plate = pytesseract.image_to_string( processed_img, config='-l eng --oem 2 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') 
# print("oem2", plate)


def ocr_image(img,coordinates):
    x,y,w, h = int(coordinates[0]), int(coordinates[1]), int(coordinates[2]),int(coordinates[3])
    img = img[y:h,x:w]

    gray = cv2.cvtColor(img , cv2.COLOR_RGB2GRAY)
    #gray = cv2.resize(gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
    result = reader.readtext(gray)
    text = ""

    for res in result:
        if len(result) == 1:
            text = res[1]
        if len(result) >1 and len(res[1])>6 and res[2]> 0.2:
            text = res[1]
    #     text += res[1] + " "
    
    return str(text)

"""
oem option 
0 (Legacy OCR Engine): This mode uses Tesseract's original OCR engine, which is based on a combination of traditional computer vision techniques and statistical models. It provides good accuracy for many cases but may not perform as well as newer engine modes in certain scenarios.

1 (Neural Nets LSTM Engine): This mode utilizes Tesseract's newer OCR engine, which is based on deep learning and recurrent neural networks (LSTM). It can deliver better accuracy, particularly for complex text layouts, difficult fonts, and languages with more complex scripts. However, it may be slower in some cases compared to the legacy engine.

2 (Default OCR Engine): This mode uses Tesseract's default OCR engine, which is a combination of both the legacy engine and the LSTM engine. It attempts to provide a balance between accuracy and speed, leveraging the strengths of both engine modes.

The default value for the oem option is usually set to 2 (Default OCR Engine) if not explicitly specified.

psm option

0 (Orientation and script detection (OSD) only): This mode performs only the orientation and script detection of the image without any further segmentation.

1 (Automatic page segmentation with OSD): This mode automatically detects the page structure and performs OCR on the detected regions. It is the default mode and works well for most cases.

2 (Automatic page segmentation, but no OSD or OCR): This mode automatically detects the page structure but skips the OSD and OCR steps. It can be useful if you only need the page layout information without extracting the text.

3 (Fully automatic page segmentation, with a single column of text): This mode assumes a single column of text and performs OCR accordingly. It is suitable for documents with a simple layout, such as articles or plain text.

4 (Assume a single uniform block of text): This mode assumes a single block of text and performs OCR accordingly. It is useful for documents with a uniform block of text, such as invoices or forms.

5 (Assume a single text line): This mode assumes a single line of text and performs OCR accordingly. It can be used for images containing a single line of text.

6 (Assume a single word): This mode assumes a single word and performs OCR accordingly. It is suitable for images containing a single word.

7 (Assume a single character): This mode assumes a single character and performs OCR accordingly. It can be used for images containing individual characters.

8 (Sparse text: Find as much text as possible in no particular order): This mode performs OCR on the entire image and tries to find as much text as possible, disregarding any specific order or structure.

9 (Sparse text with OSD): This mode performs OCR on the entire image, looking for sparse text, and includes OSD for orientation and script detection.


{
  "predictions": [
    {
      "x": 341,
      "y": 181.5,
      "width": 44,
      "height": 15,
      "confidence": 0.89,
      "class": "plaque"
    },
    {
      "x": 169.5,
      "y": 175.5,
      "width": 49,
      "height": 19,
      "confidence": 0.806,
      "class": "plaque"
    }
  ]
}"""