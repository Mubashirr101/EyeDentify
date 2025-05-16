from flask import Flask, render_template, request, jsonify
import cv2
import os
import numpy as np
import face_recognition
import base64
from io import BytesIO
from PIL import Image
from supabase_client import supabase1
from datetime import datetime, timedelta
import pickle
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# load encoding files
with open("EncodeFile.p", "rb") as file:
    knownEncodelist, empID = pickle.load(file)

# counter
last_seen = {}


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

    emp_id = "Unknown"
    name = "Unknown"
    last_loggedIn = "Unknown"
    department = "Unknown"

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(knownEncodelist, encodeFace)
        faceDis = face_recognition.face_distance(knownEncodelist, encodeFace)
        if len(faceDis) > 0:
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                emp_id = empID[matchIndex].upper()
                print("Face matched")
                print(emp_id)
                # y1, x2, y2, x1 = faceLoc
                # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                # cv2.rectangle(img_np, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # cv2.rectangle(img_np, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                # cv2.putText(
                #     img_np,
                #     name,
                #     (x1 + 6, y2 - 6),
                #     cv2.FONT_HERSHEY_COMPLEX,
                #     1,
                #     (255, 255, 255),
                #     2,
                # )

                # time-interval based repeated entires prevention in eyetandance & eyesuite

                # log the login time
                # now = datetime.now()

                # get emp data

                try:
                    res = supabase1.table("emp").select("*").eq("id", emp_id).execute()
                    emp = res.data[0]
                    name = emp["name"]
                    last_loggedIn = emp.get("last_attendance_time", "N/A")
                    department = emp["department"]
                    supabase1.table("emp").update(
                        {"last_attendance_time": datetime.now().isoformat()}
                    ).eq("id", emp_id).execute()
                except Exception as e:
                    print(f"Error fetching or updating employee data: {e}")
                    # Optionally, return a JSON error response here

                break

    return jsonify(
        {
            "name": name,
            "id": emp_id,
            "department": department,
            "last_LoggedIn": last_loggedIn,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
