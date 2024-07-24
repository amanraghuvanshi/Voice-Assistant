# Libraries
import os
import openai
import base64
import streamlit as st
from audio_recorder_streamlit import audio_recorder  # For recording the audio

response_token = os.getenv('API_KEY')

# initializing the openai client
def openai_setup(OPENAI_TOKEN):
    return openai.OpenAI(api_key = OPENAI_TOKEN)

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
    resp.stream_to_file(audio_path)
    
# front page of the application
def main():
    st.sidebar.title("Secret Key Configuration")
    OPENAI_TOKEN = st.sidebar.text_input("Please share your secret key with us: ", type = "password")
    
    
    st.title("Aura Voice Channel 💎")
    st.write("Hi, This is Aura ✨. Hope you are doing well. Let me know, how may I help you!")
    
    if OPENAI_TOKEN:
        client = openai_setup(OPENAI_TOKEN)
        record_audio = audio_recorder()
        
        # If recording done
        if record_audio:
            audio_file = "audio.mp3"
            with open(audio_file, "wb") as f:
                f.write(record_audio)
                
            transcribe_text = translate_audio(client=client, audio_path=audio_file)
            st.write("Translated Text: ", transcribe_text)
            
            generated_resp = fetch_response(client=client, input_data=transcribe_text)
            
            resp_audio = "response.mp3"
            text_to_audio(client=client, text=generated_resp, audio_path=resp_audio)
            st.audio(resp_audio)
            
            st.write("Resolution: ", generated_resp)
    
# The design for the main page

    
    
if __name__ == "__main__":
    main()