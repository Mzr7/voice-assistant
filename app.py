import streamlit as st
import feedparser
import requests
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import base64
import io
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="Personal AI Assistant", page_icon="🤖", layout="wide")

# Initialize Session States
if "reminders" not in st.session_state:
    st.session_state.reminders = []
if "news_url" not in st.session_state:
    st.session_state.news_url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

# --- CORE LOGIC FUNCTIONS ---

def speak(text):
    """Converts text to speech and auto-plays in the browser."""
    if text:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
        st.markdown(md, unsafe_allow_html=True)

def get_weather(city):
    """Fetches real-time weather using Open-Meteo for any city name."""
    try:
        geo_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
        geo_res = requests.get(geo_url, headers={'User-Agent': 'AssistantApp'}).json()
        if not geo_res: return f"I couldn't find a location named {city}."
        
        lat, lon = geo_res[0]['lat'], geo_res[0]['lon']
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(w_url).json()
        temp = w_res['current_weather']['temperature']
        return f"The current temperature in {city} is {temp}°C."
    except:
        return "Weather service is currently unavailable."

def get_multiple_news(limit=5):
    """Parses multiple news entries from the RSS feed."""
    feed = feedparser.parse(st.session_state.news_url)
    items = []
    voice_briefing = "Here are the top headlines. "
    
    for i, entry in enumerate(feed.entries[:limit]):
        items.append({"title": entry.title, "link": entry.link})
        voice_briefing += f"Headline {i+1}: {entry.title}. "
        
    return items, voice_briefing

# --- UI & BACKGROUND TIMER ---

st.title("🎙️ Voice Personal Assistant")

# Timer Heartbeat (Checks every 5s)
@st.fragment(run_every="5s")
def check_reminders_periodically():
    now = datetime.now()
    for r in st.session_state.reminders:
        if now >= r['time'] and not r['done']:
            r['done'] = True
            msg = f"Reminder: It's time to {r['task']}!"
            st.toast(msg, icon="🔔")
            speak(msg)
            st.rerun()

check_reminders_periodically()

# Main Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Voice Commands")
    st.write("Try: 'Weather in Kannur', 'Latest News', or 'Remind me in 1 minute to check email'")
    
    # Microphone Input
    voice_text = speech_to_text(language='en', start_prompt="🎙️ Click to Speak", just_once=True, key='main_mic')

    if voice_text:
        query = voice_text.lower()
        st.info(f"Recognized: {query}")

        # WEATHER LOGIC
        if "weather" in query:
            city = query.split("weather in")[-1].strip() if "weather in" in query else "London"
            report = get_weather(city)
            st.success(report)
            speak(report)

        # NEWS LOGIC (Multiple Items)
        elif "news" in query:
            news_items, briefing = get_multiple_news(5)
            st.subheader("📰 Latest Headlines")
            for item in news_items:
                st.markdown(f"- [{item['title']}]({item['link']})")
            speak(briefing)

        # REMINDER LOGIC
        elif "remind" in query:
            try:
                # Extracts minutes and task
                mins = int([s for s in query.split() if s.isdigit()][0])
                task = query.split("to")[-1].strip()
                t_time = datetime.now() + timedelta(minutes=mins)
                st.session_state.reminders.append({"task": task, "time": t_time, "done": False})
                speak(f"Set a reminder for {task} in {mins} minutes.")
            except:
                speak("I couldn't catch the time. Please say something like 'remind me in 2 minutes to take tea'.")

with col2:
    st.header("Assistant Status")
    st.subheader("📌 Reminders List")
    if st.session_state.reminders:
        for r in st.session_state.reminders:
            status = "✅ Done" if r['done'] else f"⏳ at {r['time'].strftime('%H:%M:%S')}"
            st.write(f"**{r['task']}** ({status})")
    else:
        st.write("No active reminders.")