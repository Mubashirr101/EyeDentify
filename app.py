from flask import Flask, render_template, request, jsonify
import cv2
import os
import numpy as np
import face_recognition
import base64
from io import BytesIO
from PIL import Image
from supabase import create_client, Client

app = Flask(__name__)

# Load known faces
path = "ImagesBasic"
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f"{path}/{cl}")
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

encodeList = []
for img in images:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]
    encodeList.append(encode)

print("Encoding Complete")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process_frame", methods=["POST"])
def process_frame():
    data = request.get_json()
    image_data = data["image"].split(",")[1]
    image_bytes = base64.b64decode(image_data)

    # Convert to numpy array
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    img_np = np.array(img)
    img_small = cv2.resize(img_np, (0, 0), None, 0.25, 0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(img_small)
    encodesCurFrame = face_recognition.face_encodings(img_small, facesCurFrame)

    name = "Unknown"

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeList, encodeFace)
        faceDis = face_recognition.face_distance(encodeList, encodeFace)
        if len(faceDis) > 0:
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print("one match & saving")
                print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img_np, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img_np, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(
                    img_np,
                    name,
                    (x1 + 6, y2 - 6),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                )
                break

    return jsonify({"name": name})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
