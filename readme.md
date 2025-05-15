
---

# EyeDentify

**EyeDentify** is a real-time face recognition web application built using Flask, OpenCV, and the `face_recognition` library. It captures video from a webcam, processes the frames in real time, and identifies faces based on a set of pre-encoded images.

## 🚀 Features

* 🔍 Real-time face recognition using webcam
* 🧠 Utilizes pre-trained face encodings from local image files
* 🖥️ Web-based UI with live video and recognition feedback
* 🗃️ Supabase server for database and cloud storage
* 🧰 Modular and easy-to-extend code structure

## 🛠️ Tech Stack

* **Frontend**: HTML5, JavaScript (WebRTC, Canvas API)
* **Backend**: Python (Flask)
* **Libraries**: OpenCV, face\_recognition, NumPy, Pillow
* **Server**: Supabase


## 🖼️ Preparing Your Dataset

1. Place clear face images in the `Images/` folder.
2. Each image file name (without extension) will be used as the label.
3. Example:

   ```
   Images/
   ├── Alice.jpg
   ├── Bob.png
   ```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/eyedentify.git
cd eyedentify
```

### 2. Install Dependencies

Ensure you're using Python 3.7 or higher.

```bash
pip install flask opencv-python face_recognition numpy pillow
```

> Note: `face_recognition` depends on `dlib`. For installation help on different platforms, refer to the [face\_recognition GitHub](https://github.com/ageitgey/face_recognition#installation).

### 3. Run the Application

```bash
python app.py
```

Then open your browser and go to: [http://localhost:5000](http://localhost:5000)

## 🧪 How It Works

* On launch, the app encodes all face images from `Images/`.
* The browser captures webcam frames and sends them to the backend.
* The backend compares the incoming face encodings with the known ones.
* The details and ID of the matched face are fetched from the supabase server.
* They are then displayed in the UI.



## 📜 License

This project is licensed under the **GNU General Public License v3.0**.
You may redistribute, modify, and share the software under the terms of the GPL.

For more details, see the full license text here: [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

---
