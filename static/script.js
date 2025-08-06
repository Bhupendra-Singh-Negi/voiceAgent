// text to voice
document.getElementById("btn").addEventListener("click", async () => {
    const text = document.getElementById("textInput").value.trim();
    if(!text){
        alert("Enter some text");
        return;
    }
    const payload = {
        text: text,
        voice_id: "en-US-terrell"  // Add this line (default Murf voice ID)
    };
    const response = await fetch("/generate-audio", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    const data = await response.json();
    

    if (data.audio_url) {
        document.getElementById("audioResult").innerText = data.audio_url;
        const player = document.getElementById("player");
        player.src = data.audio_url;
        player.style.display = "block";
        player.play(); // auto-play when loaded
    } else {
        alert("Error: " + (data.error || "Unknown error"));
    }
});

//echo bot
let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById("startRecording");
const stopBtn = document.getElementById("stopRecording");
const echoPlayer = document.getElementById("echoPlayer");

startBtn.addEventListener("click", async () => {
    try {
         const options = { mimeType: 'audio/webm;codecs=opus' };

        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            alert("WebM/Opus not supported in this browser.");
            return;
        }

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const audioUrl = URL.createObjectURL(audioBlob);
            echoPlayer.src = audioUrl;
            echoPlayer.classList.remove("hidden");
            echoPlayer.play();

            // Upload to server
            const uploadStatus = document.getElementById("uploadStatus");
            uploadStatus.innerText = "Uploading...";

            const formData = new FormData();
            const filename = `recording-${Date.now()}.webm`;
            formData.append("file", audioBlob, filename);

            fetch("/upload-audio", {
                method: "POST",
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                uploadStatus.innerText = `✅ Uploaded: ${data.filename} (${data.size_kb} KB)`;
            })
            .catch(err => {
                uploadStatus.innerText = "❌ Upload failed: " + err.message;
            });
        };


        mediaRecorder.start();
         
        startBtn.classList.add("opacity-70");
        startBtn.disabled = true;
        stopBtn.disabled = false;
    } catch (error) {
        alert("Could not access microphone: " + error.message);
    }
});

stopBtn.addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();

        startBtn.classList.remove("opacity-70");
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
});