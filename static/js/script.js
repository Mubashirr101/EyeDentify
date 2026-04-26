const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const resultText = document.getElementById("result");
const context = canvas.getContext("2d");
const pname = document.getElementById("name")
const pid = document.getElementById("empId")
const pdept = document.getElementById("dept")
const plogintime = document.getElementById("lastloggedin")
const imurl = document.getElementById("loginavatar")
const retakebtn = document.getElementById("retake")
const loginbtn = document.getElementById("loginbtn")

let intervalId = null;
let isProcessing = false;
let hasMatched = false;
let currentEmpId = null;

function startrecogloop(){
    intervalId = setInterval(() => {
        if(isProcessing || hasMatched) return; //preventing overlap or repeated match
        isProcessing = true;

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
            imurl.src = `${data.imgurl}`

            if (data.name!=="Unknown"){
                clearInterval(intervalId);
                intervalId = null;
                hasMatched = true;
                currentEmpId = data.id;
            }
           })
            .catch((err) => {
            console.error("Error sending frame:", err);
            })
            .finally(()=>{
             isProcessing = false;
            });            
        }, 1000); // adjust timing as needed
    }

// Start the webcam stream
navigator.mediaDevices
.getUserMedia({ video: true })
.then((stream) => {
    video.srcObject = stream;
})
.catch((err) => {
    console.error("Camera access error: ", err);
});
startrecogloop()

//reset on retake
retakebtn.addEventListener("click",()=> {
    if (!intervalId){
        resultText.textContent = "Recognized: None";
        pname.textContent = "Name";
        pid.textContent = "ID";
        pdept.textContent = "Department";
        plogintime.textContent = "Last Login Time";
        imurl.src = "static/images/placeholderavatar.png";

        hasMatched = false;
        isProcessing = false;
        currentEmpId = null;
        startrecogloop();
    }
}
);

//login button
loginbtn.addEventListener("click", () => {
    if (currentEmpId && hasMatched) {
        fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ emp_id: currentEmpId }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Login successful!");
                plogintime.textContent = `Last Login: ${data.last_LoggedIn}`;
            } else {
                alert("Login failed: " + data.message);
            }
        })
        .catch((err) => {
            console.error("Error logging in:", err);
        });
    } else {
        alert("No employee recognized. Please try again.");
    }
});