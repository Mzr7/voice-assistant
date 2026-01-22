🎙️ Voice-Activated Personal Assistant
A minimalist, interactive digital companion built with Python and Streamlit. This assistant leverages real-time speech recognition and text-to-speech to help you manage your day hands-free.

🚀 Features
Dynamic Weather Search: Get live weather updates for any city (e.g., "Kannur", "New York") using geocoding and the Open-Meteo API.

Latest News Briefings: Fetches the top 5 headlines and summaries from global RSS feeds using feedparser.

Smart Voice Reminders: Set time-based reminders verbally. A background "heartbeat" monitors the clock and triggers a voice alert when time is up.

Voice-First Experience: Integrated Speech-to-Text (STT) for commands and Text-to-Speech (TTS) for audio responses.

Real-time Dashboard: A clean Streamlit UI that displays transcripts, active reminders, and news cards.

🛠️ Tech Stack
Frontend: Streamlit

Voice Recognition: streamlit-mic-recorder (Browser-based STT)

Speech Synthesis: gTTS (Google Text-to-Speech)

Data Sources: - News: feedparser (RSS)

Weather: requests + Open-Meteo API

Logic: Python datetime & Session State

📦 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/yourusername/voice-assistant.git
cd voice-assistant
Install dependencies:

pip install streamlit streamlit-mic-recorder feedparser gTTS requests

Run the application:

streamlit run app.py
