🤖 EMOBOT – Emotion Detecting Chatbot

An AI-powered chatbot that understands human emotions and responds empathetically.
Built with Flask, PyTorch, and BERT, EMOBOT provides personalized, engaging conversations while promoting emotional well-being.

🌟 Features

🔍 Emotion Detection – Detects joy, sadness, anger, fear, surprise, love, neutral from user text using pretrained BERT.

💬 Interactive Chatbot – Generates empathetic and human-like responses.

🎭 Emotion-based Actions – Displays dynamic buttons like:

Joy → Play a game

Sadness → Suggest a book or meme

Fear → Relaxation techniques

Love → Love songs on Spotify

Surprise → Explore Wikipedia

📜 Conversation Memory – Maintains chat history with Flask sessions.

🌐 User-Friendly UI – Responsive HTML/CSS + JavaScript interface.

🛠️ Tech Stack

Backend: Flask, Flask-CORS, Python

AI Model: HuggingFace Transformers (nateraw/bert-base-uncased-emotion) + PyTorch

Frontend: HTML5, CSS3, Vanilla JavaScript

Database (optional): Flask session (in-memory)

📂 Repository Structure
emobot-chatbot/
│── app.py                # Flask backend (API + chatbot logic)
│── requirements.txt       # Dependencies
│── templates/
│   └── index.html         # Chat UI
│── static/
│   └── script.js          # Frontend logic (fetch + dynamic buttons)
│── README.md              # Project overview
│── LICENSE                # MIT License
│── .gitignore             # Ignore Python/env files
│── MINI_PROJECT_FINAL.pdf # Detailed project report

🚀 Getting Started
1. Clone the repo
git clone https://github.com/<your-username>/emobot-chatbot.git
cd emobot-chatbot

2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Run the Flask server
python app.py

5. Open in browser

Go to → http://127.0.0.1:5000

📡 API Usage
Endpoint: POST /chat

Request:

{ "message": "I am feeling happy today" }


Response:

{ 
  "reply": "That’s amazing! Tell me more about what’s making you happy! 😊", 
  "emotion": "joy" 
}

📖 Future Scope

🎙️ Voice & Facial Emotion Detection for richer interaction.

🌍 Multi-language Support for wider accessibility.

🕶️ AR/VR Integration for immersive emotional support.

🤝 Integration into mental health apps for real-world impact.

👩‍💻 Author

Jhansi Balla
B.Tech – Information Technology (4th Year)
MVGR College of Engineering


