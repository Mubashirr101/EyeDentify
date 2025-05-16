# EyeDentify

**EyeDentify** is a real-time face recognition web application built using Flask, OpenCV, and the `face_recognition` library. It captures video from a webcam, processes the frames in real time, and identifies faces based on a set of pre-encoded images. The app uses [Supabase](https://supabase.com/) for both facial data (Postgres) and cloud image storage.

---

## 🚀 Features

- 🔍 Real-time face recognition using webcam
- 🧠 Utilizes pre-trained face encodings from local image files
- 🖥️ Web-based UI with live video and recognition feedback
- ☁️ **Supabase integration** for facial database and cloud image storage
- 🧰 Modular and easy-to-extend code structure

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, JavaScript (WebRTC, Canvas API)
- **Backend**: Python (Flask)
- **Libraries**: OpenCV, face_recognition, NumPy, Pillow
- **Database & Storage**: Supabase (Postgres, Storage)

---

## 🖼️ Preparing Your Dataset

1. Place clear face images in the `Images/` folder.
2. Each image file name (without extension) will be used as the label.
3. Example:
   ```
   Images/
   ├── Alice.jpg
   ├── Bob.png
   ```

---

## ☁️ Supabase Integration

### 1. **Supabase Client Setup**

- The project uses two Supabase clients:
  - `supabase1`: For database (Postgres) operations (employee info, attendance).
  - `supabase2`: For storage operations (image upload/list).
- API keys are loaded from `.env`:
  - `spbkey` for database access
  - `sb_sr_key` for storage access

See [`supabase_client.py`](supabase_client.py):

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/eyedentify.git
cd eyedentify
```

### 2. Install Dependencies

Ensure you're using Python 3.7 or higher.

```bash
pip install -r requirements.txt
```

> Note: `face_recognition` depends on `dlib`. For installation help on different platforms, refer to the [face_recognition GitHub](https://github.com/ageitgey/face_recognition#installation).

### 3. Configure Environment Variables

Create a `.env` file in your project root with your Supabase keys:

```
spbkey=your_supabase_anon_key
sb_sr_key=your_supabase_service_role_key
sburl=your_supabase_project_url
```

### 4. Run the Application

```bash
python app.py
```

Then open your browser and go to: [http://localhost:5000](http://localhost:5000)

---

## 🧪 How It Works

- On launch, the app encodes all face images from `Images/` and uploads new ones to Supabase Storage.
- The browser captures webcam frames and sends them to the backend.
- The backend compares the incoming face encodings with the known ones.
- The details and ID of the matched face are fetched from the Supabase database.
- The last login time is updated in Supabase.
- Results are displayed in the UI.

---

## 📁 Project Structure

```
EyeDentify/
├── app.py
├── encode_imgs.py
├── supabase_client.py
├── Images/
├── EncodeFile.p
├── requirements.txt
├── .env
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── script.js
└── templates/
    └── index.html
```

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0**.
You may redistribute, modify, and share the software under the terms of the GPL.

For more details, see the full license text here: [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

---