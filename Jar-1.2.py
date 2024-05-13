import os
import openai
from google.cloud import texttospeech
import speech_recognition as sr

# Google Cloud Speech-to-Text setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_google_credentials.json"
speech_client = sr.Recognizer()

# Google Text-to-Speech setup
tts_client = texttospeech.TextToSpeechClient()

# OpenAI setup
OPENAI_KEY = ""
openai.api_key = OPENAI_KEY

def speak_text(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice_params, audio_config=audio_config)

    with open("output.wav", "wb") as out:
        out.write(response.audio_content)
    os.system("aplay output.wav")

def record_text():
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = speech_client.listen(source)

        try:
            text = speech_client.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

def send_to_openai(messages, model="gpt-3.5-turbo"):
    response = openai.Completion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    messages = response.choices[0].message["content"]
    messages.append(response.choices[0].message)
    return messages

messages = [{"role": "user", "content": "act like jarvis from ironman"}]
while True:
    user_input = record_text()
    messages.append({"role": "user", "content": user_input})
    response = send_to_openai(messages)
    speak_text(response)
    print(response)
