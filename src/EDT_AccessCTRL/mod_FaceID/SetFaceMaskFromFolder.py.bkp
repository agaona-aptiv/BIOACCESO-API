
import os
import ST_FaceID
import cv2
import face_recognition

print('******************** Set black facemask to a folder *************************')
faceIdentification = ST_FaceID.ST_FaceID(useTensorFlow=False)
for root, dirs, files in os.walk('Condutel'):
    for file in files:
        if (file.endswith('jpg')):
            path = os.path.join(root, file)
            image = face_recognition.load_image_file(path)
            image = image[:, :, ::-1] ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            facemaskList = faceIdentification.GetFaceMasksImages(image)
            if (len(facemaskList)>1):
                newpath = path.replace('.jpg','_2.jpg')
                cv2.imwrite(newpath,facemaskList[2])
            else:
            	print('Not saved: ' + path)


