import os
import cv2
import face_recognition
from supabase_client import supabase2
import pickle

# import student images from cloud

# Load known faces
path = "Images"
images = []
empID = []
myList = os.listdir(path)

# adding all the imgs and their names in 2 individual arrays
for cl in myList:
    curImg = cv2.imread(f"{path}/{cl}")
    images.append(curImg)
    empID.append(os.path.splitext(cl)[0])

    imgpath = os.path.join(path, cl)
    with open(imgpath, "rb") as f:
        supabase2.storage.from_("emp-images").upload(f"Images/{cl}", f)


print("emp id: ", empID)


def findEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


print("Encoding Started")
knownEncodelist = findEncoding(images)
knownEncodelistWithIds = [knownEncodelist, empID]
print("Encoding Complete")

file = open("EncodeFile.p", "wb")
pickle.dump(knownEncodelistWithIds, file)
file.close()
print("Encoding Saved")
