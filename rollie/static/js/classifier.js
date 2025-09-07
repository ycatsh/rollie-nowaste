const video = document.getElementById("reader");
const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
const resultDiv = document.getElementById("result");
const nextBtn = document.getElementById("nextBtn");

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => { video.srcObject = stream; })
  .catch(err => console.error("Error accessing webcam:", err));

nextBtn.addEventListener("click", () => {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL("image/jpeg");

    resultDiv.textContent = "Classifying...";

    fetch("/tmp/garbage/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: dataUrl })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            resultDiv.textContent = "Error: " + data.error;
            resultDiv.className = "fail";
        } else {
            resultDiv.innerHTML = `<b>Prediction:</b> ${data.class} <br>
                                   <b>Confidence:</b> ${data.confidence}%`;
            resultDiv.className = data.confidence >= 80 ? "success" : "";
        }
    })
    .catch(err => {
        resultDiv.textContent = "Error: " + err;
        resultDiv.className = "fail";
    });
});
