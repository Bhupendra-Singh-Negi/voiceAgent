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
    console.log("Server response:", data);  // 👈 Add this line
    
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