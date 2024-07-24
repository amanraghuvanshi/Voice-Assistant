# Libraries
import openai
import base64
import streamlit as st
from audio_recorder_streamlit import audio_recorder  # For recording the audio

# initializing the openai client
def openai_setup(secret_key):
    return openai.OpenAI(api_key = secret_key)

# translation of audio to text
def translate_audio(client, audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model = "whisper-1", file = "audio_file")
        return transcript.text
    
# sending the text to OpenAI
def fetch_response(client, input_data):
    messages = [{"role": "user", "content" : input_data}]
    resp = client.chat.completions.create(model = "gpt-3.5-turbo-1106", messages = messages)
    return resp.choices[0].message.content

# Conversion of text to audio
def text_to_audio(client, text, audio_path):
    resp = client.audio.speech.create(model = "tts-1", voice = "onyx", input = text)

# front page of the application
def main():
    st.sidebar.title("Secret Key Configuration")
    api_key = st.sidebar.text_input("Please share your secret key with us: ", type = "password")
    
    
    st.title("Aura Voice Channel 💎")
    st.write("Hi, This is Aura ✨. Hope you are doing well. Let me know, how may I help you!")
    record_audio = audio_recorder()
    
# The design for the main page

    
    
if __name__ == "__main__":
    main()