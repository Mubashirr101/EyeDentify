from flask import Flask, render_template, request, jsonify, url_for
import cv2
import os
import numpy as np
import face_recognition
import base64
from io import BytesIO
from PIL import Image
from supabase_client import supabase1, supabase2
from datetime import datetime, timedelta
from dateutil import tz
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
    imgurl = url_for("static", filename="images/placeholderavatar.png")

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
                    last_logged_In = emp.get("last_attendance_time", "N/A")
                    if last_logged_In is None:
                        last_logged_In = "N/A"
                    print(last_logged_In)
                    try:
                        # Parssingg the UTC timestamp from Supabase 
                        dt = datetime.fromisoformat(last_logged_In.replace('Z', '+00:00'))
                        # Ensure it's treated as UTC
                        dt_utc = dt.replace(tzinfo=tz.UTC)
                        # Convert to local time for india
                        dt_local = dt_utc.astimezone(tz.gettz("Asia/Kolkata"))
                        dt = dt_local.strftime("%d-%m-%Y %H:%M")
                    except ValueError:
                        dt = "N/A"
                    last_loggedIn = dt
                    department = emp["department"]

                    fetchimg = supabase2.storage.from_("emp-images").create_signed_url(
                        f"Images/{emp_id}.jpg", 3600
                    )

                    imgurl = fetchimg["signedURL"]
                    print(imgurl)

                    
                except Exception as e:
                    print(f"Error fetching or updating employee data: {e}")

                break

    return jsonify(
        {
            "name": name,
            "id": emp_id,
            "department": department,
            "last_LoggedIn": last_loggedIn,
            "imgurl": imgurl,
        }
    )


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    emp_id = data.get("emp_id")
    if not emp_id:
        return jsonify({"success": False, "message": "Employee ID missing"})
    
    print(f"Login attempt for emp_id: {emp_id}")
    try:
        # getting current UTC time and storing in UTC
        now_utc = datetime.now(tz.UTC).isoformat()
        print(f"Updating with UTC time: {now_utc}")
        supabase1.table("emp").update(
            {"last_attendance_time": now_utc}
        ).eq("id", emp_id).execute()
        print("Update executed")
        
        # getting da updated time for response
        res = supabase1.table("emp").select("last_attendance_time").eq("id", emp_id).execute()
        print(f"Fetch result: {res.data}")
        last_time = res.data[0]["last_attendance_time"]
        print(f"Last time fetched: {last_time}")
        if last_time is None:
            last_time = "N/A"
        else:
            try:
                #convert to local time for display
                dt = datetime.fromisoformat(last_time.replace('Z', '+00:00'))
                dt_utc = dt.replace(tzinfo=tz.UTC)
                dt_local = dt_utc.astimezone(tz.gettz("Asia/Kolkata")) # indian time
                last_time = dt_local.strftime("%d-%m-%Y %H:%M")
            except ValueError:
                last_time = "N/A"
        
        return jsonify({"success": True, "last_LoggedIn": last_time})
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({"success": False, "message": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
