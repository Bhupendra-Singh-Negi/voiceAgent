document.getElementById("btn").addEventListener("click", async () => {
            const text = document.getElementById("textInput").value;

            const response = await fetch("/generate-audio", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text })
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