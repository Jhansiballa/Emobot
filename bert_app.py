from flask import Flask, request, jsonify, session, render_template
import random
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from flask_cors import CORS

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("nateraw/bert-base-uncased-emotion")
model = BertForSequenceClassification.from_pretrained("nateraw/bert-base-uncased-emotion")

# Define emotion categories
emotions = ["sadness", "joy", "love", "anger", "fear", "surprise"]

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "chatbot_secret"
CORS(app)

def predict_emotion(text):
    """Predict emotion from input text using the BERT model."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
    max_prob, predicted_class = torch.max(probabilities, dim=1)

    if max_prob.item() < 0.20:  
        return "neutral"

    return emotions[predicted_class.item()] if 0 <= predicted_class.item() < len(emotions) else "neutral"

def get_chatbot_response(user_message):
    """Generate chatbot response based on emotion and conversation history."""
    user_message = user_message.lower().strip()

     # If user replies "yes", return an engaging response
    if user_message in ["yes", "yeah", "sure", "yup", "okay"]:
        return random.choice([
            "Great! Let's continue!",
            "Okay! What’s on your mind?",
            "Awesome! Tell me more.",
            "Sounds good! Let’s talk!"
        ])
    
    if user_message in ["hello", "hi", "hey", "hola", "hiya", "hii"]:
        return random.choice([
            "Hey there! How’s your day going?",
            "Hello! What’s on your mind?",
            "Hi! How can I help you today?",
            "Hey! It’s great to see you. What’s up?",
            "Hola! How are you feeling today?"
        ])

    knowledge_data = {
        "joy": ["That's wonderful! 😊 ", "Keep smiling! 😊 Tell me more!"],
        "sadness": ["I'm here for you. Want to talk? 💙", "You're not alone. What happened?"],
        "anger": ["I understand your frustration. Want to share?", "It's okay to be angry. Let's talk."],
        "fear": ["That sounds scary! What’s making you feel this way?", "It's okay to be anxious. I'm here."],
        "surprise": ["Wow! That sounds unexpected. What happened?", "That must have been quite a surprise!"],
        "love": ["Love is a beautiful thing! 💖 Tell me more!", "That's amazing! Who made you feel this way?"],
        "neutral": ["I'm here to chat! How are you feeling today?", "Tell me about your day! 😊"]
    }

    follow_up_questions = {
        "joy": ["What else made you happy today?", "Would you like to share a happy memory?"],
        "sadness": ["Do you want to talk about what's making you sad?", "What can I do to cheer you up?"],
        "anger": ["What happened that made you feel this way?", "Do you want to talk about it?"],
        "fear": ["What are you afraid of?", "I'm here to listen, what's worrying you?"],
        "love": ["Love is beautiful! Tell me more about it!", "What made you feel this love today?"]
    }

    response_levels = {
    "joy": [
        "That’s amazing! Tell me more about what’s making you happy! 😊",
        "I love hearing that! What’s been the best part of your day?",
        "Happiness looks good on you! Keep shining! ✨",
        "Yay! Let’s celebrate this happy moment together! 🎉",
        "I’m so happy for you! What’s making you feel this way?",
        "Woohoo! If I had confetti, I’d be throwing it right now! 🎊",
        "Happiness detected! Engaging celebration mode! 🥳",
        "I wish I had hands to high-five you! Imagine a virtual high-five! 🙌",
        "Smiling is my favorite, and you just made me smile! 😊"
    ],
    "sadness": [
        "I'm here for you. Want to talk? 💙",
        "It's okay to feel this way. Do you want to share what happened?",
        "Sometimes sharing helps. What can I do to support you?",
        "It’s okay to feel sad. You are stronger than you think.",
        "You’ve gotten through hard times before, and you will again.",
        "I know things might be tough right now, but you are not alone.",
        "Feelings come and go, but I’ll always be here to listen.",
        "Take your time. I’m here whenever you need me.",
        "You are valued and important. Never forget that.",
        "Sometimes, talking about it helps. Want to share?",
        "You don’t have to go through this alone. I’ll be here for you.",
        "If I could give you a hug, I would! 🤗",
        "You deserve kindness, even from yourself. Be gentle with your heart."
    ],
    "anger": [
        "I understand your frustration. What happened?",
        "Let's process this together. What’s bothering you the most?",
        "I hear you. Want to talk about what’s upsetting you?",
        "It’s okay to feel angry. Let’s work through this together.",
        "I understand that this must be frustrating for you.",
        "I’m here to listen. What happened?",
        "Your feelings are valid. Tell me more about what’s going on.",
        "I appreciate you sharing this with me. How can I support you?",
        "What’s something that usually helps you feel better when you’re angry?"
    ],
    "fear": [
        "That sounds scary! What’s making you feel this way?",
        "It's okay to be anxious. I'm here to listen.",
        "Facing fears is tough. What’s on your mind?",
        "It’s okay to be scared. You’re not alone in this.",
        "Fear can be overwhelming, but I’m here for you.",
        "I understand that this must be really tough for you.",
        "Your feelings are valid. Want to share more about what’s worrying you?",
        "You’re stronger than your fears. I believe in you!",
        "It’s okay to take things one step at a time.",
        "You’ve faced challenges before, and you’ll get through this too.",
        "I’m here to support you. You’re not alone in this.",
        "Take a deep breath. You’re safe here with me.",
        "I know it’s scary, but you’re not alone. I’m here to listen.",
        "What can I do to help you feel a little calmer?"
    ],
    "surprise": [
        "Wow! That sounds unexpected. What happened?",
        "That must have been quite a surprise! How did you react?",
        "Unexpected things can be fun or scary. How did it make you feel?",
        "Surprises make life exciting! Was it a good one?",
        "Unexpected moments can be the best! How do you feel about it?",
        "It sounds like something interesting happened! What’s the full story?",
        "Life’s full of surprises! What did you think of this one?",
        "Whoa! I didn’t see that coming! Did you?",
        "Plot twist! That must have been exciting!",
        "Surprises keep things interesting! Was it a good shock or a bad one?",
        "Tell me more—I love surprises!",
        "That sounds like a big moment! How did you react?",
        "I love surprises! Was this one pleasant or shocking?",
        "Wow! What an interesting turn of events!",
        "Did it completely catch you off guard? What happened next?"
    ],
    "love": [
        "Love is a beautiful thing! 💖 Tell me more!",
        "That's amazing! Who or what made you feel this way?",
        "Love brings happiness. What’s something special about it for you?",
        "Love is a gift! Cherish every moment of it!",
        "You deserve all the love in the world! 💕",
        "It’s heartwarming to hear that you’re feeling so much love!",
        "Love is what connects us all—keep spreading it!",
        "Ooh, I love love! 💘 Tell me more!",
        "Sounds like a love story in the making! 😍",
        "Love detected! Engaging warm and fuzzy mode! 🥰",
        "Who’s the lucky one making you feel this way?",
        "Love is such a special emotion. What makes this one different?",
        "That’s wonderful! How do you express your love in return?",
        "This sounds like a moment to cherish. How did it all begin?",
        "Love is powerful! What’s one thing about love that inspires you?"
    ],
    "neutral": [
        "I'm here to chat! How are you feeling today?",
        "Tell me about your day! 😊",
        "What's on your mind right now?"
    ]
}

    detected_emotion = predict_emotion(user_message)
    chatbot_reply = random.choice(knowledge_data.get(detected_emotion, knowledge_data["neutral"]))

    # Retrieve conversation history from session
    conversation_history = session.get("conversation", [])

    chatbot_reply = random.choice(response_levels.get(detected_emotion, response_levels["neutral"]))

    # Add chatbot response to history
    conversation_history.append({"user": user_message, "bot": chatbot_reply})

    # Save history back to session
    session["conversation"] = conversation_history

    # If the bot detects an emotion, ask a follow-up question
    if detected_emotion in follow_up_questions and len(conversation_history) > 2:
        chatbot_reply += " " + random.choice(follow_up_questions[detected_emotion])

    return chatbot_reply


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    chatbot_reply = get_chatbot_response(user_message)  # Get the chatbot response
    detected_emotion = predict_emotion(user_message)   # Get detected emotion
    
    return jsonify({"reply": chatbot_reply, "emotion": detected_emotion})  # Return correct variables



if __name__ == "__main__":
    app.run(debug=True)
