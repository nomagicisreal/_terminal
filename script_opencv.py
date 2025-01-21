
import cv2
from script import foreachFiles, path, os

cwd = os.getcwd()
def cropping(child: str):
    img = cv2.imread(child)
    crop_img = img[330:1850, 50:1200]
    location = path.join('Photos', path.basename(child))
    cv2.imwrite(location, crop_img) # save after create folder

# foreachFiles(cropping, parent='Photos-001')
