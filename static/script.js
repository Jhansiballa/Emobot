document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");

    function addMessage(text, sender) {
        const message = document.createElement("div");
        message.className = sender === "user" ? "user-message" : "bot-message";
        message.innerHTML = `<strong>${sender === "user" ? "You" : "Chatbot"}:</strong> ${text}`;
        chatBox.appendChild(message);
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll
        return message;
    }

    function addActionButton(emotion, parentElement) {
        let button = document.createElement("button");
    
        const emotionActions = {
            "joy": { text: "Play", url: "https://playtictactoe.org/" },
            "sadness": { text: "Book", url: "https://www.gutenberg.org/ebooks/4507" },
            "anger": { text: "Meme", url: "https://www.memedroid.com/" },
            "fear": { text: "Relax", url: "https://www.calm.com/" },
            "surprise": { text: "Learn More", url: "https://www.wikipedia.org/" },
            "love": { text: "Listen to Love Songs", url: "https://open.spotify.com/playlist/37i9dQZF1DWXb9I5xoXLjp" },
            "neutral": { text: "Explore", url: "https://www.google.com/" }
        };
    
        if (emotionActions[emotion]) {
            button.innerText = emotionActions[emotion].text;
            button.classList.add("emotion-button");
            button.onclick = function () {
                window.open(emotionActions[emotion].url, "_blank");
            };
            parentElement.appendChild(button);
        }
    }
    

    window.sendMessage = function () {
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        addMessage(userMessage, "user");
        userInput.value = "";  // Clear input

        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            let botMessage = addMessage(data.reply, "bot");

            // Add emotion-based button
            if (data.emotion) {
                addActionButton(data.emotion, botMessage);
            }
        })
        .catch(error => console.error("Error:", error));
    };

    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") sendMessage();
    });

    // Bot's First Message
    setTimeout(() => {
        addMessage("Hello! How are you feeling today? 😊", "bot");
    }, 500);
});
