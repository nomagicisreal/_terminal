
# import cv2
# from script_ import foreachFile, os

# join = lambda parent, child: os.path.join(parent, child)


# cwd = os.getcwd()
# def cropping(child: str):
#     img = cv2.imread(os.path.join('tmp', child), cv2.IMREAD_UNCHANGED)
#     crop_img = img[350:1850, 850:2350] # 
#     cv2.imwrite(os.path.join('cropped', child), crop_img)

# # os.mkdir('cropped') # must create folder before save
# foreachFile(cropping, parent='tmp')