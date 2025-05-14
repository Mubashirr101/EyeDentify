const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const resultText = document.getElementById("result");
const context = canvas.getContext("2d");
const pname = document.getElementById("name")
const pid = document.getElementById("empId")
const pdept = document.getElementById("dept")
const plogintime = document.getElementById("lastloggedin")
// Start the webcam stream
navigator.mediaDevices
.getUserMedia({ video: true })
.then((stream) => {
    video.srcObject = stream;
})
.catch((err) => {
    console.error("Camera access error: ", err);
});

// Send a frame every second
setInterval(() => {
context.drawImage(video, 0, 0, canvas.width, canvas.height);
const dataURL = canvas.toDataURL("image/jpeg");

fetch("/process_frame", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: dataURL }),
})
    .then((response) => response.json())
    .then((data) => {
    resultText.textContent = `Recognized: ${data.name}`;
    pname.textContent = `Name: ${data.name}`;
    pid.textContent = `ID: ${data.id}`;
    pdept.textContent = `DEPT: ${data.department}`;
    plogintime.textContent = `Last Login: ${data.last_LoggedIn}`;

    })
    .catch((err) => {
    console.error("Error sending frame:", err);
    });
}, 1000); // adjust timing as needed